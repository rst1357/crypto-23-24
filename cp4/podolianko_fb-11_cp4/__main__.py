import random
from rsa import *

A_keypair = GenerateKeyPair(256)
B_keypair = GenerateKeyPair(256)

while A_keypair[0][1] > B_keypair[0][1]:
    # regenerate the keys for them to be suitable for the key transfer protocol
    A_keypair = GenerateKeyPair(256)

print(
    f"""
A's keypair:
    Public: ({A_keypair[0][0]:#X},
        {A_keypair[0][1]:#X})
    Private: ({A_keypair[1][0]:#X},
        {A_keypair[1][1]:#X},
        {A_keypair[1][2]:#X})
    """
)

print(
    f"""
B's keypair:
    Public: ({B_keypair[0][0]:#X},
        {B_keypair[0][1]:#X})
    Private: ({B_keypair[1][0]:#X},
        {B_keypair[1][1]:#X},
        {B_keypair[1][2]:#X})
    """
)

message = random.randint(1, A_keypair[0][1] - 1)

for_a_encrypted_message = Encrypt(message, A_keypair[0])
by_a_signed_message = Sign(message, A_keypair[1])
for_a_decrypted_message = Decrypt(for_a_encrypted_message, A_keypair[1])

for_b_encrypted_message = Encrypt(message, B_keypair[0])
by_b_signed_message = Sign(message, B_keypair[1])
for_b_decrypted_message = Decrypt(for_b_encrypted_message, B_keypair[1])

# confidential key transfer protocol
k = random.randint(1, A_keypair[0][1] - 1)
a_protected_key_for_b = SendKey(k, A_keypair[1], B_keypair[0])
b_received_key_from_a = ReceiveKey(a_protected_key_for_b, B_keypair[1], A_keypair[0])

print(
    f"""
Message: {message: #x}
Encryption:
    B encrypts for A: {for_a_encrypted_message: #x}
    A encrypts for B: {for_b_encrypted_message: #x}

Decryption:
    Of message to A: {for_a_decrypted_message: #x}
    (result matched to original? {for_a_decrypted_message == message})

    Of message to B:{for_b_decrypted_message: #x}
    (result matched to original? {for_b_decrypted_message == message})
    
Signing and validating signatures (of the given message):
    A's signature: {by_a_signed_message[1]: #x}
        (verified? {Verify(by_a_signed_message, A_keypair[0])})
    B's signature: {by_b_signed_message[1]: #x}
        (verified? {Verify(by_b_signed_message, B_keypair[0])})
        
Simulating secure key transfer protocol
    Key to be sent: {k:#X}
    A -> B:
        (k1, S1): ({a_protected_key_for_b[0]:#X}, 
            {a_protected_key_for_b[1]:#X})
            
        B received (and verified) key: {b_received_key_from_a:#X}
    """
)

assert Verify(by_a_signed_message, A_keypair[0])
assert Verify(by_b_signed_message, B_keypair[0])
assert for_b_decrypted_message == message
assert for_a_decrypted_message == message
assert k == b_received_key_from_a
