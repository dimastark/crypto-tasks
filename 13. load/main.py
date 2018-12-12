import psutil


def main():
    print('Процент загрузки компьютера:', psutil.cpu_percent(1))


if __name__ == '__main__':
    main()
