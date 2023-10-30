import math

with open('04.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()

print(file_contents)


def CountBigram(bigram, text):
    i = 2
    counter = 0
    pointer = 0
    while i<len(text):
        if text[pointer:i] == bigram:
            counter = counter + 1
        pointer = i
        i = i + 2
    return counter

letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
global_letter_count = 0
for char in file_contents:
    # Check if the current character is an alphabetic character
    if char.isalpha():
        global_letter_count += 1

bigrams = [letters[i] + letters[j] for i in range(len(letters)) for j in range(len(letters))]
global_bigram_count = 0
global_bigram_entropy = 0
global_bigram_ni_count = len(file_contents)/2
global_bigram_ni_entropy = 0
for bigram in bigrams:
    bigram_count = file_contents.count(bigram)
    bigram_ni_count = CountBigram(bigram, file_contents)
    if bigram_count > 0:  # Check if bigram_count is greater than zero
        bigram_frequency = bigram_count / global_bigram_count
        global_bigram_entropy += (bigram_frequency * math.log2(bigram_frequency))/2
        print(f"Біграмма з перетином'{bigram}': {bigram_frequency}")
    if bigram_ni_count > 0:
        bigram_frequency_ni = bigram_ni_count / global_bigram_ni_count
        global_bigram_ni_entropy += (bigram_frequency_ni * math.log2(bigram_frequency_ni)) / 2
        print(f"Біграмма без перетину' {bigram}': {bigram_frequency_ni}")

print(f"Ентропія біграм: {global_bigram_entropy * -1}")
print(f"Ентропія біграм без перетину: {global_bigram_ni_entropy * -1}")




