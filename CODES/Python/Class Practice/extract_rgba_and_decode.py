# extract_rgba_and_decode.py
from PIL import Image
import sys
import string

IMG = "holiday_card.png"   # change if needed
STEP = 5

def rot_printable(s, shift):
    return ''.join(chr(((ord(c) - 32 - shift) % 95) + 32) for c in s)

def try_decode_from_values(rgba_list):
    # rgba_list is list of (r,g,b,a)
    # Build the observed "mod256" chars you already saw, just for cross-check:
    observed = ''.join(chr((a) % 256) for (_,_,_,a) in rgba_list)
    print("Observed alpha-as-chars (raw):", observed)

    candidates = []

    # For each pixel compute X = R ^ ((G + B) % 3)
    Xs = [(r ^ ((g + b) % 3)) for (r,g,b,a) in rgba_list]
    print("Computed Xs (R ^ ((G+B)%3)):", Xs)

    # Try several algebraic interpretations of the riddle
    # Form variants to compute ord_char:
    # 1) ord = a - X
    # 2) ord = (a - X) % 256
    # 3) ord = a ^ X
    # 4) ord = (a + X) % 256
    # 5) ord = X ^ a  (same as 3)
    # 6) ord = (X - a) % 256
    # 7) ord = (a - X) interpreted with Python signed wrap -> already covered by %256
    variants = []
    a_vals = [a for (_,_,_,a) in rgba_list]
    for variant in ("a_minus_X","a_minus_X_mod256","a_xor_X","a_plus_X_mod256","X_minus_a_mod256"):
        if variant == "a_minus_X":
            ints = [a - X for (a,X) in zip(a_vals, Xs)]
        elif variant == "a_minus_X_mod256":
            ints = [((a - X) % 256) for (a,X) in zip(a_vals, Xs)]
        elif variant == "a_xor_X":
            ints = [(a ^ X) for (a,X) in zip(a_vals, Xs)]
        elif variant == "a_plus_X_mod256":
            ints = [((a + X) % 256) for (a,X) in zip(a_vals, Xs)]
        elif variant == "X_minus_a_mod256":
            ints = [((X - a) % 256) for (a,X) in zip(a_vals, Xs)]
        else:
            ints = []
        # make string if printable
        try:
            s = ''.join(chr(i) for i in ints)
        except Exception:
            s = ''.join(chr(i % 256) for i in ints)
        variants.append((variant, ints, s))

    # Print results
    for name, ints, s in variants:
        printable_ratio = sum(1 for ch in s if ch in string.printable) / (len(s) if s else 1)
        print("\nVariant:", name)
        print("  ints:", ints)
        print("  string:", s)
        print("  printable ratio:", printable_ratio)
        # also try printable rotations (Caesar over printable range)
        if all(32 <= ord(ch) <= 126 for ch in s):
            for shift in range(95):
                r = rot_printable(s, shift)
                if "PFSWT" in r or "PFSWT{" in r or "pfswt" in r or "{" in r:
                    print("   ROT match shift", shift, "->", r)

    # Additional brute attempts combining a simple single-byte XOR with these results
    print("\nTrying single-byte XORs over the derived 's' strings (to catch hidden single-key XOR):")
    for name, ints, s in variants:
        for key in range(256):
            dec = ''.join(chr((ord(c) ^ key) % 256) for c in s)
            if "PFSWT{" in dec or "PFSWT" in dec or "pfswt{" in dec or "{" in dec:
                print("  Found with variant", name, "xor key", key, "->", dec)
                # don't return immediately; show all

    print("\nIf nothing above shows 'PFSWT{', copy the 'ints' lines above (they are the numeric ordinals).")
    print("Paste them here and I will try more algebraic combinations. The crucial data I need are the RGBA tuples or the Xs and alpha values above.")

def gather_diag_pixels(img_path):
    img = Image.open(img_path).convert("RGBA")
    w,h = img.size
    coords = []
    rgba = []
    # main diagonal x==y, start offset 0, step STEP
    limit = min(w,h)
    for i in range(0, limit, STEP):
        coords.append((i,i))
        rgba.append(img.getpixel((i,i)))
    return coords, rgba

if __name__ == "__main__":
    try:
        coords, rgba = gather_diag_pixels(IMG)
    except FileNotFoundError:
        print("ERROR: cannot find", IMG, "— put script in same folder as the PNG or update IMG variable.")
        sys.exit(1)
    print("Image loaded. Coordinates used (main diagonal every 5 pixels):")
    print(coords)
    print("RGBA tuples (one per chosen pixel):")
    for t in rgba:
        print(t)
    try:
        try_decode_from_values(rgba)
    except Exception as e:
        print("Decode helper failed:", e)
