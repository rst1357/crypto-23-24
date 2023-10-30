from collections import Counter

with open('04.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()

letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
bigrams = [letters[i] + letters[j] for i in range(len(letters)) for j in range(len(letters))]

bigram_counts = Counter()
for bigram in bigrams:
    bigram_count = file_contents.count(bigram)
    bigram_counts[bigram] = bigram_count

# Get the 5 most common bigrams
most_common_bigrams = bigram_counts.most_common(5)

for bigram, count in most_common_bigrams:
    print(f"'{bigram}',  '{count}'")





