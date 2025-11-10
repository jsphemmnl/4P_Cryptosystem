import time
from cryptosystem import HybridCryptosystem

def main():
    print("Cryptosystem Time Calculation: Hybrid AES + DNA Encoding + Chaos Mapping\n")
    sample_text = input("Enter plaintext: ").strip()
    iterations = input("Number of iterations [default=10]: ").strip()
    try:
        iterations = int(iterations)
    except ValueError:
        iterations = 10
    hybrid = HybridCryptosystem()
    # Time encryption
    start_enc = time.time()
    for _ in range(iterations):
        encrypted, _, _, r_left, x0_left, r_right, x0_right = hybrid.encrypt(sample_text)
    end_enc = time.time()
    avg_enc = (end_enc - start_enc) / iterations
    # Time decryption
    decrypt_success = 0
    start_dec = time.time()
    for _ in range(iterations):
        result = hybrid.decrypt(encrypted, r_left, x0_left, r_right, x0_right)
        if result is not None:
            decrypt_success += 1
    end_dec = time.time()
    avg_dec = (end_dec - start_dec) / decrypt_success if decrypt_success > 0 else float('inf')
    print(f"Average encryption time over {iterations} runs: {avg_enc:.6f} seconds")
    print(f"Average decryption time over {decrypt_success} successful runs: {avg_dec:.6f} seconds")
    if decrypt_success < iterations:
        print(f"Warning: {iterations - decrypt_success} decryptions failed.")

if __name__ == "__main__":
    main()
