from lab4_math import generatePrime, getModuloInverse, HornerPow


class RSA:
    def __init__(self, e: int, length: int, name: str) -> None:
        self.name = name
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
