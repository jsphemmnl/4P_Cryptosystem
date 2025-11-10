import math
from cryptosystem import HybridCryptosystem

def shannon_entropy(data):
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    n = len(data)
    entropy = 0
    for count in freq.values():
        p = count / n
        entropy -= p * math.log2(p)
    return entropy

def main():
    print("Cryptosystem Entropy Analysis: Hybrid AES + DNA Encoding + Chaos Mapping\n")
    plaintext = input("Enter plaintext to analyze: ").strip().encode()
    pt_entropy = shannon_entropy(plaintext)
    print(f"\nPlaintext entropy: {pt_entropy:.4f} bits/byte, length: {len(plaintext)} bytes")
    print(f"Total entropy of plaintext: {pt_entropy * len(plaintext):.4f} bits")
    hybrid = HybridCryptosystem()
    merged, *rest = hybrid.encrypt(plaintext.decode())
    split_idx = len(merged) // 2
    from modules import DNAEncoder
    ct_left = DNAEncoder.decode(merged[:split_idx])
    ct_right = DNAEncoder.decode(merged[split_idx:])
    ciphertext_bytes = ct_left + ct_right
    ct_entropy = shannon_entropy(ciphertext_bytes)
    print(f"\nCiphertext entropy: {ct_entropy:.4f} bits/byte, length: {len(ciphertext_bytes)} bytes")
    print(f"Total entropy of ciphertext: {ct_entropy * len(ciphertext_bytes):.4f} bits")
    print(f"Maximum possible entropy (byte): {math.log2(256):.4f} bits/byte")

if __name__ == "__main__":
    main()
