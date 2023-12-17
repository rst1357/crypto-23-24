import random
import secrets
import math
import string
import hashlib



def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

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
    return [num1, num2]

def get_pq():
    #a for p1 b for q2
    pq = _get_pq()
    p = pq[0]
    q = pq[1]
    pq1 = _get_pq()
    p1 = pq1[0]
    q1 = pq1[1]
    while p * q > p1 * q1:
        pq = _get_pq()
        p = pq[0]
        q = pq[1]
        pq1 = _get_pq()
        p1 = pq1[0]
        q1 = pq1[1]

    return [[p,q],[p1,q1]]


def generate_e(n):
    while True:
        candidate = random.randint(2, n-1)
        if math.gcd(n, candidate) == 1:
            return candidate

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def generate_d(p, q, e):
    phi_n = (p - 1) * (q - 1)
    d = modinv(e, phi_n)
    return d

def Generate_Keys():
    PQ_array = get_pq()
    e1 = generate_e((PQ_array[0][0]-1)*(PQ_array[0][1]-1))
    e2 = generate_e((PQ_array[1][0] - 1) * (PQ_array[1][1] - 1))
    d1 = generate_d(PQ_array[0][0], PQ_array[0][1], e1)
    d2 = generate_d(PQ_array[1][0], PQ_array[1][1], e2)
    n1 = PQ_array[0][0] * PQ_array[0][1]
    n2 = PQ_array[1][0] * PQ_array[1][1]
    return [[e1,n1,d1],[e2,n2,d2]]

def Encrypt(message, n, e): # n and e are public keys. Message will be a string without numbers. (n = p*q, e is coprime of (p-1)*(q-1))
    numbers = [ord(char) for char in message]
    message = ""
    temp = ""
    for num in numbers:
        if len(str(num)) == 2:
            temp = "0" + str(num)
            message = message + temp
        else:
            temp = str(num)
            message = message + temp
    message = str(random.randint(1,9)) + message # to make possible 0XX code at first pos, delete first number when decode
    encoded_message = pow(int(message), e, n)
    return encoded_message

def Decrypt(message, n, d):
    decoded_message_num = pow(message, d, n)
    decoded_message_num_without_first = str(decoded_message_num)[1:]
    decoded_message = ""
    i = 0
    while i < len(decoded_message_num_without_first) and decoded_message_num_without_first[i:i+3] != '':
        batch = int(decoded_message_num_without_first[i:i+3])
        char = chr(batch)
        decoded_message = decoded_message + char
        i = i + 3

    return decoded_message

#signatures
def generate_signature(data, your_signature):
    return hashlib.sha256((data + your_signature).encode()).digest() #generates a hash out of a string

def encrypt_signature(signature, n1, e1):
    hex_string = ''.join(['{:02X}'.format(byte) for byte in signature])
    return Encrypt(hex_string, n1, e1)

def check_signature(encrypted_signature, encrypted_text, n1, d1, your_signature):
    signature =  bytes.fromhex(Decrypt(encrypted_signature, n1, d1))
    return signature == generate_signature(Decrypt(encrypted_text, n1, d1), your_signature)





#sender side

keys = Generate_Keys()
e1 = keys[0][0] #public key
n1 = keys[0][1] #public key
d1 = keys[0][2] #private key
message = "Hello world, that's my real RSA encrypted message!"
signature_string = "MY_SIGNATURE"
encrypted = Encrypt(message, n1, e1)
signature = generate_signature(message, signature_string)
encrypted_signature = encrypt_signature(signature, n1, e1)
#signature + encrypted is getting sent

#recipient side
#key is already known
decrypted = Decrypt(encrypted, n1, d1)
if check_signature(encrypted_signature, encrypted, n1, d1, "MY_SIGNATURE"):
    print("Signature is verified. Message is valid.")
    print(f"Message {decrypted}")
    print(f"Signature : {signature_string}")
    print(f"Public keys :")
    print(f"n: {n1}")
    print(f"e: {e1}")
    print(f"Private key : d: {d1}")

else:
    print("SOMEONE CHANGED THE MESSAGE!!!! SIGNATURE IS NOT VERIFIED!!!!")





