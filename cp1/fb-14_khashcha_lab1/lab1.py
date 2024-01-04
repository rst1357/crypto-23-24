import math
import pandas as pd
from re import sub
import numpy as np


def load_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def clean_text(input_text):
    lower_text = input_text.lower()
    cleaned_text = sub("[^а-я]", " ", lower_text)
    cleaned_text = sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text.replace("ъ", "ь").replace("ё", "е")

def calculate_letter_freq(clean_text, include_space=True):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя' + (' ' if include_space else '')
    freq = {letter: clean_text.count(letter) / len(clean_text) for letter in alphabet}
    sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
    print("\n".join([f' "{k}"   -->   {v}' for k, v in sorted_freq.items()]))
    return freq

def entropy_redundancy(freq, include_space):
    entropy = -sum(p * math.log2(p) for p in freq.values() if p > 0)
    print(f"Entropy H.1 = {entropy}")
    base = math.log2(32) if include_space else math.log2(31)
    redundancy = 1 - (entropy / base)
    print(f"Redundancy R.1 = {redundancy}\n")

def bigram_analysis(text, cross=True, include_spaces=True):
    if not include_spaces:
        text = text.replace(' ', '')
    bigrams = [text[i:i+2] for i in range(len(text) - (1 if cross else 2))]
    if not cross:
        bigrams = bigrams[::2]

    freq = {bg: bigrams.count(bg) / len(bigrams) for bg in set(bigrams) if len(bg) == 2}
    freq = {k: round(v, 10) for k, v in freq.items()}

    alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя' + (' ' if include_spaces else '')
    df = pd.DataFrame(np.zeros((len(alphabet), len(alphabet))), index=list(alphabet), columns=list(alphabet), dtype=float)
    for (c1, c2), f in freq.items():
        df.at[c1, c2] = f

    fname = f"bigram_table_{'cross' if cross else 'not_cross'}_{'spaces' if include_spaces else 'not_spaces'}.xlsx"
    df.to_excel(fname)

    entropy = -sum(p * math.log2(p) for p in freq.values() if p > 0) / 2
    print(f"Entropy H.2 = {entropy}")
    base = math.log2(len(alphabet))
    redundancy = 1 - (entropy / base)
    print(f"Redundancy R.2 = {redundancy}\n")

def process_file(file_path):
    text = load_text(file_path)
    cleaned_text = clean_text(text)

    freq_with_space = calculate_letter_freq(cleaned_text)
    entropy_redundancy(freq_with_space, True)
    bigram_analysis(cleaned_text)
    bigram_analysis(cleaned_text, cross=False)

    freq_without_space = calculate_letter_freq(cleaned_text, False)
    entropy_redundancy(freq_without_space, False)
    bigram_analysis(cleaned_text, include_spaces=False)
    bigram_analysis(cleaned_text, cross=False, include_spaces=False)

if __name__ == '__main__':
    file_path = 'text_f.txt'
    process_file(file_path)
