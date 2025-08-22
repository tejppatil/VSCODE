import hashlib

hash_to_find = "faad49866e9498fc1719f5289e7a0269"

candidates = [
    "flag{}",
    "flag{}",
    "flag{1234}",
    "flag{secret}",
    "flag{password}",
    # add more guesses here
]

for candidate in candidates:
    h = hashlib.md5(candidate.encode()).hexdigest()
    if h == hash_to_find:
        print(f"Found! {candidate} hashes to {hash_to_find}")
        break
else:
    print("No matches found in candidate list")
