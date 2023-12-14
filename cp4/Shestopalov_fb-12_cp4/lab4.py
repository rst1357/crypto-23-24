import random
import math

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def miller_rabin(n, k=5): # number of tests
    if n == 2 or n == 3:
        return True

    if n <= 1 or n % 2 == 0:
        return False

    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=256):
    p = 4
    while not miller_rabin(p, 128):
        p = generate_prime_candidate(length)
    return p

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = pow(e, -1, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    e, n = pk
    return [pow(ord(char), e, n) for char in plaintext]

def decrypt(pk, ciphertext):
    d, n = pk
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)

def sign(pk, plaintext):
    d, n = pk
    return [pow(ord(char), d, n) for char in plaintext]

def verify(pk, signature):
    e, n = pk
    return ''.join(chr(pow(char, e, n)) for char in signature)

def sendKey(pk, key):
    e, n = pk
    return [pow(ord(char), e, n) for char in key]

def receiveKey(pk, encrypted_key):
    d, n = pk
    return ''.join(chr(pow(char, d, n)) for char in encrypted_key)

p = generate_prime_number()
q = generate_prime_number()
public, private = generate_keypair(p, q)
encrypted_msg = encrypt(public, 'Hello!')
print(encrypted_msg)
decrypted_msg = decrypt(private, encrypted_msg)
print(decrypted_msg)
signature = sign(private, 'Hello!')
print(signature)
verified = verify(public, signature)
print(verified)
sent_key = sendKey(public, 'Key')
print(sent_key)
received_key = receiveKey(private, sent_key)
print(received_key)
