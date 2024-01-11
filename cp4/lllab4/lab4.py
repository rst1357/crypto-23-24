from random import randint

interval_min = (2 ** 255) + 1
interval_max = (2 ** 256) - 1
# e = (2**16)+1


def gcd(int_a, int_b):          # НСД з лаб3
    if int_b == 0:
        return abs(int_a)
    else:
        return gcd(int_b, int_a % int_b)


def pow_l(a, d, m):             # алгоритм швидкого піднесення до степеня за модулем
    b = 1
    while d != 0:
        if (d % 2) == 1:
            b = (b * a) % m
            d = d // 2
            a = (a * a) % m
        else:
            d = d // 2
            a = (a * a) % m
    return b


def is_prime(num):                              # додаткова початкова перевірка числа на простоту
    prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for prime_num in prime_nums:
        if num % prime_num == 0:
            return 0
        else:
            return 1


def find_s_and_d(num):  # знаходження s та d (0 крок тесту Міллера-Рабіна)
    s = 0
    p = num - 1
    d = p
    while d % 2 == 0:
        s = s + 1
        d = d // 2
    return s, d


def miller_rabin_test(p):       # Тест Міллера-Рабіна
    pr = 0
    sd = find_s_and_d(p)
    s = sd[0]
    d = sd[1]
    if is_prime(p) == 1:    # додаткова перевірка
        for k in range(150):    # kєN
            x = randint(1, p)
            g = gcd(x, p)
            if g == 1:  # крок 1
                if (pow_l(x, d, p)) in [1, -1]:  # крок 2.1
                    pr = 1
                    return pr
                else:
                    for r in range(1, s - 1):   # крок 2.2
                        x_r = pow_l(x, d * (2 ** r), p)
                        if x_r == -1:
                            pr = 1
                            return pr  # cringe(break)
                        elif x_r == 1:
                            pr = 0
                            return pr
                        else:
                            continue
                    if pr == 1:
                        return pr
            else:
                pr = 0
                return pr
    return pr


def rand_prime_num(interval):          # генерація псевдовипадкового простого числа з інтервалу
    k = 0
    while k == 0:
        rand_num = randint(interval[0], interval[1])
        prime = is_prime(rand_num)
        if prime:
            prime1 = miller_rabin_test(rand_num)
            if prime1:
                return rand_num


def make_pairs(interval):      # формування пар (p,q) для двох абонентів
    while True:
        nums = [rand_prime_num(interval), rand_prime_num(interval), rand_prime_num(interval),
                rand_prime_num(interval)]
        if (nums[0] * nums[1]) <= (nums[2] * nums[3]) and len(set(nums)) == 4:  # pq<=p1q1
            return (nums[0], nums[1]), (nums[2], nums[3])


def extended_euclid(a, n):          # розширений алгоритм Евкліда з лаб 3
    result = [0, 1]
    while a != 0 and n != 0:
        if a > n:
            result.append(a // n)
            a = a % n
        elif n > a:
            result.append(n // a)
            n = n % a
        else:
            print("Оберненого не існує :(")
    for i in range(2, len(result)-1):
        result[i] = result[i - 2] + (-result[i]) * result[i - 1]
    return result[-2]


def modular_inverse(a, n):  # якщо обернений елемент виявиться від'ємним, то взяти його ще раз по модулю
    x = extended_euclid(a, n)
    if x < 0:
        return x % n
    return x


def generate_key_pair(p, q):    # генерування ключів e, n, d
    n = (p * q)
    fi = (p - 1)*(q - 1)
    k = 1
    while k == 1:
        e = randint(2, fi - 1)
        if gcd(e, fi) == 1:
            d = modular_inverse(e, fi)
            return e, n, d
        else:
            k = 1


class SubscriberKey:
    def __init__(self, subscriber_name, e, n, d):   # ім'я абонента та його ключі
        self.subscriber_name = subscriber_name
        self.e = e
        self.n = n
        self.d = d

    def encrypt(self, message):         # шифрування
        c = pow_l(message, self.e, self.n)
        return c

    def decrypt(self, enc_message):     # дешифрування
        m = pow_l(enc_message, self.d, self.n)
        return m

    def sign(self, message):            # підпис
        s = pow_l(message, self.d, self.n)
        return s

    def verify(self, message, s):       # перевірка підпису
        m = pow_l(s, self.e, self.n)
        if m == message:
            return 1
        else:
            return 0

    def send_key(self, open_key_e, open_key_n, k):  # конфіденційне розсилання ключів по відкритих каналах
        k1 = pow_l(k, open_key_e, open_key_n)
        s = pow_l(k, self.d, self.n)
        s1 = pow_l(s, open_key_e, open_key_n)
        return k1, s1

    def receive_key(self, key_e, key_n, send_key_subscriber):   # підтвердження справжності відправника
        k = pow_l(send_key_subscriber[0], self.d, self.n)
        s = pow_l(send_key_subscriber[1], self.d, self.n)
        authentication = pow_l(s, key_e, key_n)
        if authentication == k:
            return print("Authentication succeeded.")
        else:
            return print("Authentication fault!")

    def create_signature(self, message):            # створення підпису
        encrypt_message = self.encrypt(message)
        sign_message = self.sign(encrypt_message)
        return encrypt_message, sign_message

    def check_signature(self, encrypt_message, sign_message):   # перевірка підпису
        vr = self.verify(encrypt_message, sign_message)
        if vr == 1:
            print("Verification successful.")
        else:
            print("Message garbled!!!")
        decrypt_message = self.decrypt(encrypt_message)
        return decrypt_message


pairs_for_subscribers = make_pairs([interval_min, interval_max])
# print(pairs_for_subscribers)
for_A = generate_key_pair(pairs_for_subscribers[0][0], pairs_for_subscribers[0][1])
for_B = generate_key_pair(pairs_for_subscribers[1][0], pairs_for_subscribers[1][1])
# for_A = generate_key_pair(103215410456116554317730649364749076226993216453889968793952739706290096545069,
# 82977080782476587613316804504196860709837974699708924773866479823442319524287)
# for_B = generate_key_pair(102298500362828793282005913542220855102685956820664462980708127434112028799207,
# 86894184749984631598657139522826455862095561742516593812144168448686980539879)
print(f'Ключі для абонента А:')
keys_A = ['e', 'n', 'd']
for i in range(len(keys_A)):
    print(f'{keys_A[i]} : {for_A[i]}')
print(f'Ключі для абонента B:')
keys_B = ['e1', 'n1', 'd1']
for i in range(len(keys_B)):
    print(f'{keys_B[i]} : {for_B[i]}')
A = SubscriberKey('A', for_A[0], for_A[1], for_A[2])
B = SubscriberKey('B', for_B[0], for_B[1], for_B[2])
some_message = randint(0, A.n - 1)
# some_message = 8434971726723315451649187518731482526272374054321931043660830494297088495430173073503044540949065240632799412368936268142783112915981747156911258611230798
print(f'Message: {some_message}')
enc_mes_A = A.encrypt(some_message)
print(f'Encrypted message: {enc_mes_A}')
dec_message = A.decrypt(enc_mes_A)
print(f'Decrypted message: {dec_message}')
key_k = randint(0, A.n)
# key_k = 6221955839830221912723710432412134070087811550880461519318909488028422568926286270041004247594670710406245080034656805657842745896874577735576219838210602
print(f'Key k: {key_k}')
send_key = A.send_key(B.e, B.n, key_k)
print(send_key)
B.receive_key(A.e, A.n, send_key)
signature_A = A.create_signature(some_message)
print(signature_A)
check = A.check_signature(signature_A[0], signature_A[1])
print(check)


n = 271069907083902572793476553998716799677
# CBEE2A447C72D371B704C18C72128ABD (у 16-ковій)
e = int('10001', 16)
some_message = 21 #(15 у 16-ковій)
A = SubscriberKey('A', e, n, d=None)
print(A.encrypt(21))
# 239084941111324639416817542337403103810
signed_message = int('4B6CB046FB009D1F4278AC84EF27A871', 16)
print(A.verify(some_message, signed_message))