
from modules import AES_CBC, DNAEncoder, ChaosMapper

CHAOS_R_MIN = 3.57
CHAOS_R_MAX = 4.0
CHAOS_X0_MIN = 0.0
CHAOS_X0_MAX = 1.0

DNA_SYMBOLS = ('A', 'T', 'C', 'G')

def validate_chaos_param(label, value, min_val, max_val):
    if not (min_val <= value <= max_val):
        raise ValueError(f"{label}={value} out of bounds [{min_val}, {max_val}]")

def validate_dna_seq(seq):
    for c in seq:
        if c not in DNA_SYMBOLS:
            raise ValueError(f"Invalid DNA symbol: {c}")

def handle_exception(action, exception):
    print(f"[cryptosystem.py] {action} error: {exception}")

class HybridCryptosystem:
    def __init__(self):
        self.aes_left = AES_CBC()
        self.aes_right = AES_CBC()

    def split(self, plaintext):
        if not isinstance(plaintext, str):
            raise TypeError("Plaintext must be a string")
        split_idx = len(plaintext) // 2
        return plaintext[:split_idx], plaintext[split_idx:]

    def merge(self, left, right):
        if not (isinstance(left, str) and isinstance(right, str)):
            raise TypeError("Merge inputs must be strings")
        return left + right

    def encrypt(self, plaintext, chaos_override=None):
        try:
            left, right = self.split(plaintext)
            ct_left = self.aes_left.encrypt(left.encode())
            ct_right = self.aes_right.encrypt(right.encode())
            # DNA encoding
            dna_left = DNAEncoder.encode(ct_left)
            dna_right = DNAEncoder.encode(ct_right)
            validate_dna_seq(dna_left)
            validate_dna_seq(dna_right)
            # Chaos permutation
            if chaos_override:
                r_l, x0_l, r_r, x0_r = chaos_override
                validate_chaos_param('r_left', r_l, CHAOS_R_MIN, CHAOS_R_MAX)
                validate_chaos_param('x0_left', x0_l, CHAOS_X0_MIN, CHAOS_X0_MAX)
                validate_chaos_param('r_right', r_r, CHAOS_R_MIN, CHAOS_R_MAX)
                validate_chaos_param('x0_right', x0_r, CHAOS_X0_MIN, CHAOS_X0_MAX)
                mapper_left = ChaosMapper(r=r_l, x0=x0_l, length=len(dna_left))
                mapper_right = ChaosMapper(r=r_r, x0=x0_r, length=len(dna_right))
            else:
                mapper_left = ChaosMapper(length=len(dna_left))
                mapper_right = ChaosMapper(length=len(dna_right))
            indices_left = mapper_left.get_indices()
            indices_right = mapper_right.get_indices()
            permuted_left = ChaosMapper.permute(dna_left, indices_left)
            permuted_right = ChaosMapper.permute(dna_right, indices_right)
            merged = self.merge(permuted_left, permuted_right)
            return merged, indices_left, indices_right, mapper_left.r, mapper_left.x0, mapper_right.r, mapper_right.x0
        except Exception as e:
            handle_exception("Encryption", e)
            return None, None, None, None, None, None, None

    def decrypt(self, merged, r_left, x0_left, r_right, x0_right):
        try:
            split_idx = len(merged) // 2
            permuted_left = merged[:split_idx]
            permuted_right = merged[split_idx:]
            validate_dna_seq(permuted_left)
            validate_dna_seq(permuted_right)
            validate_chaos_param('r_left', r_left, CHAOS_R_MIN, CHAOS_R_MAX)
            validate_chaos_param('x0_left', x0_left, CHAOS_X0_MIN, CHAOS_X0_MAX)
            validate_chaos_param('r_right', r_right, CHAOS_R_MIN, CHAOS_R_MAX)
            validate_chaos_param('x0_right', x0_right, CHAOS_X0_MIN, CHAOS_X0_MAX)
            mapper_left = ChaosMapper(r_left, x0_left, len(permuted_left))
            mapper_right = ChaosMapper(r_right, x0_right, len(permuted_right))
            indices_left = mapper_left.get_indices()
            indices_right = mapper_right.get_indices()
            unpermuted_left = ChaosMapper.unpermute(permuted_left, indices_left)
            unpermuted_right = ChaosMapper.unpermute(permuted_right, indices_right)
            ct_left = DNAEncoder.decode(unpermuted_left)
            ct_right = DNAEncoder.decode(unpermuted_right)
            left = self.aes_left.decrypt(ct_left)
            right = self.aes_right.decrypt(ct_right)
            if left is None or right is None:
                raise ValueError("AES decryption failed (wrong key or parameters)")
            return self.merge(left.decode(errors="ignore"), right.decode(errors="ignore"))
        except Exception as e:
            handle_exception("Decryption", e)
            return None