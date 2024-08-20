def takeSecond(elem):
    return elem[0]/elem[1]


def bag(v, spisok):
    """
    v - объем мешка
    spisok - список со значениями товаров
    """
    # сортировка по убыванию отношения
    spisok.sort(key=takeSecond, reverse=True)
    # создания цены
    price = 0

    # перебор по списку
    for good in spisok:
        # если объем меньше веса единицы товара
        # то считаем отношение на оставшийся объем
        if v <= good[1]:
            price += (good[0]/good[1])*v
            return round(price, 3)
        # обновляем
        price += good[0]
        # обновляем вес
        v = v-good[1]
    return round(price, 3)


def main():
    # получаем значения
    first_row = list(map(int, input().split()))
    # объем рюкзака
    v = first_row[1]

    # вводим список
    spisok = [list(map(int, input().split())) for i in range(first_row[0])]

    # выводим результат
    print(bag(v, spisok))


if __name__ == "__main__":
    main()
