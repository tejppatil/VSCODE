from math import isqrt

p = 5926835082066197957903234154181522681863622955227045368107
g = 4678654847136353854775636105256598394616786090947648190523
A = 2045734495688464063300316233392363491690361831090874226130
shared_secret = 3689548518411912030091342114442484140666122346917587506263

# Solve for a: A = g^a mod p

def baby_step_giant_step(g, h, p):
    m = isqrt(p) + 1
    tbl = {}

    # Baby steps
    e = 1
    for i in range(m):
        tbl[e] = i
        e = (e * g) % p

    # Compute g^-m
    g_inv = pow(g, -m, p)

    # Giant steps
    e = h
    for j in range(m):
        if e in tbl:
            return j * m + tbl[e]
        e = (e * g_inv) % p
    return None

a = baby_step_giant_step(g, A, p)
print(f"a = {a}")
print(f"FLAG{{{str(a)[-9:]}}}")
