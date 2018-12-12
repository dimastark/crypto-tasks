from c import encrypt, decrypt


def main():
    message = input('Надо зашифровать сообщение: ')
    key = input('Используем ключ: ')

    encrypted_message = encrypt(key, message)

    print('Зашифрованное сообщение: ', encrypted_message)

    print('Расшифрованное сообщение с помощью закладки: ', decrypt(encrypted_message, encrypted_message, True))


if __name__ == '__main__':
    main()
