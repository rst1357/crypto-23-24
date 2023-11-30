import collections
from numpy import inf







def GetProbability(Filename, Alphabet):
    File = open(Filename, "r")
    RawText = File.read().lower()
    RawText = RawText.replace('ё','е')
    RawText = RawText.replace('ъ','ь')

    TextList = [i for i in RawText if i in Alphabet]

    LetterCount = collections.Counter(TextList)
    TotalAmount = 0
    for i in LetterCount.values():
        TotalAmount += i
    print(f"Total letters: {TotalAmount}")

    LetterProbablilty =  {}
    for i in LetterCount.keys():
        LetterProbablilty[i] = LetterCount[i]/TotalAmount
    return LetterProbablilty




def vigenere_encrypt(filename, out_filename, cypher, alphabet, print_out=True, write_file = False):
    with open(filename, "r") as file:
        cleartext = file.read().lower()
    cleartext = [i for i in cleartext if i in alphabet]
    file_len = len(cleartext)
    cypher_len = len(cypher)
    adj_cypher = cypher*((file_len // cypher_len) + 1)


    cyphertext = ""
    for i in range(file_len):
        cyphertext += alphabet[(alphabet.index(cleartext[i])  + alphabet.index(adj_cypher[i])) % len(alphabet)]

    if print_out == True:
        print(cyphertext)

    if write_file == True:
        with open(out_filename, "w") as file:
            file.write(cyphertext)
    return cyphertext

def compliance_index(text, alphabet):
    text_len = len(text)
    letter_count = {}
    for i in alphabet:
        letter_count[i] = text.count(i)

    compliance_index_value = 0
    for i in letter_count.keys():
        compliance_index_value += letter_count[i]*(letter_count[i] - 1)
    compliance_index_value = compliance_index_value / (text_len * (text_len - 1))
    return compliance_index_value


def split_text(text, step):
    return_array = []
    for i in range(step):
        return_array.append(text[i::step])
    return return_array

def kron_delta(a, b):
    return int(a==b)

def find_D(text, alphabet, step):
    D = 0
    for i in range(len(text) - step):
        D += kron_delta(alphabet.index(text[i]), alphabet.index(text[i + step]))
    return D

def get_vigenere_prob(cyphertext, alphabet, step, letter_count):
    letter_count = dict(sorted(letter_count.items(), key = lambda x: x[1], reverse = True))
    key = []
    splitted_text = split_text(cyphertext, step)
    cyphertext_letter_count = {}
    popular_letter = alphabet[0]
    popular_letters = []

    for part in splitted_text:
        for letter in alphabet:
            cyphertext_letter_count[letter] = part.count(letter)


        for i in cyphertext_letter_count.keys():
            if cyphertext_letter_count[i] > cyphertext_letter_count[popular_letter]:
                popular_letter = i
        cyphertext_letter_count = dict(sorted(cyphertext_letter_count.items(), key = lambda x: x[1], reverse=True))
        popular_letters.append(cyphertext_letter_count)
        key.append(alphabet[(alphabet.index(popular_letter) - alphabet.index('о')) % (len(alphabet) )])


    return popular_letters


def get_vigenere_key(cleartext_letter_prob, cyphertext_letter_prob, alphabet):


    key = ""

    for i in cyphertext_letter_prob:
        key += alphabet[(alphabet.index(list(i.keys())[0]) - alphabet.index('о')) % len(alphabet)]


    print("looks like your key is: ")

    for i in key:
        print(i.ljust(3, " "), end="")
    print("")
    for i in range(len(key)):
        print(str(i).ljust(3, " "), end="")
    print("")
    key = [ i for i in key]
    backup_key = key
    print("to return to backup key enter 'b'")

    while 1:
        choise = input("to change letter enter its index, to exit enter '-': ")
        if choise == "-":
            break
        if choise == 'b':
            key = backup_key
            continue

        choise_index = input("enter new index: ")
        key[int(choise)] = alphabet[( alphabet.index( list(cyphertext_letter_prob[int(choise)].keys())[int(choise_index)]) - alphabet.index('о') ) % len(alphabet)]

        for i in key:
            print(i.ljust(3, " "), end="")
        print("")
        for i in range(len(key)):
            print(str(i).ljust(3, " "), end="")
        print("")


    return key


def decrypt_vigenere(cyphertext, alphabet, key):
    cleartext = ""

    key_adj = key * (len(cyphertext) // len(key) + 1)

    for i in range(len(cyphertext)):
        cleartext += alphabet[ alphabet.index(cyphertext[i]) - alphabet.index(key_adj[i]) %  (len(alphabet))]
    print(cleartext)
    return cleartext


def main():
    alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', 'ъ']
    filename = "cleartext.txt"
    key2 = "из"
    key3 = "воз"
    key4 = "раст"
    key5 = "еряша"
    key_big = "чашкаиложкаичай"
    key_big_big = "оченьнеимовернобольшойключ"
    cyphertext = vigenere_encrypt(filename, "test", key_big_big, alphabet, print_out=False)
    print(compliance_index(cyphertext, alphabet))
    with open(filename, "r") as file:
        text = file.read()


    text = [i for i in text if i in alphabet]
    text=  "".join(text)
    print("real compl: ",compliance_index(text, alphabet))
    key2_splitted = split_text(cyphertext, 2)
    print(compliance_index(key2_splitted[1], alphabet))


    letter_probability = GetProbability(filename, alphabet)



    with open("cypher.txt", "r") as file:
        work_text = file.read()


    work_text = [i for i in work_text if i in alphabet]

    choise =  ""
    while choise != "-":
        testshit = get_vigenere_prob(work_text, alphabet, 14, letter_probability)
        key = get_vigenere_key(letter_probability, testshit, alphabet)
        choise = input("to print small part of text enter p, to continue enter c, to exit enter -: ")
        if choise == "p":
            decrypt_vigenere(work_text[:len(key)], alphabet, key)
        if choise == "c":
            continue

    step = 14
    prob_step = 28

    return
 







if __name__ == "__main__":
    main()
