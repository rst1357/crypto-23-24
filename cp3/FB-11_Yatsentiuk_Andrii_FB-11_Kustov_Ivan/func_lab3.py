from collections import Counter


letters = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
## ст но то ен ов
## [('еш', 67), ('еы', 49), ('шя', 47), ('ск', 47), ('до', 46)]


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
    return x % m if x < 0 else x



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
    if any(bigram in text for bigram in ['аы', 'аь', 'бй', 'вй', 'гй', 'гф', 'гх', 'дй', 'еы', 'еь', 'жй', 'жф', 'жх', 'жш', 'жщ', 'зй', 'зп', 'зщ', 'иь', 'йа', 'йж', 'йй', 'йь', 'кщ', 'кй', 'лй', 'мй', 'нй', 'оь', 'пв', 'пг', 'пж', 'пз', 'пй', 'сй', 'тй', 'уь', 'фб', 'фж', 'фз', 'фй', 'фп', 'фх', 'фц', 'фщ', 'хж', 'хй', 'хщ', 'хь', 'хю', 'хя', 'цб', 'цж', 'цй', 'цф', 'цх', 'цч', 'цщ', 'ць', 'цю', 'ця', 'чб', 'чг', 'чз', 'чй', 'чп', 'чф', 'чщ', 'чю', 'чя', 'шд', 'шж', 'шз', 'шй', 'шш', 'шщ', 'щб', 'щг', 'щд', 'щж', 'щз', 'щй', 'щл', 'щп', 'щт', 'щф', 'щх', 'щц', 'щч', 'щш', 'щщ', 'щю', 'щя', 'ьа', 'яй', 'ьл', 'ьу', 'ьь', 'юу', 'юь', 'яа', 'яо', 'яь']):  #if difference > 0.15 or
        return False
    else:
        return True

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

def find_most_frequent_pairs(input_string):
    pairs = [input_string[i:i + 2] for i in range(0, len(input_string) - 1, 2)]
    pair_counts = Counter(pairs)
    most_frequent_pairs = pair_counts.most_common(10)
    return most_frequent_pairs

def Find_Coef(Xarray, Yarray): ##accepts X-array [X1, X2] and Y-array [Y1, Y2]
    Y = Yarray[0]-Yarray[1]
    X = Xarray[0]-Xarray[1]
    m = 31**2
    a = (Y * pow(X,-1, m))  #mod_inverse replaced with pow(x,-1,z)
    b = (Yarray[0]-a*Xarray[0])%m
    return [a,b]

def SolveCoef(text):
    pairs_encoded = find_most_frequent_pairs(encoded_text)
    pairs = ["ст", "но", "то", "ен", "ов", "на", "не", "ра", "ли", "ни"]
    coef_array = []
    i = 0
    while i < len(pairs)-1:
        try:
            Yarray = [From_Bigram_To_Number(pairs_encoded[i][0]), From_Bigram_To_Number(pairs_encoded[i+1][0])]
            Xarray = [From_Bigram_To_Number(pairs[i]),From_Bigram_To_Number(pairs[i+1])]
            coef_array.append(Find_Coef(Xarray, Yarray))
        except:
            i = i + 1
            continue
        i = i + 1
    return coef_array


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


def Decode_bigram(bigram, coef_array):  #coef_array [a,b]
    m = 31**2
    decoded_number = (pow(coef_array[0], -1, m) * (From_Bigram_To_Number(bigram)-coef_array[1]))%m
    return From_Number_To_Bigram(decoded_number)



def Decode(text, coef_array):#coef_array [a,b]
    decoded_text = ""
    i = 0
    while i < len(text)-2:
        decoded_text = decoded_text + Decode_bigram(text[i:i+2], coef_array)
        i = i + 2
    return decoded_text


def BruteForce(text):  #coef_array [a,b]
    m = len(letters)**2

    i = 0
    while i < m:
        j = 0
        while j < m:
            try:
                #print(f"a:{i}, b{j}")
                if RussianCheck(Decode(text, [i,j])) is True:
                    print(f"Returned True with a:{i}, b:{j}")
                    j = j + 1
                    continue
                else:
                    j = j + 1
            except:
                j = j + 1

        i = i + 1


encoded_text = ReadText("04.txt", "utf-8")

BruteForce(encoded_text)



