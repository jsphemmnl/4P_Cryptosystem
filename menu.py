import os
import sys
import subprocess

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name])
    if result.returncode != 0:
        print(f"\n[{script_name}] exited with code {result.returncode}.\n")

def main_menu():
    scripts = [
        ("System Demonstration", "cryptosystem_demo.py"),
        ("Entropy Analysis", "entropy.py"),
        ("Encryption and Decryption Speed", "timing.py"),
        ("Brute Force Simulation", "calculations.py"),
        ("Clean Code, AES Comparison", "cryptosystem_clean.py"),
        ("Exit", None)
    ]

    while True:
        print("\nCryptosystem Menu: Hybrid AES + DNA Encoding + Chaos Mapping")
        for i, (desc, _) in enumerate(scripts, 1):
            print(f"{i}. {desc}")
        try:
            choice = int(input("Choose an option (1-{}): ".format(len(scripts))))
            if 1 <= choice <= len(scripts):
                if scripts[choice - 1][1] is None:
                    print("Exiting. Goodbye!")
                    break
                run_script(scripts[choice - 1][1])
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main_menu()