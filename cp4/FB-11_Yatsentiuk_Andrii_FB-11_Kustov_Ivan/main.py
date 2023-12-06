import random
import secrets
def is_prime_miller_rabin(num, k=5):
    # Check for small numbers
    if num < 2:
        return False

    # Handle base cases
    if num == 2 or num == 3:
        return True

    # Check for even numbers (excluding 2)
    if num % 2 == 0:
        return False

    # Write num as 2^r * d + 1
    r, d = 0, num - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        # Choose a random base a in the range [2, num - 2]
        a = random.randint(2, num - 2)

        # Compute a^d % num
        x = pow(a, d, num)

        # Check if the result is 1 or num - 1
        if x == 1 or x == num - 1:
            continue  # Proceed to the next iteration

        # Repeat the square-and-multiply process r - 1 times
        for _ in range(r - 1):
            x = pow(x, 2, num)

            # If x becomes num - 1, it's not a witness
            if x == num - 1:
                break
        else:
            return False  # None of the bases were witnesses

    return True  # The number is probably prime


def GetPrime():
    random_number = secrets.randbits(512)
    while not is_prime_miller_rabin(random_number):
        random_number = secrets.randbits(512)
    return random_number
def _get_pq():
    num1 = GetPrime()
    num2 = GetPrime()
    return (num1, num2)

def get_pq():
    #a for p1 b for q2
    p, q = _get_pq()
    p1, q1 = _get_pq()
    while p * q > p1 * q1:
        p, q = get_pq()
        p1,q1 = get_pq()

    return [[p,q],[p1,q1]]



print(get_pq())



