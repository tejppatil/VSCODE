def caesar_encrypt(text, key):
    encrypted = ''
    for ch in text:
        if ch.islower():
            encrypted += chr((ord(ch) - ord('a') + key) % 26 + ord('a'))
        elif ch.isupper():
            encrypted += chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
        else:
            encrypted += ch
    return encrypted

def caesar_decrypt(text, key):
    decrypted = ''
    for ch in text:
        if ch.islower():
            decrypted += chr((ord(ch) - ord('a') - key) % 26 + ord('a'))
        elif ch.isupper():
            decrypted += chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
        else:
            decrypted += ch
    return decrypted

while(True):
    choice = int(input("\n1)Press 1 to Encrypt.\n2)Press 2 to decrypt.\nPress 3 to exit.\nEnter your choice here:- "))
    if choice == 1:
        text = input("\nEnter the text for encryption:")
        key = int(input("Enter the secret key:"))
        print("Encrypted Message:", caesar_encrypt(text, key))
    
    elif choice == 2:
        text = input("\nEnter the text for decryption:")
        key = int(input("Enter the secret key:"))
        print("Decrypted Message:", caesar_decrypt(text, key))
    
    elif choice == 3:
        print("Program exited successfully>>>>>>\n")
        break
    else:
        print(">>>Wrong input,Please enter correctly<<<")