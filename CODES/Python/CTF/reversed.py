cipher_text = "33,@;&:-f517:/f7"

plaintext = ""

for i in range(0, len(cipher_text), 2):
    ch1 = cipher_text[i]
    ch2 = cipher_text[i+1]
    
    random_ch = ord(ch1)
    tmp_char2 = ord(ch2)
    
    ch_ascii = tmp_char2 - 32 + random_ch
    plaintext += chr(ch_ascii)

print("Decrypted message:", plaintext)
