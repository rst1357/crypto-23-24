#!/bin/python3

from random import randint
import sys

# Calculate greatest simple divisor of a and b.
def gcd(a: int, b: int) -> int:
    # Make positive.
    a, b = abs(a), abs(b)
    # Swap values if necessary.
    if a > b:
        a, b = b, a
    r = a % b
    # Find gcd(a, b) and inverses.
    while a % b:
        a = b
        b = r
        r = a % b
    return b
    
# Calculate euler function of a.
def euler(a: int) -> int:
    assert a > 0, "a is negative or 0"
    # Count number of coprime numbers to a that are less than a.
    result = 1
    for i in range(2, a):
        if gcd(a, i) == 1:
            result += 1
    return result
    
# Calculate x in power a with module m (Horner's scheme).
def horner(x: int, a: int, m: int) -> int:
    # Transform a to binary form.
    # Return coefficient list [a_0, a_1, ... , a_k-1].
    def to_bin(a: int) -> list:
        result = []
        while a != 0:
            result.append(a % 2)
            a //= 2
        return result
        
    assert x >= 0, "x is negative"
    assert x < m, "x is greater or equal m"
    assert a >= 0, "a is negative"
    a_bin = to_bin(a)
    k = len(a_bin)
    y = 1
    for i in range(k - 1, -1, -1):
        y = (y ** 2) % m
        y = (y * x ** a_bin[i]) % m
    return y
    
# Check if p is prime.
def miller_rabin(p: int) -> bool:
    # Find such d and s that: p - 1 = d * 2 ^ s.
    # Return list [d, s].
    def decompose(p: int) -> list:
        assert p % 2 == 1, "p is not an odd number"
        d = p - 1
        s = 0
        # Divide p - 1 by 2 s times.
        # What is left is d.
        while d % 2 == 0:
            s += 1
            d //= 2
        return [d, s]
        
    # Check if p is a strong pseudoprime with base a (2 methods).
    def is_pseudoprime(p: int, a: int, d: int, s: int) -> bool:
        # Method I.        
        # Check if a ^ d = 1 (mod p).
        if (a ** d) % p == 1:
            return True
        # Method II.
        else:
            # 0 <= r < s.
            for r in range(s):
                # Check if a ^ (d * 2 ^ r) = -1 (mod p).
                if (a ** (d * 2 ** r) + 1) % p == 0:
                    return True
            return False
          
    # Preprocess.
    d, s = decompose(p)
    for a in [2, 3, 5, 7, 11]:
        if not is_pseudoprime(p, a, d, s):
            return False
    # Initialize algorithm.
    k = randint(1, p - 1)
    counter = 0
    # Main loop.
    while counter < k:
        x = randint(2, p - 1)
        if gcd(p, x) != 1:
            return False
        if not is_pseudoprime(p, a, d, s):
            return False
        else:
            counter += 1
    return True

# Get a random prime number withing range [n0, n1].
def get_prime(n0: int, n1: int) -> int:
    MAX_ITERS = 10

    # Find p1 (p').
    def get_base_prime(n0: int, n1: int) -> int:
        while True:
            x = randint(n0, n1)
            m0 = x + (x % 2 == 0)
            last = (n1 - m0) // 2
            for i in range(last + 1):
                if miller_rabin(m0 + 2 * i):
                    return m0 + 2 * i
          
    # Find such p that p = 2ip' + 1.          
    i = 1
    p1 = get_base_prime(n0, n1)
    p = 2 * i * p1 + 1
    counter = 0
    while counter < MAX_ITERS:
        # Check if p is still in the specified range.
        if p <= n1:
            if miller_rabin(p):
                return p
            i += 1
        # ... if not, recalculate p1.
        else:
            p1 = get_base_prime(n0, n1)
            i = 1
        p = 2 * i * p1 + 1
        counter += 1
    return p1
    
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
    print("=== TESTS ===")
    # Find gcd.
    print(f"""\n=== GCD TEST ===
gcd(155, 29) = {gcd(155, 29)}
gcd(2, -5) = {gcd(2, -5)}
gcd(-15, 40) = {gcd(-15, 40)}""")
    # Find euler function.
    print(f"""\n=== EULER FUNCTION TEST ===
phi(1) = {euler(1)}
phi(2) = {euler(2)}
phi(5) = {euler(5)}
phi(6) = {euler(6)}""")
    #print(f"phi(-1) = {euler(-1)}")
    # Calculate x ^ a (mod m).
    print(f"""\n=== HORNER'S SCHEME TEST ===
14 ^ 8 mod 23 = {horner(14, 8, 23)}
1 ^ 25 mod 456 = {horner(1, 25, 456)}""")
    '''
    print(f"""3 ^ 2 mod 2 = {horner(3, 2, 2)}
2 ^ 0 mod 3 = {horner(2, 0, 3)}
0 ^ 145 mod 89 = {horner(0, 145, 89)}
12 ^ -5 mod 9 = {horner(12, -5, 9)}
-7 ^ 1 mod 5 = {horner(-7, 1, 5)}""")
    '''
    # Check prime number.
    print(f"""\n=== PRIME CHECK TEST ===
9 is prime == {miller_rabin(9)}
13 is prime == {miller_rabin(13)}
23 is prime == {miller_rabin(23)}
293 is prime == {miller_rabin(293)}""")
    '''
    print(f"""0 is prime == {miller_rabin(0)}
1 is prime == {miller_rabin(1)}
2 is prime == {miller_rabin(2)}""")
    '''
    # Find some prime number on interval.
    print(f"""\n=== PRIME FIND TEST ===
(1, 100) = {get_prime(1, 100)}
(250, 1000) = {get_prime(250, 1000)}
(500, 10000) = {get_prime(500, 10000)}
(5000, 10000) = {get_prime(5000, 10000)}""")

# Solve task.
def solve() -> None:
    pass

if __name__ == "__main__":
    tests()
