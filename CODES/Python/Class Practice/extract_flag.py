from PIL import Image
import numpy as np
import string

# ---------- CONFIG ----------
IMG_PATH = "holiday_card.png"   # change path if needed
STEP = 5                        # "every fifth step aligns"
PRINTABLE = set(bytes(string.printable, "ascii")).union(set(range(32,127)))
# ----------------------------

def ord_candidates_from_pixels(pixels):
    """Given a list of (R,G,B,A) tuples, compute ord candidates using:
       ord = alpha - (R XOR ((G+B) % 3))
       Try both plain subtraction and subtraction modulo 256.
    """
    plain_chars = []
    mod256_chars = []
    raw_vals_plain = []
    raw_vals_mod = []

    for (r,g,b,a) in pixels:
        X = r ^ ((g + b) % 3)
        val_plain = a - X
        val_mod = (a - X) % 256
        raw_vals_plain.append(val_plain)
        raw_vals_mod.append(val_mod)

        plain_chars.append(chr(val_plain) if 0 <= val_plain < 256 else '?')
        mod256_chars.append(chr(val_mod) if 0 <= val_mod < 256 else '?')

    return raw_vals_plain, raw_vals_mod, ''.join(plain_chars), ''.join(mod256_chars)

def is_mostly_printable(s, threshold=0.8):
    if not s:
        return False
    printable = sum(1 for ch in s if ch in string.printable)
    return printable / len(s) >= threshold

def gather_pixels(img, mode, start_offset=0):
    """Return list of RGBA tuples following a path.
       mode: 'diag' (x==y), 'anti' (x==w-1-y), 'row' (center row), 'col' (center col)
       start_offset: 0..(STEP-1) to try different 5-step alignments
    """
    w,h = img.size
    pix = img.load()
    coords = []
    pixels = []

    if mode == 'diag':
        limit = min(w,h)
        for i in range(start_offset, limit, STEP):
            coords.append((i,i))
    elif mode == 'anti':
        limit = min(w,h)
        for i in range(start_offset, limit, STEP):
            coords.append((i, (h-1)-i))
    elif mode == 'row':
        y = h // 2
        for x in range(start_offset, w, STEP):
            coords.append((x,y))
    elif mode == 'col':
        x = w // 2
        for y in range(start_offset, h, STEP):
            coords.append((x,y))
    else:
        raise ValueError("unknown mode")

    for (x,y) in coords:
        r,g,b,a = pix[x,y]
        pixels.append((r,g,b,a))
    return coords, pixels

def try_all_paths(img):
    modes = ['diag','anti','row','col']
    results = []
    for mode in modes:
        for offset in range(STEP):
            coords, pixels = gather_pixels(img, mode, start_offset=offset)
            raw_plain, raw_mod, s_plain, s_mod = ord_candidates_from_pixels(pixels)

            # Build printable-filtered strings
            filtered_plain = ''.join(ch if ch in string.printable else '.' for ch in s_plain)
            filtered_mod = ''.join(ch if ch in string.printable else '.' for ch in s_mod)

            results.append({
                'mode': mode,
                'offset': offset,
                'coords': coords,
                'raw_plain': raw_plain,
                'raw_mod': raw_mod,
                's_plain': s_plain,
                's_mod': s_mod,
                'filtered_plain': filtered_plain,
                'filtered_mod': filtered_mod,
                'most_printable_plain': is_mostly_printable(s_plain),
                'most_printable_mod': is_mostly_printable(s_mod),
            })
    return results

def print_findings(results):
    for r in results:
        if r['most_printable_plain'] or r['most_printable_mod']:
            print("=== Candidate path: mode=%s offset=%d ===" % (r['mode'], r['offset']))
            print("Coords count:", len(r['coords']))
            print("Plain chars (raw):\n", r['filtered_plain'])
            print("Mod256 chars (raw):\n", r['filtered_mod'])
            # Look for "flag" or "{"
            if "flag" in r['filtered_plain'].lower() or "{" in r['filtered_plain']:
                print("--> 'flag' or '{' found in plain!")
            if "flag" in r['filtered_mod'].lower() or "{" in r['filtered_mod']:
                print("--> 'flag' or '{' found in mod!")

def main():
    img = Image.open(IMG_PATH).convert("RGBA")
    print("Image size:", img.size, "mode: RGBA")
    results = try_all_paths(img)

    # Print top candidates
    print_findings(results)

    # If nothing obviously printable, print a summary of a few promising paths
    print("\nSummary of all paths (showing first 60 chars of each):\n")
    for r in results:
        fp = r['filtered_plain'][:60]
        fm = r['filtered_mod'][:60]
        score_plain = sum(1 for c in r['s_plain'] if c in string.printable)
        score_mod = sum(1 for c in r['s_mod'] if c in string.printable)
        print(f"mode={r['mode']} off={r['offset']} printable_plain={score_plain} printable_mod={score_mod}")
        print("  plain:", fp)
        print("  mod:  ", fm)
    print("\nIf you see a line containing 'flag' or 'THM' or braces {{}} above, that's likely the flag. If not, paste the most promising 'plain' or 'mod' string here and I will help decode further.")

if __name__ == "__main__":
    main()
