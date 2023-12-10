import secrets
import random
from math import gcd

def miller_rabin_test(p: int, k: int = 10) -> bool:
    # 0
    # p - 1 = d * 2**s
    s = 0; d = p - 1
    while d & 1 == 0: s+=1; d = d >> 1
    assert 2**s * d == p - 1, "?!"

    counter = 0

    is_spp = False
    while counter < k:
        # 1
        x = random.randint(2, p-1)
        if gcd(x, p) > 1:
            return False
        # 2 2.1
        c2_1 = pow(x, d, p)
        if c2_1 == -1 % p or c2_1 == 1:
            is_spp = True
        else:
            # 2.2
            r = 1
            xr = pow(x, d * 2, p)
            while True:
                if xr == -1 % p:
                    is_spp = True
                    break
                elif xr == 1:
                    is_spp = False
                    break
                else: pass

                r += 1
                if r > s-1:
                    break
                xr = pow(xr, 2, p)
        # 2.3
        if not is_spp:
            return False
        else:
            counter += 1
        # 3 (loop)

    return is_spp

def is_prime(p: int) -> bool:
    for q in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107]:
        if p != q and p % q == 0: return False

    return miller_rabin_test(p)

def get_prime(bits: int) -> int:
    while True:
        p = secrets.randbits(bits)
        if is_prime(p): return p
