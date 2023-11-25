#!/bin/python3

from random import randint
import sys

# Calculate greatest simple divisor of a and b.
def gcd(a: int, b: int) -> int:
    pass
    
# Calculate euler function of a.
def euler(a: int) -> int:
    pass
    
# Calculate x in power a with module m (Horner's scheme).
def horner(x: int, a: int, m: int) -> int:
    # Transform a to binary form.
    # Return coefficient list [a_k-1, a_k-2, ... , a_0].
    def to_bin(a: int) -> list:
        pass
    
# Check if p is prime.
def miller_rabin() -> bool:
    # Find such d and s that: p - 1 = d * 2 ^ s.
    # Return list [d, s].
    def decompose(p: int) -> list:
        pass
        
    # Check if p is a strong pseudoprime with base a (2 methods).
    def is_pseudoprime(p: int, a: int) -> bool:
        pass
        # Check if p is even.
        # Find d.
        # Check if a ^ d = 1 (mod p).
        # Check if a ^ (d * 2 ^ r) = -1 (mod p).
          
    # Check if p is pseudoprime with bases 2, 3, 5, 7, 11.
    # Find d.
    # Choose random k.
    # While counter < k:
    #   Choose random 1 < x < p.
    #   Check if gcd(p, x) = 1.
    #   Check if p is pseudoprime with base x (2 methods).
    #   If so, counter++, else return.
    pass

# Get a random prime number withing range [n0, n1].   
def get_prime(n0: int, n1: int) -> int:
    # Get random n0 <= x <= n1.
    # Calculate m0.
    # Find and check p' and q'.
    # Find and check p = 2ip' + 1 and q = 2jq' + 1.
    pass
    
# Generate key pair list [public_key, private_key].
# public_key = [e, n]
# private_key = [d, n]
def generate_key_pair() -> list:
    pass

# Encrypt message pt with pubkey.
def encrypt(pt: str, pubkey: list) -> str:
    pass

# Decrypt encrypted message ct with privkey.
def decrypt(ct: str, privkey: list) -> str:
    pass

# Sign message M with privkey.
# Returns list [M, S].
# S - digital signature.
def sign(M: str, privkey: list) -> list:
    pass

# Check digital signature.
def verify(signed: list, pubkey: list) -> bool:
    pass

# A sends encrypted signed secret key k to B.
# k - secret key.
# privkeyA = [d, n]
# pubkeyA = [e, n]
# pubkeyB = [e1, n1]
# Returns list [k1, S1]
def send_key(k: str, privkeyA: list, pubkeyA: list, pubkeyB: list) -> list:
    # Check if n1 >= n.
    # Calculate:
    # * k1 = k ^ e1 (mod n1)
    # * S1 = S ^ e1 (mod n1)
    # * S = k ^ d (mod n)
    pass

# B receives encrypted signed secret key k from A and verifies it.
def receive_key(signed: list, privkeyB: list, pubkeyB: list, pubkeyA: list) -> bool:
    # Calculate:
    # * k = k1 ^ d (mod n1)
    # * S = S1 ^ d (mod n1)
    # Verify S.
    pass
    
# Test all functions.
def tests() -> None:
    pass

# Solve task.
def solve() -> None:
    pass

if __name__ == "__main__":
    solve()
