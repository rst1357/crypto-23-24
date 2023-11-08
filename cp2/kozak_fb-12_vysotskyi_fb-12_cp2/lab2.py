from re import sub

path = "idiot.txt"

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

def vigenere_cipher(text: str, key: str) -> str:
    alphabet = {
        'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
        'en': 'abcdefghijklmnopqrstuvwxyz'
    }

    lang = "ru"
    cipher_text = ''
    key_index = 0

    for char in text:

        char_index = alphabet[lang].index(char.lower())
        key_char = key[key_index % len(key)]
        key_index += 1

        cipher_char = alphabet[lang][(char_index + alphabet[lang].index(key_char.lower())) % len(alphabet[lang])]
        cipher_text += cipher_char if char.islower() else cipher_char.upper()

    return cipher_text

