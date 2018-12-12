import random

from typing import Iterable, List, Tuple


PRIME = 2 ** 127 - 1

Polynomial = List[int]
PolynomialResult = Tuple[int, int]


def main():
    share_count = int(input('Разделяем секрет между: '))
    recover_count = int(input('Чтобы восстановить секрет надо: '))

    secret, shares = create_secret(recover_count, share_count)

    print('Сгенерированный секрет:', secret)
    print('Сгенерированные личные (разделяемые) секреты:\n\t' + '\n\t'.join(map(str, shares)))

    for i in range(2, share_count + 1):
        print(f'{i} человека смогли восстановить секрет:', recover_secret(shares[:i]))


def create_secret(recover_count: int, share_count: int) -> Tuple[int, List[PolynomialResult]]:
    if recover_count > share_count:
        raise ValueError('При таких параметрах невозможно будет восстановить секрет')

    polynomial = [random.randint(0, PRIME) for _ in range(recover_count)]
    shares = [(i, evaluate_polynomial(polynomial, i)) for i in range(1, share_count + 1)]

    return polynomial[0], shares


def evaluate_polynomial(polynomial: Polynomial, x: int) -> int:
    result = 0

    for c in reversed(polynomial):
        result = (result * x + c) % PRIME

    return result


def divide_mod(number: int, divider: int, modulo: int) -> int:
    return number * extended_euclidean(divider, modulo)


def extended_euclidean(a: int, b: int) -> int:
    old_x, x = 0, 1
    old_y, y = 1, 0

    while b != 0:
        q = a // b

        a, b = b, a % b

        old_x, x = x - q * old_x, old_x
        old_y, y = y - q * old_y, old_y

    return x


def recover_secret(shares: List[PolynomialResult]) -> int:
    if len(shares) < 2:
        raise ValueError('Нужно как минимум две точки')

    return interpolate_polynomial(0, *zip(*shares), PRIME)


def interpolate_polynomial(x: int, x_s: List[int], y_s: List[int], p: int) -> int:
    k = len(x_s)

    numbers = []
    dividers = []

    for i in range(k):
        others = list(x_s)
        current = others.pop(i)

        numbers.append(interpolate_pi(x - o for o in others))
        dividers.append(interpolate_pi(current - o for o in others))

    divider = interpolate_pi(dividers)
    number = sum([divide_mod(numbers[i] * divider * y_s[i] % p, dividers[i], p) for i in range(k)])

    return (divide_mod(number, divider, p) + p) % p


def interpolate_pi(numbers: Iterable[int]) -> int:
    result = 1

    for number in numbers:
        result *= number

    return result


if __name__ == '__main__':
    main()
