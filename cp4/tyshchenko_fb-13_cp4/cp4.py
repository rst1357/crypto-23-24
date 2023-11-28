#!/bin/python3

from random import randint, getrandbits
import sys

MAX_K = 20

# Calculate gcd and inverses.
# Return list [gcd(a, b), a^(-1), b^(-1)].
def euclid(a: int, b: int) -> list:
    # Make positive.
    a, b = abs(a), abs(b)
    # Initialize base values.
    u = [1, 0]
    v = [0, 1]
    a0, b0 = a, b
    # Swap values if necessary.
    if a > b:
        a, b = b, a
        u, v = v, u
        a0, b0 = b, a
    r = a % b
    q = [a // b]
    # Find gcd(a, b) and inverses.
    while a % b:
        a = b
        b = r
        r = a % b
        u.append(u[-2] - q[-1] * u[-1])
        v.append(v[-2] - q[-1] * v[-1])
        q.append(a // b)
    # If found inverses are negative, make them positive.
    if u[-1] < 0:
        u[-1] += b0
    if v[-1] < 0:
        v[-1] += a0
    return [b, u[-1], v[-1]]
    
# Calculate euler function of a.
# Returns phi(n).
def euler(n: int, p=0, q=0) -> int:
    # Case incorrect input.
    if n <= 0:
        print(f"euler: incorrect input {n}")
        return -1
    # Case factorization is given.
    if p != 0 and q != 0:
        result = (p - 1) * (q - 1)
    else:
        # Count number of coprime numbers to a that are less than a.
        result = 1
        for i in range(2, n):
            if euclid(n, i)[0] == 1:
                result += 1
    return result
    
# Calculate x in power a with module m (Horner's scheme).
# Returns x ^ a mod m.
def horner(x: int, a: int, m: int) -> int:
    # Transform a to binary form.
    # Return coefficient list [a_0, a_1, ... , a_k-1].
    def to_bin(a: int) -> list:
        result = []
        while a != 0:
            result.append(a % 2)
            a //= 2
        return result
        
    # Case incorrect input.
    if x < 0 or x >= m or a < 0:
        print(f"horner: incorrect input x={x}, a={a}, m={m}")
        return -1
    a_bin = to_bin(a)
    k = len(a_bin)
    y = 1
    for i in range(k - 1, -1, -1):
        y = (y ** 2) % m
        y = (y * x ** a_bin[i]) % m
    return y
    
# Check if p is prime.
# Returns True if it is and False otherwise.
def miller_rabin(p: int, k=MAX_K) -> bool:
    # Find such d and s that: p - 1 = d * 2 ^ s.
    # Returns list [d, s].
    def decompose(p: int) -> list:
        if p % 2 == 0:
            print(f"miller_rabin (decompose): incorrect input {p}")
            return -1
        d = p - 1
        s = 0
        # Divide p - 1 by 2 s times.
        # What is left is d.
        while d % 2 == 0:
            s += 1
            d //= 2
        return [d, s]
        
    # Check if p is a strong pseudoprime with base a (2 methods).
    # Returns True if it is and False otherwise.
    def is_pseudoprime(p: int, a: int, d: int, s: int) -> bool:
        # Method I.        
        # Check if a ^ d = 1 (mod p).
        if pow(a, d, p) == 1:
            return True
        # Method II.
        else:
            # 0 <= r < s.
            for r in range(s):
                # Check if a ^ (d * 2 ^ r) = -1 (mod p).
                if pow(a, d * 2 ** r, p) == p - 1:
                    return True
            return False
          
    # Preprocess.
    d, s = decompose(p)
    for a in [2, 3, 5, 7]:
        if not is_pseudoprime(p, a, d, s):
            return False
    # Initialize algorithm.
    counter = 0
    while counter < k:
        x = randint(2, p - 1)
        if euclid(p, x)[0] != 1:
            return False
        if not is_pseudoprime(p, a, d, s):
            return False
        else:
            counter += 1
    return True

# NOT USED
# Get a random prime number withing range [n0, n1].
def get_prime(n0: int, n1: int, k=MAX_K) -> int:
    while True:
        x = randint(n0, n1)
        m0 = x + (x % 2 == 0)
        last = (n1 - m0) // 2
        for i in range(last + 1):
            if miller_rabin(m0 + 2 * i, k):
                return m0 + 2 * i

# Get a random prime that is suitable for RSA.
# Returns prime number p of more than 256 bits: p = 2ip' + 1.
# p' - a 256 bit prime number.
def get_RSA_prime(k=MAX_K) -> int:
    MAX_ITERS = 5
    
    # Generate random 256 prime.
    def get_RSA_prime() -> int:
        nonlocal k
        while True:
            x = getrandbits(256)
            # If x is even, make it odd.
            x += (x % 2 == 0)
            for p in range(x, (2 * x - 2) + 1, 2):
                if miller_rabin(p, k):
                    return p

    # Try to find such p that: p = 2ip' + 1. 
    p1 = get_RSA_prime()
    i = 1
    counter = 0
    while counter < MAX_ITERS:
        p = 2 * i * p1 + 1
        if miller_rabin(p, k):
            return p
        i += 1
        counter += 1
    return p1

# Generate key pair list.
# Returns key list [public_key, private_key].
# public_key = [e, n]
# private_key = [d, p, q]
def generate_key_pair() -> list:
    e = pow(2, 16) + 1
    # Set basic case.
    p = get_RSA_prime()
    q = get_RSA_prime()
    n = p * q
    phi = euler(n, p=p, q=q)
    # Find suitable primes p and q.
    val = euclid(e, phi)
    while val[0] != 1:
        p = get_RSA_prime()
        q = get_RSA_prime()
        n = p * q
        phi = euler(n, p=p, q=q)
        val = euclid(e, phi)
    d = val[1]
    return [[e, n], [d, p, q]]

# Encrypt a message M with a public key pubkey = [e, n].
# Returns encrypted message.
def encrypt(M: int, pubkey: list) -> int:
    e, n = pubkey
    # Case invalid input.
    if M >= n:
        print(f"encrypt: invalid input M={M} >= n={n}")
        return -1
    
    return horner(M, e, n)
    
# Decrypt a message C with a private key privkey = [d, p, q].
# Returns decrypted message.
def decrypt(C: int, privkey: list) -> int:
    d, p, q = privkey
    n = p * q
    # Case invalid input.
    if C >= n:
        print(f"decrypt: invalid input C={C} >= n={n}")
        return -1

    return horner(C, d, n)

# Sign message M with a private key privkey = [d, p. q].
# Returns list [M, S].
# S - digital signature.
def sign(M: int, privkey: list) -> list:
    d, p, q = privkey
    S = horner(M, d, p * q)
    return [M, S]

# Check digital signature with a public key pubkey = [e, n].
# Returns True if signature is correct and False otherwise.
def verify(signed: list, pubkey: list) -> bool:
    M, S = signed
    e, n = pubkey
    return horner(S, e, n) == M

# A sends encrypted signed secret key k to B.
# k - secret key.
# privkeyA = [d, p, q]
# pubkeyA = [e, n]
# pubkeyB = [e1, n1]
# Returns list [k1, S1]
def send_key(k: int, privkeyA: list, pubkeyA: list, pubkeyB: list) -> list:
    d, p, q = privkeyA
    e, n = pubkeyA
    e1, n1 = pubkeyB
    # Case invalid input.
    if k >= n:
        print(f"send_key: invalid input k={k} >= n={n}")
        return -1
    if n1 < n:
        print(f"send_key: invalid input n1={n1} < n={n}")
        return -1
        
    # Calculate digital signatures S, S1 and key k1.
    S = horner(k, d, n)
    S1 = horner(S, e1, n1)
    k1 = horner(k, e1, n1)
    return [k1, S1]

# B receives encrypted signed secret key k from A and verifies it.
# k - secret key.
# privkeyB = [d1, p1, q1]
# pubkeyA = [e, n]
# pubkeyB = [e1, n1]
# Returns True if signature is correct and False otherwise.
def receive_key(signed: list, privkeyB: list, pubkeyA: list, pubkeyB: list) -> bool:
    k1, S1 = signed
    d1, p1, q1 = privkeyB
    e1, n1 = pubkeyB
    # Restore digital signature S and key k.
    k = horner(k1, d1, n1)
    S = horner(S1, d1, n1)
    return verify([k, S], pubkeyA)
    
# Test all functions.
def tests() -> None:
    print("=== TESTS ===")
    # Find gcd and inverses.
    print(f"""\n=== GCD & INVERSES TEST ===
euclid(155, 29) = {euclid(155, 29)}
euclid(2, -5) = {euclid(2, -5)}
euclid(-15, 40) = {euclid(-15, 40)}""")
    # Find euler function.
    print(f"""\n=== EULER FUNCTION TEST ===
phi(1) = {euler(1)}
phi(5) = {euler(5)}
phi(6) = {euler(6)}
phi(23147) (factorization is unknown) = {euler(23147)}
phi(23147) (factorization is given) = {euler(23147, p=79, q=293)}""")
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
    print(f"""\n=== PRIME GENERATION TEST ===
(1, 100) = {get_prime(1, 100)}
(250, 1000) = {get_prime(250, 1000)}
(500, 10000) = {get_prime(500, 10000)}
(5000, 10000) = {get_prime(5000, 10000)}
RSA prime = {get_RSA_prime(k=10)}""")
    # Generate key pair for RSA.
    keys = generate_key_pair()
    print(f"""\n=== RSA KEY PAIR GENERATION TEST ===
Public key:\t(e, n) = ({keys[0]})
Private key:\td, p, q = {keys[1][0]}, {keys[1][1]}, {keys[1][2]}""")
    # Encrypt and decrypt a message.
    M = randint(1, pow(2, 16))
    C = encrypt(M, keys[0])
    print(f"""\n=== RSA ENCRYPTION/DECRYPTION TEST ===
Original:\t{M}
Encrypted:\t{C}
Decrypted:\t{decrypt(C, keys[1])}""")
    # Sign and verify a message.
    privkey = keys[1]
    signed = sign(M, privkey)
    print(f"""\n=== RSA SIGN/VERIFY TEST ===
Message:\t{signed[0]}
Signature:\t{signed[1]}
Correct (right key):\t{verify(signed, keys[0])}
Correct (wrong key):\t{verify(signed, [29, 79])}""")
    # Key transferring.
    k = get_prime(1, 100)
    # Generate such pair of keys that: nA <= nB.
    keysA = generate_key_pair()
    keysB = generate_key_pair()
    while keysA[0][1] > keysB[0][1]:
        keysA = generate_key_pair()
    # Send and receive key.
    signed = send_key(k, keysA[1], keysA[0], keysB[0])
    received_correct = receive_key(signed, keysB[1], keysA[0], keysB[0])
    print(f"""\n=== RSA SEND/RECEIVE KEY TEST ===
Secret key:\t{k}
A keys:\t(e, n) = ({keysA[0]}), (d, p, q) = {keysA[1]}
B keys:\t(e1, n1) = ({keysB[0]}), (d1, p1, q1) = {keysB[1]}
Message:\t{signed[0]}
Signature:\t{signed[1]}
Correct (right key):\t{received_correct}
Correct (wrong key):\t{receive_key(signed, keysB[1], [29, 79], keysB[0])}""")
    
# Solve task.
def solve() -> None:
    pass

if __name__ == "__main__":
    tests()
