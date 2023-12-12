from collections import defaultdict
from math import gcd
from typing import List
from itertools import combinations


frequent_bigrams = ["ст", "но", "то", "на", "ен"]
# ["то", "он", "на", "не", "по"]
alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
#           0123456789012345678901234567890 -> 31
non_tipical_bigrams = ["оь", "йц", "йш", "ъй", "йь", "йю", "йя", "щй", "ьй", "эь", "ыа", "щю"
                       "гй", "фг", "йй", "ьь", "кы", "зщ", "йь", "оы", "рц" ]


# from lab1

def frequency_bigrams(text:str, stepUse:bool = False):
    step = 2 if stepUse else 1
    bigrams = defaultdict(int)
    for i in range(0, len(text)-1, step):
        bigram = text[i:i+2]
        bigrams[bigram] += 1
    return bigrams

def process_text(file_name:str):
    with open(file_name, "rt", encoding='utf-8') as file:
        text = file.read().lower().replace("\n", "").replace("ё", "е").replace(" ", "")
        symbols = "? , . … ; “ „ : -  ! ( ) * « » \ / — 1 2 3 4 5 6 7 8 9 0 №"
        for symbol in symbols.split():
            text = text.replace(symbol, "")
    return text

# 2
# for invertion: x^(-1) = pow(x, -1, modulo)
# for gcd: gcd(a, b)

def solve_linear_mod_expression(a:int, b:int, modulo:int):

    """ розв'язання рівнянь виду ax = b mod c """

    res = []
    if gcd(a , modulo) == 1:
        res.append(pow(a,-1,modulo) * b % modulo)
        # print(f"Рівняння {a}x = {b} mod({modulo}) : x =", res)
        return res
    elif gcd(a, modulo) > 1:
        d = gcd(a, modulo)
        # Перевірка на кратність b до НСД(a, modulo) та на можливість знайти обернений елемент
        if b % d != 0 or pow(a // d, -1, modulo // d) == None:  
            # print(f"Рівняння {a}x = {b} mod({modulo}) не має розв'язків")
            return res
        else:
            x = pow(a // d, -1, modulo // d) * (b // d) % (modulo // d)
            res = [x + (modulo // d) * i for i in range(d)]  # усі можливі корені
            # print(f"Усі можливі корені для рівняння {a}x = {b} mod({modulo}) : ", res)
            return res

def check_text(text:str, bigrams:List[str] = non_tipical_bigrams):

    """перевіряємо на наявність в тексті неможливих поєднань біграм"""

    if any(bigram in text for bigram in bigrams):
        return False
    return True


def encode_to_num(bigrams:List[str], alphabet:str = alphabet):

    """X = x[i] * m + x[i+1], де m це довжина алфавіту - нумерування біграм"""

    numsX = []
    for bigram in bigrams:
        a = bigram[0]
        b = bigram[1]
        numsX.append(alphabet.index(a) * len(alphabet) + alphabet.index(b))
    return numsX

def decode_to_bigram(bigrams_nums:List[int], alphabet:str = alphabet):

    """конвертувати біграми з циферного у буквенний вигляд"""

    bigrams  = []
    for bigram in bigrams_nums:
        l1 = alphabet[bigram // len(alphabet)]
        l2 = alphabet[bigram % len(alphabet)]

        decoded_bigram = l1+l2
        bigrams.append(decoded_bigram)

    return bigrams

def get_keys(text:str, frequent_bigrams:List[str] = frequent_bigrams, alphabet:str = alphabet):

    """шукаємо можливі ключі"""
    sorted_values = sorted(frequency_bigrams(text).items(), key=lambda x: x[1], reverse=True)
    top_5_encrypted = []
    count = 0
    temp_values = []
    # top_5_encrypted = list(dict(sorted_values[:5]).keys())
    for key, val in sorted_values:
        if val not in temp_values and count < 5:
            temp_values.append(val)
            top_5_encrypted.append(key)
            count += 1

    mod = len(alphabet)**2

    X = encode_to_num(frequent_bigrams)
    Y = encode_to_num(top_5_encrypted)

    keys_b = []
    keys = defaultdict(int)

    # Generate combinations of indices of X and Y
    X_combinations = list(combinations(range(len(X)), 2))
    Y_combinations = list(combinations(range(len(Y)), 2))

    for x1, x2 in X_combinations:
        for y1, y2 in Y_combinations:
            if pow(x1 - x2, -1, mod) is not None:
                a_values = solve_linear_mod_expression((X[x1]-X[x2])%mod, (Y[y1]-Y[y2])%mod, mod)
                for a in a_values:
                    if a != 0:
                        b = (Y[y1] - a*X[x1]) % mod
                        keys_b.append(b)
                keys[a] = keys_b

    # print(keys)
    return keys


def decipher(text: str, alphabet: str = alphabet):
    """ розшифровуємо текст"""
    mod = len(alphabet) ** 2
    possible_keys = get_keys(text)
    numerated_bigrams = encode_to_num(list(frequency_bigrams(text).keys()))

    for a, b_vals in possible_keys.items():
        for b in b_vals:
            if pow(a, -1, mod) is None:
                continue
            decrypted_nums = []
            for y in numerated_bigrams:
                x = (pow(a, -1, mod) * (y - b)) % mod
                decrypted_nums.append(x)
            decrypted_text = ''
            for n in decrypted_nums:
                l1 = n // len(alphabet)
                l2 = n % len(alphabet)
                bigram = alphabet[l1] + alphabet[l2]
                decrypted_text += bigram

            if check_text(decrypted_text):
                print("Текст змістовний, створено файл")
                print(f"Ключі: a = {a}, b = {b}")

                with open("decrypted.txt", "w", encoding="utf-8") as file:
                    file.write(decrypted_text)
                return 
    print("Не вдалося знайти змістовний текст")







        
test_text = process_text("V1_for_test_utf8.txt")
# get_keys(test_text)

decipher(test_text)
# не виходить змістовний текст