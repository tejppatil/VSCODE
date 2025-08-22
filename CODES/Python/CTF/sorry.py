def caesar_decrypt(text, shift):
    decrypted = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            decrypted.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            decrypted.append(char)
    return ''.join(decrypted)
def atbash(s):
    res = ''
    for ch in s:
        if 'A' <= ch <= 'Z':
            res += chr(ord('Z') - (ord(ch) - ord('A')))
        elif 'a' <= ch <= 'z':
            res += chr(ord('z') - (ord(ch) - ord('a')))
        else:
            res += ch
    return res

cipher = ("NB XLMWLOVMXVH ULI BLFI KZRM TEQAGDSJPCYVVVGGGGZZZZGVRRRHHSSISMRLZGVHWWISMRLZGVH"
          "OOXWISMRLZGVHOFFNDDNXWISMRLZGVHOFUUDNXWISMRLZGVHOFTTYKPYBUDNXWISMRLZGVHOFTKECQPYBUDNX"
          "WISMRLZGVHOFTKEJCQPYBUDNXWISMRLZGVHOFTKE")

plaintext = atbash(cipher)

# Extract the first sentence which looks meaningful
first_sentence = plaintext.split('GVJZTW')[0].strip()

# Replace spaces with underscores and uppercase to lowercase for flag formatting
flag_text = first_sentence.replace(' ', '_').lower()

# Construct the flag
flag = f"FLAG{{{flag_text}}}"

print(flag)

# Your ciphertext:
ciphertext = "XLMWLOVMXVH ULI BLFI KZRM TEQAGDSJPCYVVVGGGGZZZZGVRRRHHSSISMRLZGVHWWISMRLZGVHOOXWISMRLZGVHOFFNDDNXWISMRLZGVHOFUUDNXWISMRLZGVHOFTTYKPYBUDNXWISMRLZGVHOFTKECQPYBUDNXWISMRLZGVHOFTKEJCQPYBUDNXWISMRLZGVHOFTKE"

# Step 1: Caesar shift by 4
shifted_text = caesar_decrypt(ciphertext, 4)
print("Caesar Shift -4 result:\n", shifted_text)

# It starts with "THIS IS ..." so split from there
start = shifted_text.find("THIS IS")
print("\nAfter 'THIS IS':")
rest = shifted_text[start+7:].strip()  # after 'THIS IS'

print(rest)

# Step 3: Vigenère decrypt function
def vigenere_decrypt(cipher, key):
    decrypted = []
    key_length = len(key)
    key_int = [ord(i.upper()) - ord('A') for i in key]
    for i, char in enumerate(cipher):
        if char.isalpha():
            offset = ord('A')
            decrypted_char = chr((ord(char) - offset - key_int[i % key_length]) % 26 + offset)
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    return ''.join(decrypted)

# Let's try the key "PROTECTION" (since "FOR YOUR OWN PROTECTION" seems likely)
key = "PROTECTION"

# The suspicious part appears multiple times, let's extract only letters for Vigenère
import re
letters_only = re.sub(r'[^A-Z]', '', rest.upper())

print("\nLetters only part:\n", letters_only)

decrypted_vigenere = vigenere_decrypt(letters_only, key)
print("\nVigenère Decrypted with key 'PROTECTION':\n", decrypted_vigenere)
