# -*- coding: utf-8 -*-

import secrets, hashlib, bcrypt, operator, random, ast, sys
from Cryptodome.Cipher import AES

# ----- Finite field helpers -----
def modinv(a, p):
    return pow(a % p, p - 2, p)

def moddiv(a, b, p):
    return (a % p) * modinv(b, p) % p

# ----- Ed448 / Weierstrass params -----
q = (1 << 448) - (1 << 224) - 1
a_ed = 1 % q
d_ed = int("0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffffffffffffffffffffffffffffffffffffffffffffffff6756", 16) % q
A_w = (-moddiv(1, 48, q) * ((a_ed*a_ed + 14*a_ed*d_ed + d_ed*d_ed) % q)) % q
B_w = ( moddiv(1, 864, q) * ((a_ed + d_ed) % q) * ((-a_ed*a_ed + 34*a_ed*d_ed - d_ed*d_ed) % q) ) % q
ORDER_L = int("0x3fffffffffffffffffffffffffffffffffffffffffffffffffffffff7cca23e9c44edb49aed63690216cc2728dc58f552378c292ab5844f3", 16)

# ----- Birational maps between Twisted Edwards and Weierstrass -----
def to_weierstrass(x, y):
    num_u = (5*a_ed + a_ed*y - 5*d_ed*y - d_ed) % q
    den_u = (12 - 12*y) % q
    u = moddiv(num_u, den_u, q)
    num_v = (a_ed + a_ed*y - d_ed*y - d_ed) % q
    den_v = (4*x - 4*x*y) % q
    v = moddiv(num_v, den_v, q)
    return (u, v)

# Base point in Edwards coords
X_ed = int("0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa955555555555555555555555555555555555555555555555555555555", 16) % q
Y_ed = int("0xae05e9634ad7048db359d6205086c2b0036ed7a035884dd7b7e36d728ad8c4b80d6565833a2a3098bbbcb2bed1cda06bdaeafbcdea9386ed", 16) % q
Gx_w, Gy_w = to_weierstrass(X_ed, Y_ed)

# ----- Minimal short-Weierstrass EC implementation -----
class Point:
    __slots__ = ("x", "y", "inf")
    def __init__(self, x=None, y=None, inf=False): self.x, self.y, self.inf = x, y, inf
    def is_inf(self): return self.inf
    def __eq__(self, other):
        if self.inf and other.inf: return True
        if self.inf != other.inf: return False
        return self.x % q == other.x % q and self.y % q == other.y % q

O = Point(inf=True)
G = Point(Gx_w % q, Gy_w % q, inf=False)

def point_add(P, Q):
    if P.is_inf(): return Q
    if Q.is_inf(): return P
    if P.x == Q.x and (P.y + Q.y) % q == 0: return O
    if P == Q: s = moddiv(3 * P.x * P.x + A_w, 2 * P.y, q)
    else: s = moddiv((Q.y - P.y) % q, (Q.x - P.x) % q, q)
    rx = (s*s - P.x - Q.x) % q
    ry = (s*(P.x - rx) - P.y) % q
    return Point(rx, ry, inf=False)

def scalar_mul(k, P):
    k = k % ORDER_L
    R = O
    Q = P
    while k > 0:
        if k & 1: R = point_add(R, Q)
        Q = point_add(Q, Q)
        k >>= 1
    return R

# ----- Bit/byte sizes -----
p_order = ORDER_L
k_bytes = 8 * ((p_order.bit_length() + 7) // 8)
k2 = 128
k1 = q.bit_length() - k2

# ----- Hash / KDF helpers -----
def Hash(x: bytes, nin_bits: int, n_bits: int, div: bytes) -> bytes:
    nin, n = nin_bits // 8, n_bits // 8
    r, i = b"", 0
    while len(r) < n:
        r += hashlib.sha256(x + b"||" + div + int(i).to_bytes(8, "big")).digest()
        i += 1
    return r[:n]

F1 = lambda x: Hash(x, k2, k1, b"1")
F2 = lambda x: Hash(x, k1, k2, b"2")
H  = lambda x: Hash(x, k1 + k2, k_bytes, b"H")
xor = lambda a, b: bytes(map(operator.xor, a, b))

# ----- Solver -----
def solve():
    try:
        with open("output.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ Error: `output.txt` not found. Please ensure it's in the same directory.")
        return

    # Parse data from file
    y_line = lines[0]
    Yx_ed, Yy_ed = ast.literal_eval(y_line.split("= ")[1].strip())
    ct_hex = lines[1].split("= ")[1].strip()
    ct_bytes = bytes.fromhex(ct_hex)
    sigs_list = ast.literal_eval("".join(lines[2:]).split("= ")[1].strip())

    # Convert public key Y to Weierstrass coordinates for calculations
    Yx_w, Yy_w = to_weierstrass(Yx_ed, Yy_ed)
    Y_w = Point(Yx_w, Yy_w)
    
    print(f"✅ Data parsed. Searching for the valid signature among {len(sigs_list)} candidates...")

    k1_bytes = k1 // 8
    total_bytes = (k1 + k2) // 8
    found_key = None

    for i, (r_hex, z) in enumerate(sigs_list):
        if (i + 1) % 500 == 0:
            print(f"   ...checked {i+1}/{len(sigs_list)} signatures...")

        r = bytes.fromhex(r_hex)
        c = int.from_bytes(H(r), "big")
        
        # Recompute R' = zG + cY
        zG = scalar_mul(z, G)
        cY = scalar_mul(c, Y_w)
        R_prime = point_add(zG, cY)
        
        if R_prime.is_inf():
            continue
            
        # Unblind the message
        Rx_prime_bytes = R_prime.x.to_bytes(total_bytes, "big")
        m1_prime = xor(Rx_prime_bytes, r)
        
        m1_prime_part1 = m1_prime[:k1_bytes]
        m1_prime_part2 = m1_prime[k1_bytes:]
        m_prime = xor(F2(m1_prime_part1), m1_prime_part2)
        
        # Verify consistency
        if F1(m_prime) == m1_prime_part1:
            print(f"\n🎉 Found valid signature at index {i}!")
            found_key = m_prime
            break
    
    print("\nSearch complete.")

    if found_key:
        print(f"🔑 Recovered secret key _k: {found_key.hex()}")
        key = bcrypt.kdf(password=found_key, salt=b"ICC_CHALLENGE", desired_key_bytes=16, rounds=31337)
        cipher = AES.new(key, AES.MODE_CTR, nonce=b"")
        flag_bytes = cipher.decrypt(ct_bytes)
        print("==========================================")
        print(f"🏁 Decrypted Flag: {flag_bytes.decode()}")
        print("==========================================")
    else:
        print("💔 Could not find a valid signature. Decryption failed.")

if __name__ == "__main__":
    solve()