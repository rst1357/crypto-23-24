from random import randrange


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def trialDiv(p: int) -> bool:
    for d in [2, 5, 7, 11, 13]:
        if p % d == 0:
            return False
        
    return True


def MillerRabin(p: int, k: int) -> bool:
    s, d = 0, p - 1
    while d % 2 == 0:
        d //= 2; s += 1

    x_old = 0
    for _ in range(k):
        isStrongPseudoprime = False
        x = randrange(2, p, 1)
        while x == x_old:
            x = randrange(2, p, 1)
        x_old = x

        if gcd(x, p) > 1:
            return False
        
        if (xd := pow(x, d, p)) == 1 or xd == p - 1:
            continue
        else:
            for _ in range(1, s):
                if (xd := pow(xd, 2, p)) == p - 1:
                    isStrongPseudoprime = True
                    break
                elif xd == 1:
                    return False
            
            if isStrongPseudoprime == False:
                return False
            
    return True


def generatePrime(length: int):
    while True:
        n = 2 ** length
        x = randrange(n, 2*n - 2)
        m0 = x if x % 2 != 0 else x + 1

        for i in range(0, int((2*n - 2 - m0)/2)):
            if not trialDiv(m0 + 2*i):
                continue

            if MillerRabin(m0 + 2*i, 20):
                return m0 + 2*i
            