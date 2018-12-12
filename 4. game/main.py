from enum import Enum
from itertools import cycle
from random import choice


class Move(Enum):
    Stone = 'Камень'
    Scissors = 'Ножницы'
    Paper = 'Бумага'

    @classmethod
    def choice(cls) -> 'Move':
        return choice([cls.Stone, cls.Scissors, cls.Paper])


def main():
    first_key = input('Первый игрок генерирует ключ шифрования: ')
    second_key = input('Второй игрок генерирует ключ шифрования: ')

    first_move = xor(Move.choice().value, first_key)
    second_move = xor(Move.choice().value, second_key)

    print('Первый игрок хочет выбросить:', first_move)
    print('Второй игрок хочет выбросить:', second_move)

    print('\nИгроки обменялись ключами.\n')

    print(xor(first_move, first_key), xor(second_move, second_key))


def xor(s: str, key: str):
    result = ''

    for sc, kc in zip(s, cycle(key)):
        result += chr(ord(sc) ^ ord(kc))

    return result


if __name__ == '__main__':
    main()
