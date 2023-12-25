from lab4_math import generatePrime, getModuloInverse, HornerPow


class RSA:
    def __init__(self, e: int, length: int) -> None:
        self.e = e
        self.length = length
        self.n = None
        self._p = None
        self._q = None
        self._d = None
        self.BPubKey = None


    def encrypt(self, m: int) -> int:
        if self.BPubKey:
            n, e = self.BPubKey
            return HornerPow(m, e, n)
        raise Exception("Need to get a public key")


    def decrypt(self, c: int) -> int:
        if self._d and self.n:
            return HornerPow(c, self._d, self.n)
        raise Exception("Need to generate a key")


    def generateKeyPair(self) -> None:
        self._p = generatePrime(self.length)
        self._q = generatePrime(self.length)

        phi = (self._p - 1) * (self._q - 1)
        self._d = getModuloInverse(self.e, phi)
        self.n = self._p * self._q


    def sign(self, m: int) -> tuple[int, int]:
        if self._d and self.n:
            return (m, HornerPow(m, self._d, self.n))
        raise Exception("Need to generate a key")


    def verify(self, signature: tuple[int, int]) -> bool:
        m, s = signature
        if self.BPubKey:
            return m == HornerPow(s, self.BPubKey[1], self.BPubKey[0])
        raise Exception("Need to get a public key")


    def sendKey(self) -> tuple[int, int]:
        return (self.n, self.e)


    def receiveKey(self, publicKey: tuple[int, int]) -> None:
        self.BPubKey = publicKey


if __name__ == "__main__":
    A = RSA(2 ** 16 + 1, 256)
    B = RSA(2 ** 16 + 1, 256)

    A.generateKeyPair()
    B.generateKeyPair()

    A.receiveKey(B.sendKey())
    APubKeyModulo = A.n
    while APubKeyModulo > A.BPubKey[0]:
        A.generateKeyPair()
        APubKeyModulo = A.n

    B.receiveKey(A.sendKey())
    print(f"[*] A and B exchanged keys\n[*] A: {A.sendKey()}\nB: {B.sendKey()}\n")

    k = 1337228322

    sig = A.sign(k)
    print(f"[*] A signed message: {sig}\n")
    msg = A.encrypt(sig[0]), A.encrypt(sig[1])

    print(f"[*] Message from A to B: {msg}\n")

    print(f"[*] B received message from A: {msg}\n")

    decrypted_msg = B.decrypt(msg[0]), B.decrypt(msg[1])

    print(decrypted_msg)

    print(f"\n[*] Verification: {B.verify(decrypted_msg)}")
