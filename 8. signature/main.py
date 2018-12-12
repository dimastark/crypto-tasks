from rsa import make_key_pair


N = 0
D = 0


def main():
    # Публичный и секретный ключи RSA банка
    bank_pub, bank_sec = make_key_pair(8)
    # Публичный и секретный ключи Боба
    bob_pub, bob_sec = make_key_pair(8)

    # Боб готовит N документов, маскирует их уникальными множителями
    documents = [bob_pub.blind(D) for _ in range(N)]

    # Банк случайно выбирает N-1 документ
    verify_documents = documents[:-1]

    # Банк вскрывает их и убеждается в корректности
    for message, factor in verify_documents:
        assert bob_pub.unblind(message, factor) == D

    # Банк подписывает оставшийся документ
    message, _ = documents[-1]
    print('Подписанное', D, '=', bank_sec.sign(message))


if __name__ == '__main__':
    N = int(input('Количество сгенерированных Бобом документов: '))
    D = int(input('Подписываемое число: '))

    main()
