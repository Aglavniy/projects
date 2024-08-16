def takeSecond(elem):
    return elem[0]/elem[1]


def total_tots(v, spisok):
    """
    v - объем мешка
    spisok - список со значениями товаров
    """
    # сортировка по второму значению
    spisok.sort(key=takeSecond, reverse=True)
    print(spisok)
    # первая точка
    dot = spisok[0][1]
    # создания списка точек
    # и добавление первой точки - вторая координата отрезка
    answer = [dot]

    # перебор по списку
    for cut_ in spisok[1:]:
        if dot < cut_[0]:
            dot = cut_[1]
            answer.append(dot)
    return answer


def main():
    # получаем значения
    first_row = list(map(int, input().split()))
    # объем рюкзака
    v = first_row[1]

    # вводим список
    spisok = [list(map(int, input().split())) for i in range(first_row[0])]
    print(spisok)
    answer = bag(v, spisok)
    #print(len(answer))
    #print(*answer)


if __name__ == "__main__":
    main()
