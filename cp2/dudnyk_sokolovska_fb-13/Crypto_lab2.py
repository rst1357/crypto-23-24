import re
import pandas as pd
from collections import defaultdict
from random import choice
import numpy as np
import matplotlib.pyplot as plt

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
#           012345678901234567890123456789
CI_RUSSIAN = 0.0553
I0 = 0.03333333333333333
FREQ_LETTERS = ['о', 'а', 'е', 'и', 'н', 'т']

# from lab1
def process_text(file_name):
    with open(file_name, "rt", encoding='utf-8') as file:
        text = file.read().lower().replace("\n", "").replace("ё", "е").replace(" ", "")
        symbols = "? , . … ; “ „ : -  ! ( ) * « » \ / — 1 2 3 4 5 6 7 8 9 0 №"
        for symbol in symbols.split():
            text = text.replace(symbol, "")
    return text

def frequency(text:str, symbols_list:str = alphabet):
    freq_dict = defaultdict(int)
    for i in symbols_list:
        matches = re.findall(rf'{i}', text)
        freq_dict[i] = len(matches)
    return freq_dict

# 2
def encryption(text:str, key:str, output_file:str, alphabet:str = alphabet): 
    encrypted_text = ""
    for i in range(len(text)):
        letter_index = alphabet.index(text[i])
        key_index = alphabet.index(key[i % len(key)])
        c = (letter_index + key_index) % len(alphabet)
        encrypted_text += alphabet[c]

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)


def decryption(text:str, key:str, output_file:str, alphabet:str = alphabet):
    decrypted_text = ""
    for i in range(len(text)):
        letter_index = alphabet.index(text[i])
        key_index = alphabet.index(key[i % len(key)])
        c = (letter_index - key_index + len(alphabet)) % len(alphabet)
        decrypted_text += alphabet[c]
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)

def split_text(text:str, r:int):
    parts = [text[i:i + r] for i in range(0, len(text), r)]
    return parts

def draw_graph(dictionary:dict):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    plt.bar(keys, values, color='b')
    plt.title('')
    plt.xlabel('Довжина ключа')
    plt.ylabel('Індекси сумісності')
    plt.show()

def get_I(text:str, alphabet:str = alphabet):
    letters_frequency = frequency(text, alphabet)
    denominator = len(text) * (len(text) - 1)
    if denominator == 0:
        return 0
    return sum([(letters_frequency[i] * (letters_frequency[i] - 1)) for i in letters_frequency]) / denominator

def get_keys_I(text:str, alphabet:str = alphabet):
    keys_ci = defaultdict(int)
    for r in range(2, len(alphabet)):
        text_parts = split_text(text, r)
        keys_ci[r] = sum([get_I(part) for part in text_parts])/len(text_parts)
    draw_graph(keys_ci)

def get_MI(frequency:dict, text:str):
    if len(text) == 0:
        return 0
    return sum([(val / len(text))**2 for val in frequency.values()])

def generate_string(length:int, characters:str):
    characters = ''.join(characters)
    return ''.join(choice(characters) for _ in range(length))

# plain_text = process_text("text.txt")
text_to_decrypt = process_text("task.txt")
# with open("edited_task.txt", "w", encoding="utf-8") as file:
#     file.write(text_to_decrypt)
# print(text)

# # шифрування
# encryption(plain_text, "оставьнадежду", "output_encrypted_test.txt")
# file = open("output_encrypted_test.txt", "rt", encoding='UTF-8')
# text_to_decrypt = file.read()
# decryption(text_to_decrypt, "оставьнадежду", "output_decrypted_test.txt")

# # індекс відповідності
# print(f'I = {get_I(plain_text)}')

# # математичне очікування
# print(f'MI = {get_MI(frequency(text), text)}')

# ключі
get_keys_I(text_to_decrypt)