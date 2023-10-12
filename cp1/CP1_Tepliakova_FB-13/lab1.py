import re
import numpy #поки не застосовувала 
from collections import Counter



def edit_textfile(input_file, output_file): #редактую текст віповідно до вимог
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    text = re.sub(r'[^a-zA-Zа-яА-Я\s\n]', ' ', text)
    text = text.lower()
    text = text.replace("ё", "е")
    text = text.replace("ъ", "ь")
    text = re.sub(r'\s+', ' ', text)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

input_file_path = "D:\crypto_github\crypto-23-24\cp1\CP1_Tepliakova_FB-13\Хоббіт.txt"
output_file_path = "D:\crypto_github\crypto-23-24\cp1\CP1_Tepliakova_FB-13\Форматований Хоббіт.txt"
     
edit_textfile(input_file_path, output_file_path)









