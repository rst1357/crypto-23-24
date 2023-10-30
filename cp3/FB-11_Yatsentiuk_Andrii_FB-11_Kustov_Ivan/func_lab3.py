letters = 'абвгдежзийклмнопрстуфхцчшщыьэюя'


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



def Encode_Athene(a,b,letter,letters):
    m = len(letters)
    x = letters.find(letter)
    index = (a*x+b)%m
    return letters[index]


def Decode_Athene(a,b,letter,letters):
    m = len(letters)
    x = letters.find(letter)
    index = (mod_inverse(a,m))*(x-b)%m
    return letters[index]