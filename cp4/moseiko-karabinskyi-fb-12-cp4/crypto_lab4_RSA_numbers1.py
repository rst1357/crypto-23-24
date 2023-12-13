import random
import secrets
def decimalToBinary(decimal):
    binary = []
    while decimal > 0:
        binary.insert(0, decimal % 2)
        decimal //= 2
    return binary if binary else [0]

def d_2s(p):
    s = 0
    while p % 2 == 0:
        s += 1
        p //= 2
    return s, p

def extended_gcd_2(a, b):
    old_r, r = a, b
    x, s = 1, 0
    y, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        x, s = s, x - quotient * s
        y, t = t, y - quotient * t
    gcd = old_r
    return (gcd, x, y)

def LongModPowerBarrett(A, B, N):
    if N == 1:
        return 0

    result = 1
    A = A % N
    while B > 0:
        if B % 2 == 1:
            result = (result * A) % N

        B = B // 2
        A = (A * A) % N

    return result

def miller_rabin(p, k=20):
    s, d = d_2s(p - 1)
    for _ in range(k):
        x = random.randint(2, p - 2)
        gcd, _, _ = extended_gcd_2(x, p)
        if gcd > 1:
            return False
        else:
            l = LongModPowerBarrett(x, d, p)
            if l != 1 and l != p - 1:
                for r in range(1, s):
                    xr = LongModPowerBarrett(x, d * 2**r, p)
                    if xr == p - 1:
                        break
                else:
                    return False
    return True

def find_p():
    while True:
        p = secrets.randbits(256)
        if miller_rabin(p, k=20):
            return p

def find_q():
    while True:
        q = secrets.randbits(256)
        if miller_rabin(q, k=20):
            return q

def inverse(a, m):
    gcd, x, y = extended_gcd_2(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def congurence(a, b, m):
    gcd, x, y = extended_gcd_2(a,m)
    if b % gcd !=0:
        return 0

    find_x = inverse(a//gcd, m//gcd) * (b//gcd) % (m//gcd)
    return find_x

def gen_pp_qq1():
    p = find_p()
    q = find_q()
    p1 = find_p()
    q1 = find_q()
    while p*q >= p1*q1:
        return(gen_pp_qq1())
    return p,q,p1,q1



def GenerateKey(p, q):
     n = p * q
     fn = (p-1)*(q-1)
     e = 2**16 + 1
     d = congurence(e, 1, fn)
     return p, q, n, e, d

def modular_pow(base, e, mod):
    result = 1
    base = base % mod

    while e > 0:
        if e % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        e //= 2

    return result


def encrypt_rsa(message, public_key):
    n, e = public_key
    return modular_pow(message, e,n)


def decrypt_rsa(message, secret_key):
    d = secret_key[2]
    p = secret_key[0]
    q = secret_key[1]
    n = p * q
    return modular_pow(message, d, n)



def signature(message, secret_key):

    d = secret_key[2]
    p = secret_key[0]
    q = secret_key[1]
    n = p * q

    return modular_pow(message, d, n)



def verify_sign(sign_mes, message, public_key):
    n, e = public_key
    tst = modular_pow(sign_mes, e, n)
    return tst == message

def send_key(prvt_key_A, public_key_b, msg):
    k1 = encrypt_rsa(msg, public_key_b)
    S = signature(msg, prvt_key_A)
    S1 = encrypt_rsa(S, public_key_b)
    return k1,S1

def recieve_key(prvt_key_B, public_A, k1, S1):
    k = decrypt_rsa(k1, prvt_key_B)
    S = decrypt_rsa(S1, prvt_key_B)
    if  verify_sign(S, k, public_A) == False:
        raise TypeError("cant verify signature")
    else:
        return k,S


print()

qqq = gen_pp_qq1()
print(f"Згенеровані числа p і q для користувача A: \np={qqq[0]} \nq={qqq[1]}")
print("\n")
print(f"Згенеровані числа p1 і q1 для користувача B: \np1={qqq[2]} \nq1={qqq[3]}")
print("\n")
p, q, n, e, d = GenerateKey(qqq[0], qqq[1])
p1, q1, n1, e1, d1 = GenerateKey(qqq[2], qqq[3])
open_key_A = (n, e)
open_key_B = (n1, e1)
secret_key_A = (p,q,d)
secret_key_B = (p1,q1,d1)
print("Відкритий ключ А", open_key_A)
print("Відкритий ключ B", open_key_B)
print("Таємний ключ А", secret_key_A)
print("Таємний ключ B", secret_key_B)
print("\n")

#Завдання 4 користувач A
Message = 123456789
encrypted_message_A = encrypt_rsa(Message,  open_key_A)
e_sign_A = signature(Message, secret_key_A)
print("Оригінальне повідовлемення користувача A:", Message)
print("Закодоване повідомлення користувачем A: ", encrypted_message_A)
print("Повідомлення підписане цифровим підписом користувача A",e_sign_A)
print("розкодоване повідомлення користувача A", decrypt_rsa(encrypted_message_A, secret_key_A))
print("Перевірка цифрового підпису користувача A, цифровий підпис вірний??? ==", verify_sign(e_sign_A, Message, open_key_A))
#print(hex(n))
print(hex(encrypted_message_A))

print("\n")

#Завдання 4 користувач B
Message_2 = 988814
encrypted_message_B = encrypt_rsa(Message_2,  open_key_B)
e_sign_B = signature(Message_2, secret_key_B)
print("Оригінальне повідовлемення користувача B:", Message_2)
print("Закодоване повідомлення користувачем B: ", encrypted_message_B)
print("Повідомлення підписане цифровим підписом користувача B",e_sign_B)
print("розкодоване повідомлення користувача B", decrypt_rsa(encrypted_message_B, secret_key_B))
print("Перевірка цифрового підпису користувача B, цифровий підпис вірний??? ==", verify_sign(e_sign_B, Message_2, open_key_B))

#Звдання 5

gen_message = random.randint(1,  open_key_A[0])

k1, S1 = send_key(secret_key_A, open_key_B, gen_message)
print("закодований ключ:", k1)
print("закодований підпис:", S1)
print("\n")
k, S = recieve_key(secret_key_B, open_key_A, k1, S1)
print("декодований ключ:", k)
print("декодований підпис:", S)

#msg33 = 12345
#serv_pub_key = (int("9A3F4094520BA92BEF724072728BA038C54D90478E522CFB6759A31DB0EC19B9", 16), int("10001", 16))
#encr_serv = encrypt_rsa(msg33, serv_pub_key)
#zzz = encr_serv
#print(hex(encr_serv))