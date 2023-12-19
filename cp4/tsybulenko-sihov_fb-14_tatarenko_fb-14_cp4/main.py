from random import randint, getrandbits

def generate_prime(lenn = 256, start = None, end = None):

    while True:
        if start and not end:
            raise ValueError("You must provide both 'start' and 'end'")
        elif not start and end:
            raise ValueError("You must provide both 'start' and 'end'")
        elif start and end:
            candidate = randint(start, end)
        else:
            candidate = getrandbits(lenn)

        if try_division(candidate):
            if is_prime_miller_rabin(candidate):
                return candidate

def horner(x, power, mod):

    result = 1
    while power > 0:
        if power % 2 == 1:
            result = (result * x) % mod
        x = (x * x) % mod
        power //= 2

    return result

def try_division(n):

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for i in primes:
        if n // i == 0:
            return False
    return True

def is_prime_miller_rabin(p, k=10):

    if p == 2 or p == 3:
        return True
    if p % 2 == 0 or p == 1:
        return False

    # Кроук 0
    s, d = 0, p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Кроук 1
    for _ in range(k):
        a = randint(2, p - 2)
        x = horner(a, d, p)

        # Кроук 2
        if x == 1 or x == p - 1:
            for r in range(s - 1):
                x = horner(x, 2, p)
                if x == p - 1:
                    break
        else:
            return False  # n - складене
    return True  # n - просте

def get_prime_pairs():
    while True:
        p1 = generate_prime()
        q1 = generate_prime()
        p2 = generate_prime()
        counter = 0
        while counter < 5:
            q2 = generate_prime()
            if p1 * q1 // p2 < q2:
                return p1, q1, p2, q2
            print(f"Не пройшов q2 - {q2}")
            counter += 1
        print(f"Не пройшли:\n p1 - {p1}\n q1 - {q1}\n p2 - {p2}")

def GenerateKeyPair(p, q):
    n = p * q
    euler = (p - 1) * (q - 1)
    while True:
        e = randint(2, euler - 1)
        if gcd(e, euler) == 1:
            break
    d = invert(e, euler)
    return [d, p, q], [e, n]

def gcd(a, b):
    while(b):
       a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def invert(a, m):
    g, x, _ = extended_gcd(a, m)

    if g == 1:
        return x % m

def Encrypt(M, pubkey):
    if not isinstance(M, int):
        M = int.from_bytes(M.encode('utf-8'), byteorder='big')
    return horner(M, pubkey[0], pubkey[1])

def Decrypt(C, prkey, text=False):
    M = horner(C, prkey[0], prkey[1] * prkey[2])
    if text:
        return M.to_bytes((M.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    else:
        return M

def Sign(M, prkey):
    if not isinstance(M, int):
        M = int.from_bytes(M.encode('utf-8'), byteorder='big')
    return (M, horner(M, prkey[0], prkey[1] * prkey[2]))

def Verify(S, pubkey):

    if not isinstance(S[0], int):
        S[0] = int.from_bytes(S[0].encode('utf-8'), byteorder='big')
    sign = horner(S[1], pubkey[0], pubkey[1])
    # print(sign)
    return sign == S[0]

if __name__ == "__main__":

    p1, q1, p2, q2 = get_prime_pairs()
    pr_key_a, pub_key_a  = GenerateKeyPair(p1, q1)
    pr_key_b, pub_key_b = GenerateKeyPair(p2, q2)
    print(f"p = {p1}\n"
          f"q = {q1}\n"
          f"Public key A: {pub_key_a}\n"
          f"Private key A: {pr_key_a}\n"
          f"p = {p2}\n"
          f"q = {q2}\n"
          f"Public key B: {pub_key_b}\n"
          f"Private key A: {pr_key_b}")

    print("B ---<message>---> A")
    message = randint(2, 10000)
    print(f"Message: {message}")
    c = Encrypt(message, pub_key_a)
    print(f"Cryptogram: {c}")
    signed_message = Sign(c, pr_key_b)
    print(f"Signed message: {signed_message}")
    if Verify(signed_message, pub_key_b):
        print('Message from B is verified.')
        m = Decrypt(signed_message[0], pr_key_a)
        print(f"Decrypted message: {m}")
