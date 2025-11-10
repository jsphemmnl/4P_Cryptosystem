import random
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AES_CBC:
    def __init__(self, key=None):
        self.key = key if key else self.generate_key()
    
    def generate_key(self):
        return os.urandom(32)
    
    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
        return cipher.iv + ct_bytes
    
    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        ct = ciphertext[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        try:
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt
        except ValueError:
            return None

class DNAEncoder:
    mapping = {'00':'A', '01':'T', '10':'C', '11':'G'}
    reverse_mapping = {v: k for k, v in mapping.items()}
    
    @staticmethod
    def encode(data_bytes):
        binary = ''.join(format(b, '08b') for b in data_bytes)
        return ''.join(DNAEncoder.mapping[binary[i:i+2]] for i in range(0, len(binary), 2))
    
    @staticmethod
    def decode(dna_str):
        binary = ''.join(DNAEncoder.reverse_mapping[nuc] for nuc in dna_str)
        return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))

class ChaosMapper:
    def __init__(self, r=None, x0=None, length=0):
        self.r = r if r else random.uniform(3.57, 4.0)
        self.x0 = x0 if x0 else random.uniform(0, 1)
        self.length = length

    def get_indices(self):
        x = self.x0
        sequence = []
        for _ in range(self.length):
            x = self.r * x * (1 - x)
            sequence.append(x)
        indices = list(range(self.length))
        indices.sort(key=lambda i: sequence[i])
        return indices

    @staticmethod
    def permute(seq, indices):
        return ''.join(seq[i] for i in indices)
        
    @staticmethod
    def unpermute(seq, indices):
        res = [''] * len(seq)
        for i, idx in enumerate(indices):
            res[idx] = seq[i]
        return ''.join(res)
