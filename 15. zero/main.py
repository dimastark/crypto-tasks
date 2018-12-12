import random


def main():
    p = int(input('Удостоверяющий центр выбирает p: '))
    q = int(input('Удостоверяющий центр выбирает q: '))

    n = p * q

    print('N = ', n)

    s = int(input('Алиса хочет доказать Бобу, что владеет секретом: '))

    v = pow(s, 2, n)

    print('v = ', v)

    k = int(input('Центр проводит k раундов: '))

    proved = True

    for i in range(1, k + 1):
        print(f'\nЦентр проводит раунд №{i}')

        r = random.randint(1, n)
        print('Алиса выбирает случайное r:', r)

        a = pow(r, 2, n)
        print('Алиса отправляет r^2 mod N:', a)

        e = random.randint(0, 1)
        print('Боб выбирает случайное e:', e)
        print('Боб отправляет e Алисе')

        y = (r * s ** e) % n
        print('Алиса отправляет y:', y)
        print(f'Проверка: {y}^2 (mod {n}) = {a}{f" * " + str(v) if e else ""} (mod N)')

        if pow(y, 2, n) == (a * v ** e) % n:
            print('Все верно!')
        else:
            proved = False
            break

    if proved:
        print('\nАлиса молодец! Смогла доказать Бобу владение секретом!')
    else:
        print('\nАлиса плохая! Обманывает Боба...')


if __name__ == '__main__':
    main()
