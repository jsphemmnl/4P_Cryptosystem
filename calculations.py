def get_hybrid_key_bits(aes_bits=256, chaos_bits_per_param=30, num_chaos_params=4):
    # AES part + chaos parameters
    chaos_bits = chaos_bits_per_param * num_chaos_params
    total_bits = aes_bits + chaos_bits
    return total_bits

def brute_force_stats(key_bits, attempts_per_second):
    total_keys = 2 ** key_bits
    seconds = total_keys / attempts_per_second
    years = seconds / (60 * 60 * 24 * 365)
    return total_keys, seconds, years

def format_time(seconds):
    # For more human-friendly reporting
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365
    if years > 1e6:
        return f"{years:.2e} years"
    elif years > 1:
        return f"{years:,.2f} years"
    elif days > 1:
        return f"{days:,.2f} days"
    elif hours > 1:
        return f"{hours:,.2f} hours"
    elif minutes > 1:
        return f"{minutes:,.2f} minutes"
    else:
        return f"{seconds:,.2f} seconds"

def main():
    print("Brute-force Attack Simulation Comparison")
    print("Key lengths: 8, 16, 32, 64, 128, 256, Hybrid (AES-256+chaos)")
    # User input
    rate = float(input("How many brute force attempts per second? (e.g., 1e9 means 1 billion/sec): "))
    
    key_lengths = [8, 16, 32, 64, 128, 256]
    print("\n| Key bits | Cipher | Keyspace | Time to Exhaust Keyspace |")
    print("|----------|--------|-----------|--------------------------|")
    for bits in key_lengths:
        total_keys, seconds, years = brute_force_stats(bits, rate)
        print(f"| {bits:<8} | Symm   | {total_keys:.2e} | {format_time(seconds):>24} |")
    
    # AES-256
    aes256_bits = 256
    total_keys, seconds, years = brute_force_stats(aes256_bits, rate)
    print(f"| {aes256_bits:<8} | AES256 | {total_keys:.2e} | {format_time(seconds):>24} |")
    
    # Hybrid
    hybrid_bits = get_hybrid_key_bits()
    total_keys, seconds, years = brute_force_stats(hybrid_bits, rate)
    print(f"| {hybrid_bits:<8} | Hybrid | {total_keys:.2e} | {format_time(seconds):>24} |")

    print("\n*Hybrid effective key bits includes AES-256 key plus 4x30-bit chaos parameters.")

if __name__ == "__main__":
    main()