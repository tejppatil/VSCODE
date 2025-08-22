#!/usr/bin/env python3
"""
Windows-friendly Merkle-Hellman solver for the CTF instance.

Usage:
    1. Put this file in the same folder as your "output (12).txt".
    2. Ensure you don't have a local `random.py` (see checks below).
    3. Install dependencies:
         pip install sympy pycryptodome
       (sympy provides LLL; it's pure Python and simpler to install on Win.)
    4. Run:
         python knapsack_solve_vs.py
"""

import os
import sys
import re
from math import log2
from binascii import unhexlify

# --- safety/net checks (common Windows issues) ---
# Detect accidental shadowing of Python stdlib modules (like random)
for name in ("random",):
    if os.path.exists(os.path.join(os.getcwd(), name + ".py")):
        print(f"ERROR: Please rename or remove '{name}.py' in this directory. "
              f"It will shadow the standard library module '{name}'.")
        sys.exit(1)

# Try fpylll first (fast), then fall back to sympy
USE_FPYLLL = False
try:
    from fpylll import IntegerMatrix, LLL as fpylll_LLL
    USE_FPYLLL = True
    print("Using fpylll for LLL (fast).")
except Exception:
    try:
        from sympy import Matrix
        print("fpylll not available; using sympy.Matrix.LLL (slower but Windows-friendly).")
    except Exception as e:
        print("ERROR: Need either fpylll or sympy. Install sympy with:\n  pip install sympy")
        print("Exception:", e)
        sys.exit(1)

# ---------------- parsing ----------------
OUTFILE = "output (12).txt"

if not os.path.exists(OUTFILE):
    print(f"ERROR: Could not find '{OUTFILE}' in current folder: {os.getcwd()}")
    sys.exit(1)

txt = open(OUTFILE, "r", encoding="utf-8", errors="ignore").read()

# Try to extract: Public key: [ ... ] and Encrypted Flag: <number> (or Encrypted: <number>)
pk_match = re.search(r"Public key\s*:\s*\[([^\]]+)\]", txt, re.IGNORECASE | re.DOTALL)
ct_match = re.search(r"Encrypted(?: Flag)?:\s*([0-9]+)", txt, re.IGNORECASE)

if not pk_match:
    print("Couldn't parse public key from output file. Make sure the public key is printed as:\nPublic key: [1234, 5678, ...]\n")
    # For debugging: print a small slice to help user check
    print("File preview (first 800 chars):\n" + txt[:800])
    sys.exit(1)

pk_raw = pk_match.group(1)
# Split on commas but allow whitespace/newlines
a_list = [int(x.strip()) for x in re.split(r",\s*", pk_raw.strip()) if x.strip()]

if not ct_match:
    print("Couldn't parse ciphertext (Encrypted Flag) from output file.")
    # still continue if you want; but we'll exit
    sys.exit(1)
c_val = int(ct_match.group(1))

n = len(a_list)
print(f"Parsed public key length n = {n}")
print(f"Parsed ciphertext (decimal) with {c_val.bit_length()} bits")

# ---------------- lattice build & LLL ----------------
def run_fpylll(a, c, M_shift=16, delta=0.99):
    n = len(a)
    M = 1 << (int(log2(n)) + M_shift)
    B = IntegerMatrix(n + 1, n + 1)
    for i in range(n):
        B[i, i] = M
        B[i, n] = a[i]
    B[n, n] = c
    fpylll_LLL.reduction(B, delta=delta)
    # Return rows of reduced basis as Python lists
    rows = [[int(B[i, j]) for j in range(n+1)] for i in range(n+1)]
    return rows, M

def run_sympy(a, c, M_shift=16):
    M = 1 << (int(log2(len(a))) + M_shift)
    rows = []
    for i in range(len(a)):
        row = [0] * (len(a) + 1)
        row[i] = M
        row[-1] = a[i]
        rows.append(row)
    rows.append([0] * len(a) + [c])
    # sympy Matrix
    from sympy import Matrix
    B = Matrix(rows)
    B_red = B.LLL()  # returns reduced basis as Matrix
    return [list(map(int, r)) for r in B_red.tolist()], M

def try_extract_bits_from_basis(basis_rows, a, M):
    n = len(a)
    candidates = []
    t = M // 2
    for vec in basis_rows:
        last = abs(vec[-1])
        # require small last coordinate (heuristic)
        if last > max(1, M // 8):
            continue
        raw = vec[:-1]
        # decide mapping: positive big ~ +M -> 1, near 0 -> 0
        bits = [1 if (abs(x) > t and x > 0) else 0 for x in raw]
        # flip if many negatives
        neg_count = sum(1 for x in raw if x < 0 and abs(x) > t)
        if neg_count > n // 2:
            bits = [1 - b for b in bits]
        # verify
        if sum(ai * bi for ai, bi in zip(a, bits)) == c_val:
            candidates.append(bits)
    return candidates

def bits_to_bytes_lsb_first(bits):
    # bits[0] is global LSB per source description
    out_bytes = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        val = sum((bit & 1) << j for j, bit in enumerate(chunk))
        out_bytes.append(val)
    # reverse byte order (LSB-first across full integer)
    out_bytes = out_bytes[::-1]
    return bytes(out_bytes)

# Try run
based_candidates = []
M_used = None
for Mshift in (14, 16, 18):  # try a few shifts if default doesn't work
    try:
        if USE_FPYLLL:
            basis, M_used = run_fpylll(a_list, c_val, M_shift=Mshift, delta=0.99)
        else:
            basis, M_used = run_sympy(a_list, c_val, M_shift=Mshift)
    except Exception as e:
        print("LLL run failed for M_shift", Mshift, ":", e)
        continue
    print(f"LLL finished (M_shift={Mshift}, M ~ 2^{int(log2(len(a_list))) + Mshift})")
    cand = try_extract_bits_from_basis(basis, a_list, M_used)
    if cand:
        based_candidates = cand
        break

if not based_candidates:
    print("No valid candidate found from initial LLL pass.")
    print("You can try increasing M_shift values or running with fpylll in WSL for greater reliability.")
    # Optionally save reduced basis to file for offline inspection
    try:
        with open("reduced_basis_debug.txt", "w") as f:
            for r in basis[:min(40, len(basis))]:
                f.write(" ".join(map(str, r)) + "\n")
        print("Wrote partial reduced basis to reduced_basis_debug.txt for inspection.")
    except Exception:
        pass
    sys.exit(1)

# If we have candidates, decode them
for idx, bits in enumerate(based_candidates):
    pt_bytes = bits_to_bytes_lsb_first(bits)
    print(f"\n--- Candidate #{idx+1} ---")
    try:
        text = pt_bytes.decode("utf-8")
        print("Decoded UTF-8 plaintext:\n", text)
    except Exception:
        print("Raw bytes (hex):", pt_bytes.hex())
    # Save candidate
    with open(f"candidate_{idx+1}.bin", "wb") as f:
        f.write(pt_bytes)
    print(f"Saved candidate_{idx+1}.bin")
