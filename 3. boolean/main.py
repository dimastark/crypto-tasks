import random


def main():
    pay = int(input('Кто платит? (0 - АНБ или 1,2,3 - криптоаналитики): '))

    # Каждый из криптоаналитиков подбрасывает монетку
    # И говорит соседу справа свой результат
    first = throw_coin()
    second = throw_coin()
    third = throw_coin()

    print('Результаты подбросов монеток: {} {} {}'.format(first, second, third))

    # Каждый из криптоаналитиков смотрит, совпал ли результат с соседом

    # Если первый платит, то он отвечает наоборот
    first_result = third == first if pay != 1 else third != first
    # Если второй платит, то он отвечает наоборот
    second_result = first == second if pay != 2 else first != second
    # Если третий платит, то он отвечает наоборот
    third_result = second == third if pay != 3 else second != third

    print('Первый говорит, что монетки {}совпали'.format('' if first_result else 'не '))
    print('Второй говорит, что монетки {}совпали'.format('' if second_result else 'не '))
    print('Третий говорит, что монетки {}совпали'.format('' if third_result else 'не '))

    result = first_result + second_result + third_result

    if result % 2:
        print('Выяснилось, что платит АНБ')
    else:
        print('Выяснилось, что платит криптоаналитик')


def throw_coin() -> int:
    return random.choice([0, 1])


if __name__ == '__main__':
    main()
