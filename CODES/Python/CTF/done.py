import os, random, json
import math
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend

# === Dummy curve and parameters ===
max_exp = 10  # arbitrary small bound

class DummyCurve:
    def __init__(self):
        self.params = (0, 1)
    def __repr__(self):
        return "EllipticCurve(y^2 = x^3 + x over GF(p^2))"

base = DummyCurve()

# === Secret and Flag ===
SECRET = int.from_bytes(os.urandom(8), "big")  # 64-bit random secret
FLAG = b"flag{example_demo_flag}"

# === Crypto helper (cryptography AES-CBC) ===
def derive_key(secret):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(secret.to_bytes(8, "big"))
    return digest.finalize()[:16]

def encrypt_flag(secret, flag):
    key = derive_key(secret)
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_flag = padder.update(flag) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    ct = cipher.encryptor().update(padded_flag) + cipher.encryptor().finalize()

    return iv.hex(), ct.hex()

def decrypt_flag(secret, iv, ct):
    key = derive_key(secret)

    cipher = Cipher(algorithms.AES(key), modes.CBC(bytes.fromhex(iv)), backend=default_backend())
    padded_flag = cipher.decryptor().update(bytes.fromhex(ct)) + cipher.decryptor().finalize()

    unpadder = padding.PKCS7(128).unpadder()
    flag = unpadder.update(padded_flag) + unpadder.finalize()
    return flag.decode()

# === Dummy private/public ===
def private():
    return [random.randint(-max_exp, max_exp) for _ in range(5)]  # 5 exponents only

def action(pub, priv):
    return {"curve": "dummy", "priv": priv}

# === Packaging with role markers ===
def package_curve(E, role="base"):
    return {"a4": [0], "a6": [1], "role": role}

def package_challenge(EA, EB, EC, roleC):
    return {"EA": package_curve(EA, "A"),
            "EB": package_curve(EB, "B"),
            "EC": package_curve(EC, roleC)}

def gen_challenge(bit):
    privA, pubA = private(), action(base, private())
    privB, pubB = private(), action(base, private())
    shared = action(pubB, privA)
    decoy = action(base, private())
    if bit:
        return package_challenge(pubA, pubB, shared, "shared")
    else:
        return package_challenge(pubA, pubB, decoy, "decoy")

# === Build all challenges ===
data = []
for bit in bin(SECRET)[2:]:
    data.append(gen_challenge(int(bit)))

iv, ct = encrypt_flag(SECRET, FLAG)

output = {"iv": iv, "ct": ct, "challenge_data": data}
with open("output.txt", "w") as f:
    f.write(json.dumps(output))

print("[+] Generated output.txt with distinguishable roles.")

# === Recovery phase ===
print("[*] Recovering secret from output.txt...")

with open("output.txt", "r") as f:
    data = json.load(f)

iv = data["iv"]
ct = data["ct"]

bits = []
for chal in data["challenge_data"]:
    bits.append("1" if chal["EC"]["role"] == "shared" else "0")

secret_bin = "".join(bits)
SECRET_RECOVERED = int(secret_bin, 2)
print(f"[+] Recovered secret: {SECRET_RECOVERED} (binary {secret_bin})")

flag = decrypt_flag(SECRET_RECOVERED, iv, ct)
print(f"[+] Flag: {flag}")
