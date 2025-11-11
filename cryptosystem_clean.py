import time
import math
import string
import random
import pytest
from modules import AES_CBC, DNAEncoder
from cryptosystem import HybridCryptosystem


def generate_random_plaintext(length, charset_choice=3):
    if charset_choice == 1:
        charset = string.ascii_letters
    elif charset_choice == 2:
        charset = string.ascii_letters + string.digits
    else:
        charset = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(charset) for _ in range(length))


def shannon_entropy(data):
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    entropy = 0.0
    n = len(data)
    for count in freq.values():
        p = count / n
        entropy -= p * math.log2(p)
    return entropy


def benchmark_aes_only(plaintext, iters=100):
    aes = AES_CBC()
    pt_bytes = plaintext.encode()
    start = time.time()
    ct = None
    for _ in range(iters):
        ct = aes.encrypt(pt_bytes)
    end = time.time()
    enc_time = (end - start)/iters
    start = time.time()
    for _ in range(iters):
        pt_out = aes.decrypt(ct)
    end = time.time()
    dec_time = (end - start)/iters
    pt_entropy_per_byte = shannon_entropy(pt_bytes)
    ct_entropy_per_byte = shannon_entropy(ct)
    pt_len = len(pt_bytes)
    ct_len = len(ct)
    total_pt_entropy = pt_entropy_per_byte * pt_len
    total_ct_entropy = ct_entropy_per_byte * ct_len
    throughput = pt_len / enc_time if enc_time > 1e-7 else 0
    return enc_time, dec_time, pt_entropy_per_byte, ct_entropy_per_byte, total_pt_entropy, total_ct_entropy, throughput, pt_len, ct_len


def benchmark_hybrid(plaintext, iters=100):
    hybrid = HybridCryptosystem()
    start = time.time()
    encrypted = None
    r_l, x0_l, r_r, x0_r = None, None, None, None
    for _ in range(iters):
        encrypted, _, _, r_l, x0_l, r_r, x0_r = hybrid.encrypt(plaintext)
    end = time.time()
    enc_time = (end - start)/iters
    start = time.time()
    for _ in range(iters):
        pt_out = hybrid.decrypt(encrypted, r_l, x0_l, r_r, x0_r)
    end = time.time()
    dec_time = (end - start)/iters
    split_index = len(encrypted)//2
    ct_left = DNAEncoder.decode(encrypted[:split_index])
    ct_right = DNAEncoder.decode(encrypted[split_index:])
    ct_bytes = ct_left + ct_right
    pt_bytes = plaintext.encode()
    pt_entropy_per_byte = shannon_entropy(pt_bytes)
    ct_entropy_per_byte = shannon_entropy(ct_bytes)
    pt_len = len(pt_bytes)
    ct_len = len(ct_bytes)
    total_pt_entropy = pt_entropy_per_byte * pt_len
    total_ct_entropy = ct_entropy_per_byte * ct_len
    throughput = pt_len / enc_time if enc_time > 1e-7 else 0
    return enc_time, dec_time, pt_entropy_per_byte, ct_entropy_per_byte, total_pt_entropy, total_ct_entropy, throughput, pt_len, ct_len


@pytest.mark.parametrize("length", [100, 300, 500, 700, 1000])
def test_compare_throughput_entropy(length):
    # Use full charset always for pytest tests for uniformity
    iterations = 100
    plaintext = generate_random_plaintext(length, 3)
    aes = benchmark_aes_only(plaintext, iterations)
    hybrid = benchmark_hybrid(plaintext, iterations)

    print(f"\nLength={length}")
    print(f"AES Plaintext Entropy (per byte): {aes[2]:.4f}")
    print(f"AES Ciphertext Entropy (per byte): {aes[3]:.4f}")
    print(f"AES Total Plaintext Entropy: {aes[4]:.2f}")
    print(f"AES Total Ciphertext Entropy: {aes[5]:.2f}")
    print(f"AES Throughput (bytes/sec): {aes[6]:.2f}")
    print(f"Hybrid Plaintext Entropy (per byte): {hybrid[2]:.4f}")
    print(f"Hybrid Ciphertext Entropy (per byte): {hybrid[3]:.4f}")
    print(f"Hybrid Total Plaintext Entropy: {hybrid[4]:.2f}")
    print(f"Hybrid Total Ciphertext Entropy: {hybrid[5]:.2f}")
    print(f"Hybrid Throughput (bytes/sec): {hybrid[6]:.2f}")

    if aes[6] <= 0 or hybrid[6] <= 0:
        print(f"WARNING: Throughput measured zero for length={length}; consider increasing iterations.")


if __name__ == "__main__":
    print("AES Comparison: Manual Run with User Input")
    try:
        length = int(input("Enter plaintext length (integer): "))
        if length <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Using default length = 300.")
        length = 300

    print("Choose plaintext content type:")
    print("1 - Letters only")
    print("2 - Letters and numbers")
    print("3 - Letters, numbers, and symbols")
    try:
        charset_choice = int(input("Enter option (1-3): "))
        if charset_choice not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("Invalid input. Using full charset (letters, numbers, symbols).")
        charset_choice = 3

    plaintext = generate_random_plaintext(length, charset_choice)
    iterations = 100

    aes = benchmark_aes_only(plaintext, iterations)
    hybrid = benchmark_hybrid(plaintext, iterations)

    print(f"\nLength={length}")
    print(f"Plaintext content type: {['letters', 'letters+numbers', 'letters+numbers+symbols'][charset_choice-1]}")
    print(f"AES Plaintext Entropy (per byte): {aes[2]:.4f}")
    print(f"AES Ciphertext Entropy (per byte): {aes[3]:.4f}")
    print(f"AES Total Plaintext Entropy: {aes[4]:.2f}")
    print(f"AES Total Ciphertext Entropy: {aes[5]:.2f}")
    print(f"AES Throughput (bytes/sec): {aes[6]:.2f}")
    print(f"Hybrid Plaintext Entropy (per byte): {hybrid[2]:.4f}")
    print(f"Hybrid Ciphertext Entropy (per byte): {hybrid[3]:.4f}")
    print(f"Hybrid Total Plaintext Entropy: {hybrid[4]:.2f}")
    print(f"Hybrid Total Ciphertext Entropy: {hybrid[5]:.2f}")
    print(f"Hybrid Throughput (bytes/sec): {hybrid[6]:.2f}")