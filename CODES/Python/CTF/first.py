e = 17771392811
n = 36451716355
ciphertext = [
    21818807250, 25138307811, 26365807755, 10026020611,
    1468484582, 10026020611, 32993293192, 32993293192,
    34921876242, 30389289795, 1277059574, 32993293192,
    34587172256, 25864278125
]
def trial_division(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return i, n // i
        i += 1
    return None, None

p, q = trial_division(n)
if not p or not q:
    raise ValueError("Failed to factor n.")

phi = (p - 1) * (q - 1)
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

d = modinv(e, phi)
plaintext_nums = [pow(c, d, n) for c in ciphertext]

message = ""
for num in plaintext_nums:
    try:
        byte_data = num.to_bytes((num.bit_length() + 7) // 8, 'big')
        message += byte_data.decode('utf-8')
    except:
        message += f"[0x{num:x}]" 

print("Decrypted message:")
print(message)
