from Crypto.Util.number import long_to_bytes, inverse

def integer_cbrt(x):
    # integer cube root by binary search
    low, high = 0, 1 << (x.bit_length() // 3 + 1)
    while low < high:
        mid = (low + high) // 2
        mid_cubed = mid ** 3
        if mid_cubed == x:
            return mid
        elif mid_cubed < x:
            low = mid + 1
        else:
            high = mid
    return low - 1

n = ...  # your large n
e = 65537
c = ...  # your ciphertext

# Approximate d = p^3 + p^2 + p ≈ p^3
approx_d = integer_cbrt(n)

# Now solve p^3 + p^2 + p = approx_d using integer trial around approx_d^(1/3)
# We'll try p values near integer_cbrt(approx_d)

for p_candidate in range(approx_d - 1000000, approx_d + 1000000):
    val = p_candidate**3 + p_candidate**2 + p_candidate
    if n % val == 0:
        p = p_candidate
        q = 1 + p + p**2
        r = n // (p * q)
        break
else:
    raise Exception("Failed to factor n")

phi = (p - 1)*(q - 1)*(r - 1)

d = inverse(e, phi)

m = pow(c, d, n)
print("Flag:", long_to_bytes(m))
