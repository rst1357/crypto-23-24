import random

log = []


def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = ext_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def modInverse(num, mod):
    a, b = num, mod
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return x % mod


def miller_rabin(p):
    d = p - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(10):
        x = random.randint(1, p - 1)
        pw = pow(x, d, p)
        if pw == 1 or pw == p - 1:
            continue

        for _ in range(1, s):
            pw = pow(pw, 2, p)
            if pw == p - 1:
                break
        else:
            return False

    return True


def find_primes():
    prime = random.getrandbits(256)
    if prime % 2 == 0:
        prime += 1
    while not miller_rabin(prime):
        log.append(prime)
        prime += 2

    return prime

def gen_pairs():
    p, q, p1, q1 = 0, 0, 0, 0
    while True:
        p = find_primes()
        q = find_primes()
        p1 = find_primes()
        q1 = find_primes()
        if p*q < p1*q1:
            break
    return p, q, p1, q1


def gen_rsa_keys(p, q):
    n = p*q
    oiler = (p-1)*(q-1)

    while True:
        e = random.randint(2, oiler-1)
        #e = 65537
        if ext_gcd(e, oiler)[0] == 1:
            d = modInverse(e, oiler)
            break

    return (e, n), (d, p, q)


def encrypt(M, e, n):
    return pow(M, e, n)


def decrypt(C, d, n):
    return pow(C, d, n)


def sign(M, Sec_key):
    S = pow(M, Sec_key[0], Sec_key[1]*Sec_key[2])
    return (M, S)


def verify(S, Pub_key):
    return S[0] == pow(S[1], Pub_key[0], Pub_key[1])


def send_key(k, Sec_key, Pub_A, Pub_B):
    k1 = pow(k, Pub_B[0], Pub_B[1])
    S = pow(k, Sec_key[0], Pub_A[1])
    S1 = pow(S, Pub_B[0], Pub_B[1])
    print(f"k1: {k1} \nS: {S}\nS1: {S1}")
    return (k1, S1)


def recieve_key(msg, Sec_key, Pub_A):
    k = pow(msg[0], Sec_key[0], Sec_key[1]*Sec_key[2])
    S = pow(msg[1], Sec_key[0], Sec_key[1]*Sec_key[2])
    check = k == pow(S, Pub_A[0], Pub_A[1])
    print(f"k: {k} \nS: {S}\ncheck: {check}")
    return (k, check)


if __name__ == '__main__':
    p, q, p1, q1 = gen_pairs()
    Pub_A, Sec_A = gen_rsa_keys(p, q)
    Pub_B, Sec_B = gen_rsa_keys(p1, q1)

    print("Відкритий ключA (e, n):", Pub_A)
    print("Секретний ключA (d, p, q):", Sec_A)
    print("Відкритий ключB (e, n):", Pub_B)
    print("Секретний ключB (d, p, q):", Sec_B)
    print(f"Кандидати, що не пройшли ({len(log)}):", log[:10])
    M = 4561119
    print("ВТ:", M)
    C = encrypt(M, Pub_A[0], Pub_A[1])
    print("ШТ:", C)
    M = decrypt(C, Sec_A[0], Pub_A[1])
    print("Розшифрований:", M)
    signed = sign(M, Sec_A)
    print("Підпис (M, S):", signed)
    print("Перевірка підпису:", verify(signed, Pub_A))
    msg = send_key(667722, Sec_A, Pub_A, Pub_B)
    print("Відправлений ключ (k1, S1):", msg)
    print("Отриманий ключ (k, check):", recieve_key(msg, Sec_B, Pub_A))
    #print(verify((147, 70658818805101902294903941626363087046039463031131312227243706622088357161622), (65537, 70758511977975655009870760255940597219099169104907122289963773478977252103141)))
