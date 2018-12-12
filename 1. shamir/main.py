from itertools import cycle


def main():
    message = input('Сообщение для передачи: ')

    # Алиса выбирает ключ шифрования - a
    a_key = input('Ключ шифрования Aлисы: ')

    # Алиса шифрует сообщение - E(a, M)
    message = encrypt(a_key, message)
    print('E(a, M): "{}"'.format(message))

    # Боб выбирает ключ шифрования - b
    b_key = input('Ключ шифрования Боба: ')

    # Боб шифрует сообщение - E(b, E(a, M))
    message = encrypt(b_key, message)
    print('E(b, E(a, M)): "{}"'.format(message))

    # Алиса - вычисляет D(a, E(b, E(a, M)))
    message = decrypt(a_key, message)
    print('D(a, E(b, E(a, M))): "{}"'.format(message))

    # Боб - вычисляет D(b, D(a, E(b, E(a, M)))) и получает исходное сообщение
    message = decrypt(b_key, message)
    print('D(b, D(a, E(b, E(a, M)))): "{}"'.format(message))


def encrypt(key: str, m: str) -> str:
    """ Шифр Виженера. Функция шифрования. """
    result = ''

    for char, key_char in zip(m, cycle(key)):
        result += chr((ord(char) + ord(key_char)) % 2048)

    return result


def decrypt(key: str, c: str) -> str:
    """ Шифр Виженера. Функция расшифрования. """
    result = ''

    for char, key_char in zip(c, cycle(key)):
        result += chr((ord(char) - ord(key_char) + 2048) % 2048)

    return result


if __name__ == '__main__':
    main()
