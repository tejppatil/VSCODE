import hashlib
import itertools
import string

target_hash = "faad49866e9498fc1719f5289e7a0269"

def md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

chars = string.ascii_letters + string.digits

for length in range(1, 10): 
    for candidate in itertools.product(chars, repeat=length):
        inner = ''.join(candidate)
        flag = f"FLAG{{{inner}}}"
        if md5_hash(flag) == target_hash:
            print("Found flag:", flag)
            break
