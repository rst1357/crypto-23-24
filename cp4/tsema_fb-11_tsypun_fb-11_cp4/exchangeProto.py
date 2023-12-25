from RSA import *


class ExchangeProtocol:
    def __init__(self, Alice: RSA, Bob: RSA) -> None:
        self.Alice = Alice
        self.Bob = Bob


    def startExchange(self) -> None:
        self.Alice.generateKeyPair()
        self.Bob.generateKeyPair()

        while not self._isPossibleToExchange(self.Alice, self.Bob):
            self.Alice.generateKeyPair()

        print(f"[*] {self.Alice.name} and {self.Bob.name} can communicate now\n")

    
    def _isPossibleToExchange(self, sender: RSA, recipient: RSA) -> bool:
        return sender.n <= recipient.n
    
    
    def sendKey(self, pubKey: tuple[int, int], sender: RSA, recipient: RSA, k: int) -> tuple[int, int]:
        if not self._isPossibleToExchange(sender, recipient):
            print(f"[-] {sender.name} can\'t send key to {recipient.name}\n")
            return
        
        signature = sender.sign(k)
        print(f"[*] {sender.name} signed the key: {signature}\n")
        encrypted = sender.encrypt(signature[0], pubKey), sender.encrypt(signature[1], pubKey)
        print(f"[*] {sender.name} sent key to {recipient.name}: {encrypted}\n")
        return encrypted


    def receiveKey(self, pubKey: tuple[int, int], sender: RSA, recipient: RSA, enc_k: tuple[int, int]) -> tuple[int, bool]:
        print(f"[*] {recipient.name} received key from {sender.name}: {enc_k}\n")
        decrypted = recipient.decrypt(enc_k[0]), recipient.decrypt(enc_k[1])
        print(f"[*] Decrypted key: {decrypted}\n"); isVer = recipient.verify(decrypted, pubKey)
        print(f"[*] Signature verification: {isVer}\n")

        return decrypted[0], isVer
