import base64
import string
from itertools import product, cycle

b64_str = "DQkYDD4XDhNqGRoLeBUcChEk"

missing_padding = len(b64_str) % 4
if missing_padding:
    b64_str += '=' * (4 - missing_padding)

ciphertext = base64.b64decode(b64_str)

def xor_decrypt(data, key):
    return bytes([b ^ k for b, k in zip(data, cycle(key))])

possible_keys = string.printable.encode()

for key_length in range(1, 5):
    for key_tuple in product(possible_keys, repeat=key_length):
        key = bytes(key_tuple)
        decrypted = xor_decrypt(ciphertext, key)
        try:
            text = decrypted.decode('utf-8')
            if "flag" in text.lower():
                print(f"Key: {key} => {text}")
        except UnicodeDecodeError:
            continue
