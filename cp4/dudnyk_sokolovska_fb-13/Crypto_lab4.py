import random
from typing import List
import sys

E = 2**16 + 1


def get_inversed(a, m):

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

# lab4

def gcd(a:int, b:int):
    # easy gcd
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    

def horner_pow(num:int, exp:int, mod:int):
    res = 1
    num %= mod
    bits_num = bin(exp)[2:]
    for i in bits_num:
        res = (res*res) % mod
        if i == '1':
            res *= num % mod
    res %= mod
    return res

def test_easy_deviders(p:int):
    if p % 2 == 0 or p % 3 == 0 or p % 5 == 0 or p % 7== 0 or p % 11 == 0: 
        return False
    return True

def miller_rabin(p:int, k:int = 50):

    if test_easy_deviders(p) and p > 1:
        d, s = p-1, 0

        while d % 2 == 1:
            s += 1
            d //= 2

        for _ in range(k):
            x = random.randint(2, p-1)
            if gcd(x, p) != 1:  return False
            
            x_1 = horner_pow(x, d, p)
            if x_1 == 1 or x_1 == -1 : return True

            for r in range(1, s):
                x_r = horner_pow(x, d*(2**r), p)
                if x_r == -1 :  return True
    
    return False

# print(miller_rabin(324))        # ділиться на 2
# print(miller_rabin(321))        # ділиться на 3 
# print(miller_rabin(657))        # ділиться на 3   
# print(miller_rabin(179))        # посте


def get_random_prime(start:int = None, end:int = None, bits = None, toprint:bool=False):
    if bits is not None:
        while True:
            num = random.getrandbits(bits)
            if miller_rabin(num) : 
                if toprint: print(num)
                return num

    elif start is not None and end is not None:
        while True:
            num = random.randint(start, end)
            if miller_rabin(num): 
                if toprint: print(num)
                return num
    else:
        raise ValueError("Некорректно задано початкове та кінцеве значення інтервалу або кількість бітів!")
    
# get_random_prime(bits=64, toprint=True)
# get_random_prime(bits=128, toprint=True)
# get_random_prime(start=690, end=20578, toprint=True)


def get_keys_pairs(bits:int=256):
    secret_keys = {}
    open_keys = {}

    # for A, n and e - keys
    secret_keys['p'] = get_random_prime(bits=bits)
    secret_keys['q'] = get_random_prime(bits=bits)

    open_keys['n'] = secret_keys['p'] * secret_keys['q']
    euler = (secret_keys['p'] - 1) * (secret_keys['q'] - 1)

    open_keys['e'] = E
    secret_keys['d'] = get_inversed(open_keys['e'], euler)

    return secret_keys, open_keys

# print(get_keys_pairs()) 

def generate_pairs_AB():
    A_secretKeys, A_openKeys = get_keys_pairs()
    # перевірка q1*p1 <= q2*p2
    # міняємо
    B_secretKeys, B_openKeys = get_keys_pairs()
    if B_secretKeys['q'] * B_secretKeys['p'] > A_secretKeys['q'] * A_secretKeys['p']: 
        A_secretKeys, B_secretKeys = B_secretKeys, A_secretKeys

    return A_openKeys, A_secretKeys, B_openKeys, B_secretKeys

# A_openKeys, A_secretKeys, B_openKeys, B_secretKeys = generate_pairs_AB()
# print("A\n", A_openKeys, A_secretKeys, "\n\nB\n", B_openKeys, B_secretKeys)

def cipher_message(M: int, openKeys: dict):
    n, e = openKeys['n'], openKeys['e']
    if M >= n:
        raise ValueError(f"Ваше повідомлення занадто велике для шифрування!\nПовідомлення: {M}\nn: {n}")
    elif M < 0:
        raise ValueError("Ваше повідомлення менше 0")
    res = horner_pow(M, e, n)
    return res

def decipher_message(C: int, privateKeys: dict=None, openKeys: dict = None):
    if privateKeys is not None:
        p, q, d = privateKeys['p'], privateKeys['q'], privateKeys['d']
        n = p * q
    else :
        n = openKeys['n']
        
    if C >= n:
        raise ValueError(f"Криптограма завелика для розшифрування!\nКриптограма: {C}\nn: {n}")
    elif C < 0:
        raise ValueError("Криптограма менше нуля!")
    res = horner_pow(C, d, n)
    return res

def crypto_sign(M:int, private_keys:dict):
    S = horner_pow(M, private_keys['d'], private_keys['p'] * private_keys['q'])
    return S

def verification(M:int, S:int, open_keys:dict):
    return M == horner_pow(S, open_keys['e'], open_keys['n'])

def send_message(M:int, A_privateKeys:dict, B_openKeys:dict):
    encrypted_M = cipher_message(M, B_openKeys)
    S = crypto_sign(M, A_privateKeys)
    S1 = horner_pow(S, B_openKeys['e'], B_openKeys['n'])

    print("Підписанне повідомлення відправлено успішно!")

    return encrypted_M, S1

def receive_message(encrypted_M:int, S1:int, B_privateKeys:dict, A_openKeys:dict):
    M = decipher_message(encrypted_M, B_privateKeys)
    S = decipher_message(S1, B_privateKeys)

    verified = verification(M, S, A_openKeys)

    if not verified:
        print("Аутентифікацію провалено! Підпис та/або ключі невірні!")
    else:
        print("Аутентифікацію за підписом пройдено успішно!\nОтримане повідомлення:", M)

# messageA = random.randint(1, 130)
# messageB = random.randint(131, 260)
# print("messageA:", messageA, f"(length={sys.getsizeof(messageA)})\nmessageB:", messageB, f"(length={sys.getsizeof(messageB)})")

# A_openKeys, A_secretKeys, B_openKeys, B_secretKeys = generate_pairs_AB()

# messageA_encrypted, messageB_encrypted = cipher_message(messageA, B_openKeys), cipher_message(messageB, A_openKeys)
# print("encrypted message for A: ", messageA_encrypted, "\nencrypted message for B: ", messageB_encrypted)

# messageA_original, messageB_original = decipher_message(messageA_encrypted, B_secretKeys), decipher_message(messageB_encrypted, A_secretKeys)
# print("decrypted message for A: ", messageA_original, "\ndecrypted message for B: ", messageB_original)

# encryptedA , sign1= send_message(messageA, A_secretKeys, B_openKeys)
# receive_message(encryptedA, sign1, B_secretKeys, A_openKeys)

# encryptedB, sign2 = send_message(messageB, B_secretKeys, A_openKeys)
# receive_message(encryptedB, sign2, A_secretKeys, B_openKeys)


# статичні дані для перевірки сервером
# 128 bits для спрощення перевірки

static_open_keys = {'n' : 77290010257482367667872392744139331143985885480088616497010126116309693800311,
                    'e' : E}

static_secret_keys = {'p': 293295450714564884956358051352919305107, 'q': 263522704048693210092176810079307682573, 
                      'd': 38584269429391803454381205630559935563415609437152597019042333049816532366585}

message_static = 126
print("n = ", hex(static_open_keys['n'])[2:].upper(), "\ne = ", bin(static_open_keys['e'])[2:])
# print(static_secret_keys)
encrypted = cipher_message(message_static, static_open_keys)
encrypted_server = int('4253C72DDF34930D77E4672C701A23DB57CBAE97D4CD6ADD00310D9D96846792', 16)
# print("encrypted message: ", hex(encrypted)[2:].upper())
print("decrypted message:", decipher_message(encrypted_server, privateKeys=static_secret_keys))
