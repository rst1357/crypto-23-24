import math

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

def extended_euclid(a, n):
    if n == 0:
        return a, 1, 0
    gcd_res, x1, y1 = extended_euclid(n, a % n)
    x, y = y1, x1 - (a // n) * y1
    return gcd_res, x, y

def mod_inverse(a, n):
    if math.gcd(a, n) != 1:
        return None
    _, x, _ = extended_euclid(a, n)
    return x % n

def solve_congruence(a, b, n):
    gcd_res, x, _ = extended_euclid(a, n)
    if b % gcd_res != 0:
        return None

    solution = (x * (b // gcd_res)) % n
    solutions = [(solution + i * (n // gcd_res)) % n for i in range(gcd_res)]
    return solutions

def get_top_bigrams(text, gap=1):
    bigram_frequency = {}
    for i in range(len(text) - gap):
        bigram = text[i] + text[i + gap]
        if bigram not in bigram_frequency:
            bigram_frequency[bigram] = text.count(bigram)

    total = sum(bigram_frequency.values())
    freq_percent = {bigram: count / total for bigram, count in bigram_frequency.items()}
    sorted_bigrams = sorted(freq_percent.items(), key=lambda item: item[1], reverse=True)
    return [bigram for bigram, _ in sorted_bigrams[:5]]

def match_bigrams(expected_bigrams, observed_bigrams):
    bigram_matches = []
    for exp in expected_bigrams:
        for obs in observed_bigrams:
            if exp != obs:
                bigram_matches.append((exp, obs))
    return bigram_matches

def derive_keys(bigram_match):
    keys = []
    for b1, b2 in bigram_match:
        x1 = alphabet.index(b1[0]) * 31 + alphabet.index(b1[1])
        y1 = alphabet.index(b2[0]) * 31 + alphabet.index(b2[1])

        x2 = alphabet.index(b1[0]) * 31 + alphabet.index(b1[1])
        y2 = alphabet.index(b2[0]) * 31 + alphabet.index(b2[1])

        solutions = solve_congruence(x1 - x2, y1 - y2, 31 ** 2)
        if solutions:
            for sol in solutions:
                keys.append((sol, (y1 - sol * x1) % (31 ** 2)))
    return keys

def decipher_text(cipher, key_pair):
    plain_text = ""
    for i in range(0, len(cipher), 2):
        inv_key = mod_inverse(key_pair[0], 31 ** 2)
        if inv_key is None:
            return None

        y = alphabet.index(cipher[i]) * 31 + alphabet.index(cipher[i + 1])
        x = (inv_key * (y - key_pair[1])) % (31 ** 2)
        plain_text += alphabet[x // 31] + alphabet[x % 31]
    return plain_text

def attempt_decryption(ciphered_text, key_list):
    forbidden_bigrams = {'аы', 'оы', 'иы', 'ыы', 'уы', 'еы', 'аь', 'оь', 'иь', 'ыь', 'уь', 'еь', 'юы', 'яы',
                         'эы', 'юь', 'яь', 'эь', 'ць', 'хь', 'кь', 'ьь', 'йй', 'йь', 'йы', 'ыю'}
    for key in key_list:
        decrypted = decipher_text(ciphered_text, key)
        if decrypted and not any(bigram in decrypted for bigram in forbidden_bigrams):
            print(f'Decryption Key: {key}')
            with open("decrypted.txt", 'w', encoding='utf-8') as output_file:
                output_file.write(decrypted)
            return

with open('07.txt', 'r', encoding='utf-8') as file:
    cipher_text = file.read().replace('\n', '')

common_bigrams = ['ст', 'но', 'то', 'на', 'ен']
observed_bigrams = get_top_bigrams(cipher_text)
print(f'Top 5 bigrams in encrypted text: {observed_bigrams}')

bigram_matches = match_bigrams(common_bigrams, observed_bigrams)
key_options = derive_keys(bigram_matches)
attempt_decryption(cipher_text, key_options)
