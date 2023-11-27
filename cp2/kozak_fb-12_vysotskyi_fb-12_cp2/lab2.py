"""
9 варіант

https://en.wikipedia.org/wiki/Index_of_coincidence
"""

from re import sub
import random

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

path = "idiot.txt"

KEYS = ("а",
        "ха", "хм", "да",
        "чур", "хэй", "три", "мда",
        "влад", "макс", "клад", "пиво",
        "зорко", "абвгд", "бвгде", "смысл", "жалко",
        "скажипаляниця", "оченьдолгийключшифрования")

def read_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        file_content = f.read()
    return file_content

def clean_text(filepath):
    text = read_text(filepath)
    text = text.lower()
    text = sub("[^а-яё ]", " ", text)
    text = sub("\s+", "", text)
    return text

def save_text(filepath, text):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

#save_text("clean_text.txt", clean_text(path))

def count_letters(filepath):    # Підрахунок символів у тексті
    letter_dict = {}
    text = read_text(filepath)
    for letter in text:
        if letter in letter_dict:
            letter_dict[letter] += 1
        else:
            letter_dict[letter] = 1
    letter_dict = dict(sorted(letter_dict.items(), key=lambda x: x[1], reverse=True))
    return letter_dict

def vigenere_encrypt(text: str, key: str) -> str:
    cipher_text = ''
    key_index = 0

    for char in text:

        char_index = ALPHABET.index(char.lower())
        key_char = key[key_index % len(key)]
        key_index += 1

        cipher_char = ALPHABET[(char_index + ALPHABET.index(key_char.lower())) % len(ALPHABET)]
        cipher_text += cipher_char if char.islower() else cipher_char.upper()

    return cipher_text

def generate_key(length):
    key = ''.join(random.choice(ALPHABET) for _ in range(length))
    return key


def index_of_coincidence(text: str) -> float:
    index_value = 0
    for symbol in ALPHABET:
        letter_occurences = text.count(symbol)
        index_value += letter_occurences * (letter_occurences - 1)
    return index_value / len(text) / (len(text) - 1)


if __name__ == "__main__":
    open_text = read_text("clean_text.txt")
    encrypted_task = read_text("encrypted_task.txt")
    print(f"Відкритий текст. I_r={index_of_coincidence(open_text)}")
    print(f"Зашифрований текст (9 варіант)I_r={index_of_coincidence(encrypted_task)}")
    for key in KEYS:
        encrypted_text = vigenere_encrypt(open_text, key)
        # print(encrypted_text, end="\n\n\n")
        print(f"Шифротекст з ключем \"{key}\" (r={len(key)}). "
              f"I_r={index_of_coincidence(encrypted_text)}")
