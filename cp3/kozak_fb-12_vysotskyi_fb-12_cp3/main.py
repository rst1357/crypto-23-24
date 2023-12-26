from re import sub

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

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

#save_text("encrypted_text.txt", clean_text("09_utf.txt"))

def count_bigrams(filepath, step=1):    # Підрахунок біграм з різним кроком
    text = read_text(filepath)
    bigram_dict = {}
    for i in range(0, len(text) - 1, step):
        bigram = text[i:i+2].replace(" ", "_")
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    bigram_dict = dict(sorted(bigram_dict.items(), key=lambda x: x[1], reverse=True))  # Сортування за значеннями ключів
    return bigram_dict

def extended_euclid(a, b):   # Розширений алгоритм Евкліда
    """ Повертає d=НСД(x,y) і x, y такі, що ax + by = d """
    if b == 0:
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y

def mod_inverse(a, m):   # Обернене за модулем
    gcd, x, y = extended_euclid(a, m)
    if gcd != 1:
        raise ValueError(f"Оберненого за модулем {m} не існує для {a}")
    if gcd == 1:
        return (x % m + m) % m

def solve_linear_congruence(a, b, mod_n):
    """ ax ≡ b (mod n) """
    inverse_a = mod_inverse(a, mod_n)
    x = (inverse_a * b) % mod_n
    return x

