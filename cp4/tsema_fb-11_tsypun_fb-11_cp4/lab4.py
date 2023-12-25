from exchangeProto import ExchangeProtocol
from RSA import RSA


def main():
    e = 2 ** 16 + 1
    ep = ExchangeProtocol(Alice=RSA(e, 512, "Alice"), 
                          Bob=RSA(e, 512, "Bob")
    )

    ep.startExchange()
    enc = ep.sendKey(ep.Bob.getPubKey(), ep.Alice, ep.Bob, 1337229322)

    key = ep.receiveKey(ep.Alice.getPubKey(), ep.Alice, ep.Bob, enc)

    print(key)


if __name__ == "__main__":
    main()
    