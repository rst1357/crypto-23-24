from RSA import *


class ExchangeProtocol:
    def __init__(self, Alice: RSA, Bob: RSA) -> None:
        self.Alice = Alice
        self.Bob = Bob


    def startExchange(self) -> None:
        self.Alice.generateKeyPair()
        self.Bob.generateKeyPair()

        self._sendKey(sender=self.Bob, recipient=self.Alice)
        while not self._isPossibleToExchange(self.Alice, self.Bob):
            self.Alice.generateKeyPair()

        self._sendKey(sender=self.Alice, recipient=self.Bob)

        print(f"[*] {self.Alice.name} and {self.Bob.name} can communicate now\n")

    
    def _isPossibleToExchange(self, sender: RSA, recipient: RSA) -> bool:
        return sender.n <= recipient.n


    def _sendKey(self, sender: RSA, recipient: RSA) -> None:
        recipient.receiveKey(key := sender.sendKey())
        print(f"[*] {sender.name} sent the public key to {recipient.name}: {key}\n")

    
    def sendSecret(self, sender: RSA, recipient: RSA, message: int) -> None:
        if not self._isPossibleToExchange(sender, recipient):
            print(f"[-] {sender.name} can\'t send secret to {recipient.name}\n")
            return
        
        signature = sender.sign(message)
        print(f"[*] {sender.name} signed secret: {signature}\n")

        encrypted = sender.encrypt(signature[0]), sender.encrypt(signature[1])
        print(f"[*] {recipient.name} received secret from {sender.name}: {encrypted}\n")

        decrypted = recipient.decrypt(encrypted[0]), recipient.decrypt(encrypted[1])
        print(f"[*] Decrypted secret: {decrypted}\n")
        print(f"[*] Signature verification: {recipient.verify(decrypted)}\n")
        