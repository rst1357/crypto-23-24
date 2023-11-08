letters = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
array = ['ешст', 'шяно', 'еыто', 'зоов'] # ШТ + ВТ   # 1 2 4 5


def extended_euclid(a, b):
    if (b == 0):
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y
    #повертає НСД(0) х(1) у(2) у вигляді кортежу

def mod_inverse(a, m):
    d, x, y = extended_euclid(a, m)
    if d != 1:
        raise ValueError("Оберненого за модулем числа не існує")
    return x % m



def CountFreq(letter, text):
    len_text = len(text)
    freq = text.count(letter)/len_text
    return freq

def RussianCheck(text):  #works good only with large texts
    alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
    alphabet_letter_frequencies = [
        0.0801, 0.0159, 0.0454, 0.0165, 0.0298, 0.0849, 0.0072, 0.016, 0.0735,
        0.0106, 0.0321, 0.0497, 0.0333, 0.067, 0.1097, 0.0281, 0.0473, 0.0547, 0.0626,
        0.0262, 0.0026, 0.0097, 0.0048, 0.0144, 0.0073, 0.0061, 0.019, 0.0178,
        0.0032, 0.0064, 0.0201
    ]

    freq = []
    i = 0
    while i < len(alphabet):
        freq.append(CountFreq(alphabet[i],text))
        i = i + 1

    difference = 0
    i = 0
    while i < len(alphabet_letter_frequencies):
        difference = difference + abs(alphabet_letter_frequencies[i] - freq[i])
        i = i + 1
    if difference < 0.15:
        return True
    else:
        return False

def From_Number_To_Bigram(num):
    m = 31
    # X = x1*m +x2    66
    x1 = 0
    while (num-m*x1) > m:
        x1 += 1

    x2 = num - x1*m
    #print(f"num: {num}")
    #print(f"x1: {x1}")
    #print(f"x2: {x2}")
    string = letters[x1] + letters[x2]
    return string

def From_Bigram_To_Number(bigram):
    # X = x1*m + x2
    m = 31
    x1 = letters.find(bigram[0])
    x2 = letters.find(bigram[1])
    return x1*m + x2

def ReadText(filename, encoding):
    with open(filename, 'r', encoding=encoding) as file:
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
    return file_contents


def Solve(array):
    m = 31
    m = m^2

    X1 = array[1][2:]
    X2 = array[3][2:]
    Y1 = array[1][:2]
    Y2 = array[3][:2]

    X1 = From_Bigram_To_Number(X1)
    X2 = From_Bigram_To_Number(X2)
    Y1 = From_Bigram_To_Number(Y1)
    Y2 = From_Bigram_To_Number(Y2)

    X = X1 - X2
    Y = Y1 - Y2

    if extended_euclid(X,m)[0] == 1:
        INV_X = mod_inverse(X, m)
        a = (Y * INV_X) % m
        b = (Y1 - a * X1) % m
        return [a,b]
    else:
        return "SMTHWW"

def Decode(array, string):
    m = 31
    m = m^2
    a = array[0]
    b = array[1]
    Y = From_Bigram_To_Number(string)
    X = (mod_inverse(a, m) * (Y - b)) % m
    #print(X)
    return From_Number_To_Bigram(X)


#print(From_Number_To_Bigram(66))
print(Decode(Solve(array), 'ст'))


