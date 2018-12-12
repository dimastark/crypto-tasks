from itertools import cycle


def encrypt(key: str, m: str) -> str:
    """ Шифр Виженера. Функция шифрования. """
    result = ''

    for char, key_char, b in zip(m, cycle(key), cycle('backdoor')):
        result += chr((ord(char) + ord(key_char)) % 2048)
        result += chr((ord(char) + ord(b)) % 2048)

    return result


def decrypt(key: str, c: str, u: bool = False) -> str:
    """ Шифр Виженера. Функция расшифрования. """
    result = ''

    c = c[1::2] if u else c[::2]

    for char, key_char, b in zip(c, cycle(key), cycle('backdoor')):
        if u:
            result += chr((ord(char) - ord(b) + 2048) % 2048)
        else:
            result += chr((ord(char) - ord(key_char) + 2048) % 2048)

    return result
