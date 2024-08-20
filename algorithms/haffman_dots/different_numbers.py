
def sum_numbers(number):
    """
    number - цифра, сумму которой нужно найти
    """
    # создания списка цифр c 1 цифрой
    spisok = [1]
    # total
    total = 1

    while total != number:

        if spisok[-1]+1+total > number:
            spisok[-1] = spisok[-1] + 1
            total += 1
        else:
            total += spisok[-1]+1
            spisok.append(spisok[-1]+1)

    return spisok


def main():
    # получаем значениe
    number = int(input())
    # выводим результат
    answer = sum_numbers(number)
    print(len(answer))
    print(*answer)


if __name__ == "__main__":
    main()
