from collections import defaultdict
from math import gcd
from typing import List

frequent_bigrams = ["ст", "но", "то", "на", "ен"]
# ["то", "он", "на", "не", "по"]
alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
#           0123456789012345678901234567890 -> 31
non_tipical_bigrams = ["оь", "йц", "йш", "ъй", "йь", "йю", "йя", "щй", "ьй", "эь", "ыа", "щю"]


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
            print(f"Рівняння {a}x = {b} mod({modulo}) не має розв'язків")
            return
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

    # найчастіші біграми шифртексту
    sorted_values = sorted(frequency_bigrams(text).items(), key=lambda x: x[1], reverse=True)
    top_5_encrypted = list(dict(sorted_values[:5]).keys())

    mod = len(alphabet)**2

    X = encode_to_num(frequent_bigrams)
    Y = encode_to_num(top_5_encrypted)

    X1 = X[0]
    X2 = X[1]

    Y1 = Y[0]
    Y2 = Y[1]

    keys_a = []
    keys_b = []
    if X1 != X2 and Y1 != Y2:
        keys_a = list(solve_linear_mod_expression((X1-X2)%mod, (Y1-Y2)%mod, mod))
        for a in keys_a:
            if a != 0:
                keys_b.append((Y1 - a*X1) % mod)
            else: 
                keys_b.add(None)
        print(f'Можливі a: {keys_a}')
        print(f'Можливі b: {keys_b}')
    return keys_a, keys_b


def decipher(text:str, alphabet:str=alphabet): 

    """розшифровуємо текст: Xi = a^(-1) * (Yi - b) mod (len(alphabet))^2 і повертаємо файл з результатом якзо текст змістовний"""

    final_text = ""
    decoded_nums = []
    mod = len(alphabet)**2
    a_keys, b_keys = get_keys(text)
    numerated_bigrams = encode_to_num(list(frequency_bigrams(text).keys()))

    for Y in numerated_bigrams: 
        for a in a_keys:
            for b in b_keys:
                decoded_nums.append(solve_linear_mod_expression(a, Y-b, mod))
    
    decoded_strings = []
    for solutions in decoded_nums:
        for solution in solutions:
            if isinstance(solution, int):  # Перевіряємо, чи solution є цілим числом
                solution = [solution]  # Якщо так, створюємо список з одним цілим числом
            decoded_strings.append(decode_to_bigram(solution))

    final_text = ''.join([''.join(decoded_string) for decoded_string in decoded_strings])

    if check_text(final_text): 
        with open("decrypted_text.txt", "w", encoding="utf-8") as file:
            file.write(final_text)
    else:
        print("Текст не змістовний, файлу не створено")

  
# пошук найчастіших біграм у шифротексті
test_text = process_text("V1_for_test_utf8.txt")
# get_keys(test_text)

decipher(test_text)
# не виходить змістовний текст