def mod_exp(base, exponent, modulus):
    return pow(base, exponent, modulus)

def is_primitive_root(g, p):
    required_set = set(num for num in range(1, p))
    actual_set = set(pow(g, powers, p) for powers in range(1, p))
    return required_set == actual_set

def main():
    print("=== Diffie-Hellman Key Exchange ===")

    try:
        p = int(input("Enter a large prime number (p): "))
        if p < 2:
            raise ValueError("Prime number must be greater than 1.")

        g = int(input(f"Enter a base number (generator) less than {p}: "))
        if g <= 1 or g >= p:
            raise ValueError(f"Base number must be > 1 and < {p}.")
        if not is_primitive_root(g, p):
            raise ValueError(f"{g} is not a valid generator (primitive root) for {p}.")

        tejas_private = int(input("Enter Tejas's private key (number < p): "))
        patil_private = int(input("Enter Patil's private key (number < p): "))
        if not (0 < tejas_private < p and 0 < patil_private < p):
            raise ValueError(f"Private keys must be between 1 and {p - 1}.")

        tejas_public = mod_exp(g, tejas_private, p)
        patil_public = mod_exp(g, patil_private, p)

        tejas_shared_key = mod_exp(patil_public, tejas_private, p)
        patil_shared_key = mod_exp(tejas_public, patil_private, p)

        print("\n--- Results ---")
        print("Tejas's Public Key:", tejas_public)
        print("Patil's Public Key:", patil_public)
        print("Tejas's Shared Key:", tejas_shared_key)
        print("Patil's Shared Key:", patil_shared_key)

        if tejas_shared_key == patil_shared_key:
            print("\nShared key successfully established!")
        else:
            print("\nError: Shared keys do not match.")

    except ValueError as ve:
        print(f"\nInput Error: {ve}")

if __name__ == "__main__":
    main()
