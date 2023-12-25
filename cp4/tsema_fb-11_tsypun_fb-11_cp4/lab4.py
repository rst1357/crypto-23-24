from exchangeProto import ExchangeProtocol
from RSA import RSA


def main():
    e = 2 ** 16 + 1
    ep = ExchangeProtocol(Alice=RSA(e, 512, "Alice"), 
                          Bob=RSA(e, 512, "Bob")
    )

    ep.startExchange()
    ep.sendSecret(ep.Alice, ep.Bob, 133712345228)


if __name__ == "__main__":
    main()
    