from Crypto.Cipher import DES

ciphertext = bytes.fromhex("d09b5a45758770ca4d81af32c6701fff5a540bb76451ea9d")

weak_keys = [
    bytes.fromhex("0101010101010101"),
    bytes.fromhex("FEFEFEFEFEFEFEFE"),
    bytes.fromhex("E0E0E0E0F1F1F1F1"),
    bytes.fromhex("1F1F1F1F0E0E0E0E"),
    bytes.fromhex("01FE01FE01FE01FE"),
    bytes.fromhex("FE01FE01FE01FE01"),
    bytes.fromhex("1FE01FE00EF10EF1"),
    bytes.fromhex("E01FE01FF10EF10E"),
    bytes.fromhex("01E001E001F101F1"),
    bytes.fromhex("E001E001F101F101"),
    bytes.fromhex("1FFE1FFE0EFE0EFE"),
    bytes.fromhex("FE1FFE1FFE0EFE0E"),
]

for key in weak_keys:
    cipher = DES.new(key, DES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    try:
        print(f"Key: {key.hex()}")
        print("Plaintext:", plaintext)
        if all(32 <= b < 127 for b in plaintext):
            print("Possible plaintext:", plaintext.decode())
    except:
        pass
