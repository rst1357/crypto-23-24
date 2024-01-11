import re
from math import log2
import xlsxwriter

alphabet_with_spaces = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя '
alphabet_without_spaces = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'


def prettify_text(text_path, include_spaces):
    file = open(text_path, encoding='utf-8')
    text_file = file.read()
    file.close()
    text_file = re.sub(r'[^а-яА-Я ]', '', text_file).lower()
    while text_file.count('  '):
        text_file = text_file.replace('  ', ' ')
    if not include_spaces:
        text_file = re.sub(' ', '', text_file)
    text_file = str(text_file)

    return text_file


def count_letter_in_text(letter, text):
    counter = 0
    for l in text:
        if l == letter:
            counter += 1
    return counter


def count_letters_frequency(alphabet, text):
    letters_frequency_dict = {}
    text_length = len(text)
    for letter in alphabet:
        letter_frequency = count_letter_in_text(letter, text) / text_length
        letters_frequency_dict[letter] = round(letter_frequency, 10)
    return letters_frequency_dict


def create_bigrams(alphabet):
    bigrams_dict = {}
    for l_1 in alphabet:
        for l_2 in alphabet:
            bigram = l_1 + l_2
            bigrams_dict[bigram] = 0
    return bigrams_dict


def count_bigram_frequency(text, crossed, bigrams_frequency_dict):
    frequency = {}
    text_length = len(text)
    if crossed == 'Y':
        for i in range(len(text)-1):
            key = text[i] + text[i+1]
            bigrams_frequency_dict[key] += 1
        for key in bigrams_frequency_dict.keys():
            frequency[key] = bigrams_frequency_dict[key] / (len(text) - 1)
            frequency[key] = round(frequency[key], 8)
    else: # not crossed
        if len(text) % 2 == 1:
            text_length -= 1
        for i in range(len(text)-1):
            if i % 2 == 1:
                continue
            key = text[i] + text[i+1]
            bigrams_frequency_dict[key] += 1
        for key in bigrams_frequency_dict.keys():
            frequency[key] = bigrams_frequency_dict[key] / (text_length // 2)
            frequency[key] = round(frequency[key], 8)
    return frequency


def calculate_entropy(frequency_dict, n):
    entropy = []
    for bigram in frequency_dict.keys():
        f = frequency_dict[bigram]
        if f != 0:
            bigram_entropy = abs(float(f) * log2(f)/n)
            entropy.append(bigram_entropy)
    e = sum(entropy)
    return e


def calculate_redundancy(alphabet, entropy):
    return 1 - (entropy / log2(len(alphabet)))


def make_excel_table(dict, table_name):
    table = xlsxwriter.Workbook(table_name)
    excel_table = table.add_worksheet()
    keys = list(dict.keys())
    values = list(dict.values())
    for k in range(1, len(keys)+1):
        excel_table.write(k-1, 0, keys[k - 1])
        excel_table.write(k-1, 1, values[k - 1])
    table.close()


text_with_spaces = prettify_text('text.txt', True)
text_without_spaces = prettify_text('text.txt', False)

# letters including space
letters_frequency_with_space = count_letters_frequency(alphabet_with_spaces, text_with_spaces)
letters_E_with_space = calculate_entropy(letters_frequency_with_space, 1)
letters_R_with_space = calculate_redundancy(alphabet_with_spaces, letters_E_with_space)
print('letters with space: E = ', letters_E_with_space, ', R = ', letters_R_with_space)
make_excel_table(letters_frequency_with_space, 'letters_frequency_with_space.xlsx')
# letters not including space
letters_frequency_without_space = count_letters_frequency(alphabet_without_spaces, text_without_spaces)
letters_E_without_space = calculate_entropy(letters_frequency_without_space, 1)
letters_R_without_space = calculate_redundancy(alphabet_without_spaces, letters_E_without_space)
print('letters without space: E = ', letters_E_without_space, ', R = ', letters_R_without_space)
make_excel_table(letters_frequency_without_space, 'letters_frequency_without_space.xlsx')

# bigrams including spaces
# not crossed
bigram_frequency_with_space = count_bigram_frequency(text_with_spaces, 'N', create_bigrams(alphabet_with_spaces))
bigram_frequency_with_space_E = calculate_entropy(bigram_frequency_with_space, 2)
bigram_frequency_with_space_R = calculate_redundancy(alphabet_with_spaces, bigram_frequency_with_space_E)
print('not crossed bigram with space: E = ', bigram_frequency_with_space_E, ', R = ', bigram_frequency_with_space_R)
make_excel_table(bigram_frequency_with_space, 'bigram_frequency_with_space.xlsx')
# crossed
crossed_bigram_frequency_with_space = count_bigram_frequency(text_with_spaces, 'Y', create_bigrams(alphabet_with_spaces))
crossed_bigram_frequency_with_space_E = calculate_entropy(crossed_bigram_frequency_with_space, 2)
crossed_bigram_frequency_with_space_R = calculate_redundancy(alphabet_with_spaces, crossed_bigram_frequency_with_space_E)
print('crossed bigram with space: E = ', crossed_bigram_frequency_with_space_E, ', R = ', crossed_bigram_frequency_with_space_R)
make_excel_table(crossed_bigram_frequency_with_space, 'crossed_bigram_frequency_with_space.xlsx')

# bigrams not including spaces
# not crossed
bigram_frequency_without_space = count_bigram_frequency(text_without_spaces, 'N', create_bigrams(alphabet_without_spaces))
bigram_frequency_without_space_E = calculate_entropy(bigram_frequency_without_space, 2)
bigram_frequency_without_space_R = calculate_redundancy(alphabet_without_spaces, bigram_frequency_without_space_E)
print('not crossed bigram with space: E = ', bigram_frequency_without_space_E, ', R = ', bigram_frequency_without_space_R)
make_excel_table(bigram_frequency_without_space, 'bigram_frequency_without_space.xlsx')
# crossed 
crossed_bigram_frequency_without_space = count_bigram_frequency(text_without_spaces, 'Y', create_bigrams(alphabet_without_spaces))
crossed_bigram_frequency_without_space_E = calculate_entropy(crossed_bigram_frequency_without_space, 2)
crossed_bigram_frequency_without_space_R = calculate_redundancy(alphabet_without_spaces, crossed_bigram_frequency_without_space_E)
print('crossed bigram with space: E = ', crossed_bigram_frequency_without_space_E, ', R = ', crossed_bigram_frequency_without_space_R)
make_excel_table(crossed_bigram_frequency_without_space, 'crossed_bigram_frequency_without_space.xlsx')
