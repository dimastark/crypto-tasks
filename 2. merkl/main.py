import random
import time


N = 0


def main():
    # Алиса генерирует N сообщений
    # Которые зашифрованы заведомо слабым шифром
    messages = generate_messages()

    # Боб выбирает некоторое сообщение
    message = random.choice(messages)

    # Боб взламывает это сообщение за O(n)
    bob_time = time.time()

    cracked_message = crack_weak_cypher(message)
    print('Время, которое потратил Боб (Абонент): {:.5f}'.format(time.time() - bob_time))

    i = int(cracked_message.split(',')[1])

    # Ева взламывает все сообщения за O(n^2)
    eva_time = time.time()
    for message in messages:
        cracked_message = crack_weak_cypher(message)
        if int(cracked_message.split(',')[1]) == i:
            print('Время, которое потратила Ева (Злоумышленник): {:.5f}'.format(time.time() - eva_time))
            break


def weak_encrypt(key: int, m: str) -> str:
    """ Шифр сдвига. Функция шифрования. """
    result = ''

    for char in m:
        result += chr(ord(char) + key)

    return result


def weak_decrypt(key: int, c: str) -> str:
    """ Шифр сдвига. Функция расшифрования. """
    result = ''

    for char in c:
        result += chr(ord(char) - key)

    return result


def crack_weak_cypher(c: str) -> str:
    for n in range(1, N + 1):
        m = weak_decrypt(n, c)
        if 'secret' in m:
            return m


def generate_messages() -> list:
    result = []

    for i in range(1, N + 1):
        result.append(weak_encrypt(i, 'secret{0},{0}'.format(i)))

    return result


if __name__ == '__main__':
    N = int(input('Количество сгенерированных Алисой сообщений: '))

    main()
