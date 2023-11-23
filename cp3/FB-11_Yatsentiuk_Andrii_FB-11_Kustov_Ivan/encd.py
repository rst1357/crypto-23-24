with open("to_encd.txt", 'r', encoding='utf-8') as file:

    file_contents = file.read()
    file_contents = file_contents.lower()
    file_contents = file_contents.replace(",", "")
    file_contents = file_contents.replace("!", "")
    file_contents = file_contents.replace("?", "")
    file_contents = file_contents.replace("=", "")
    file_contents = file_contents.replace("-", "")
    file_contents = file_contents.replace("", "")
    file_contents = file_contents.replace(".", "")
    file_contents = file_contents.replace(":", "")
    file_contents = file_contents.replace(";", "")
    file_contents = file_contents.replace("1", "")
    file_contents = file_contents.replace("2", "")
    file_contents = file_contents.replace("3", "")
    file_contents = file_contents.replace("4", "")
    file_contents = file_contents.replace("5", "")
    file_contents = file_contents.replace("6", "")
    file_contents = file_contents.replace("7", "")
    file_contents = file_contents.replace("8", "")
    file_contents = file_contents.replace("9", "")
    file_contents = file_contents.replace("0", "")
    file_contents = file_contents.replace(" ", "")
    file_contents = file_contents.replace("'", "")
    file_contents = file_contents.replace("\n", "")
    file_contents = file_contents.replace("ъ", "ь")
    file_contents = file_contents.replace("ё", "е")
    file_contents = file_contents.replace("«", "")
    file_contents = file_contents.replace("»", "")
    file_contents = file_contents.replace("…","")
    file_contents = file_contents.replace("„", "")
    file_contents = file_contents.replace("“", "")
    file_contents = file_contents.replace("—", "")
    file_contents = file_contents.replace("*", "")

letters = 'абвгдежзийклмнопрстуфхцчшщыьэюя'

def From_Number_To_Bigram(num):
    m = 31
    # num = x1*m +x2    66
    x1 = 0
    while (num-m*x1) >= m:
        x1 += 1

    x2 = num - x1*m

    #print([num,x1,x2])
    string = letters[x1] + letters[x2]
    return string

def From_Bigram_To_Number(bigram):
    # X = x1*m + x2
    m = 31
    x1 = letters.find(bigram[0])
    x2 = letters.find(bigram[1])
    return x1*m + x2


def encode(text, a, b):
    ciphertext = ""
    i = 0
    while i < len(text)-2:
        bigram = text[i:i + 2]
        num = From_Bigram_To_Number(bigram)
        encoded_num = (a * num + b) % (len(letters) ** 2)
        encoded_bigram = From_Number_To_Bigram(encoded_num)
        ciphertext += encoded_bigram
        i = i+2

    return ciphertext


print(encode(file_contents, 5, 8))

# Open a file in write mode ('w')
with open('encoded.txt', 'w') as file:
    # Write content to the file
    file.write(encode(file_contents, 5, 8))











