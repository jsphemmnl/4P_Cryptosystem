def get_hybrid_key_bits():
    aes_bits = 256

    chaos_bits_per_param = 30
    num_chaos_params = 4
    chaos_bits = chaos_bits_per_param * num_chaos_params

    total_bits = aes_bits + chaos_bits
    return total_bits

def brute_force_stats(key_bits, num, exp):
    attempts_per_second = num * (10 ** exp)
    total_keys = 2 ** key_bits
    seconds = total_keys / attempts_per_second
    years = seconds / (60 * 60 * 24 * 365.25)
    return total_keys, seconds, years, attempts_per_second

def main():
    print("Cryptosystem Brute Force Simulation: Hybrid AES + DNA Encoding + Chaos Mapping")
    key_bits = get_hybrid_key_bits()
    print(f"Total effective key bits (system): {key_bits}")

    num = float(input("How many brute force attempts per second? (number, e.g., 2.5 for 2.5 x 10^9): "))
    exp = int(input("Exponent of 10 (e.g., 9 for 10^9): "))

    total_keys, seconds, years, rate = brute_force_stats(key_bits, num, exp)

    print("\n--- Brute-force Analysis ---")
    print(f"Keyspace: 2^{key_bits} = {total_keys:.3e} keys")
    print(f"Attacker tries per second: {rate:.3e} attempts/sec")
    print(f"Total time to exhaust keyspace:")
    print(f"  {seconds:.3e} seconds")
    print(f"  {years:.3e} years\n")
    print(f"At this rate, brute-forcing the hybrid keyspace ({key_bits} bits) would take {years:,.0f} years.")

if __name__ == "__main__":
    main()
