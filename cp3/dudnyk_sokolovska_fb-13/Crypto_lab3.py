from collections import defaultdict
from math import gcd
from typing import List

frequent_bigrams = ["ст", "но", "то", "на", "ен"]
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
#           01234567890123456789012345678901c

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

    if gcd(a , modulo) == 1:
        res = pow(a,-1,modulo) * b % modulo
        print(f"Рівняння {a}x = {b} mod({modulo}) : x =", res)
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
            print(f"Усі можливі корені для рівняння {a}x = {b} mod({modulo}) : ", res)
            return res

def get_X(X:List[str], alphabet:str = alphabet):
    numsX = []
    for x in X:
        a = x[0]
        b = x[1]
        numsX.append(alphabet.index(a) * len(alphabet) + alphabet.index(b))
    return numsX

def get_Y(X:List[int], Y:List[int], alphabet:str = alphabet):
    numsY = []
    for y in Y:
        a = y[0]
        b = y[1]
        if gcd(alphabet.index(a), len(alphabet)) == 1 and (alphabet.index(b) in range(0, len(alphabet)+1)): pass
        numsY.append((alphabet.index(a) * X + alphabet.index(b)) % len(alphabet)^2)
    return numsY

# def get_key_options(X: List[str], Y: List[str], alphabet:str = alphabet): 
#     """ передаємо наші біграми, X: найчастіші 5 біграм у нормальному тексті, Y - у шифротексті, і знаходимо можливі коефіцієнти для дешифрування """
#     numsX = []
#     numsY = []
#     # for x in X:



# # тестування розв'язку рівнянь - робе
# solve_linear_mod_expression(3, 8, 9) # нема коренів
# solve_linear_mod_expression(2, 5, 7)
# solve_linear_mod_expression(4, 3, 11)
# solve_linear_mod_expression(7, 9, 13)
# solve_linear_mod_expression(9, 12, 17)
# solve_linear_mod_expression(6, 10, 14)

# пошук найчастіших біграм у шифротексті
test_text = process_text("01_utf8.txt")
sorted_values = sorted(frequency_bigrams(test_text).items(), key=lambda x: x[1], reverse=True)
top_5_values = dict(sorted_values[:5])
print(top_5_values)

# print(get_X(frequent_bigrams))
# print(get_Y(top_5_values))
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!