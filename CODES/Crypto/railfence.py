def encryptRailFence(text, key):
    text = text.replace(" ", "")  # Remove spaces
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    
    dir_down = False
    row, col = 0, 0
    
    for i in range(len(text)):
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
        
        rail[row][col] = text[i]
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
            
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)
    
#def decryptRailFence(cipher, key):
    cipher = cipher.replace(" ", "")  
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    
    dir_down = None
    row, col = 0, 0
    
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
            
        rail[row][col] = '*'
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
            
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
    
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
            
        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1
            
        if dir_down:
            row += 1
        else:
            row -= 1
    return "".join(result)

if __name__ == "__main__":
   # choice = input("Please enter 'E' for encryption or 'D' for decryption: ").strip().lower()
    
    #if choice == "e":
    text = input("Enter the text to encrypt: ").replace(" ", "")  
    key = int(input("Enter the key (number of rails): "))
    encrypted_text = encryptRailFence(text, key)
    print("Encrypted Text:", encrypted_text)

   # elif choice == "d":
    #    cipher = input("Enter the text to decrypt: ").replace(" ", "") 
    #    key = int(input("Enter the key (number of rails): "))
    #    decrypted_text = decryptRailFence(cipher, key)
    #    print("Decrypted Text:", decrypted_text)

    #else:
    #    print("Invalid choice! Please enter 'E' for encryption or 'D' for decryption.")
