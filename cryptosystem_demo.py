from modules import AES_CBC, DNAEncoder, ChaosMapper
from cryptosystem import HybridCryptosystem

def format_indices(indices, label="Indices", per_line=20):
    print(f"{label} (total {len(indices)}):")
    for i in range(0, len(indices), per_line):
        line = indices[i:i+per_line]
        print("  ", ", ".join(str(x) for x in line))
    print()

def get_float(prompt, default=None):
    while True:
        value = input(prompt)
        if not value.strip() and default is not None:
            return default
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid floating-point number.")


def demo_encrypt_decrypt():
    print("Cryptosystem Demonstration: Hybrid AES + DNA Encoding + Chaos Mapping")

    # Step 1: User input of plaintext string
    plaintext = input("Enter plaintext to encrypt: ").strip()
    if not plaintext:
        print("No input provided. Exiting.")
        return
    print(f"\n[Step 1] User Input Plaintext:")
    print(f"  {repr(plaintext)}")

    # Step 2: Encrypt plaintext with hybrid system (AES + DNA + chaos mapping)
    print("[Step 2] Encrypting Plaintext using Cryptosystem Model")
    hybrid = HybridCryptosystem()
    encrypted, indices_left, indices_right, r_left, x0_left, r_right, x0_right = hybrid.encrypt(plaintext)
    print(f"\nEncrypted (DNA + Permuted) Ciphertext:\n  {encrypted}\n")
    print(f"Chaos Parameters (Secret Keys):")
    print(f"  Left half - r: {r_left}, x0: {x0_left}")
    print(f"  Right half - r: {r_right}, x0: {x0_right}\n")

    print("Permutation indices applied to DNA (Chaos Mapping):")
    format_indices(indices_left, "Left Indices")
    format_indices(indices_right, "Right Indices")

    # Step 3: Decrypt the Ciphertext with correct chaos parameters
    print("[Step 3] Decrypting Ciphertext with Correct Chaos Parameters")
    decrypted = hybrid.decrypt(encrypted, r_left, x0_left, r_right, x0_right)
    if decrypted is not None:
        print(f"Decrypted Plaintext:\n  {repr(decrypted)}")
    else:
        print("ERROR: Decryption with correct chaos parameters failed.")

    # Step 4: Decrypt with wrong chaos parameters
    demo_wrong = input("Try Decryption with wrong Chaos Parameters? (y/n): ").strip().lower()
    if demo_wrong == 'y':
        wrong_r_left = get_float("  Enter wrong r for left half: ", r_left + 0.01)
        wrong_x0_left = get_float("  Enter wrong x0 for left half: ", x0_left + 0.01)
        wrong_r_right = get_float("  Enter wrong r for right half: ", r_right + 0.01)
        wrong_x0_right = get_float("  Enter wrong x0 for right half: ", x0_right + 0.01)
        try:
            decrypted_wrong = hybrid.decrypt(
                encrypted, wrong_r_left, wrong_x0_left, wrong_r_right, wrong_x0_right
            )
            if decrypted_wrong is None:
                print("Decryption with wrong chaos parameters failed (padding error or gibberish).")
            else:
                print(f"Decrypted with wrong chaos parameters:\n  {repr(decrypted_wrong)}")
        except Exception as e:
            print(f"Decryption error with wrong parameters: {e}")

if __name__ == "__main__":
    demo_encrypt_decrypt()
