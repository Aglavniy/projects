def takeSecond(elem):
    return elem[1]


def total_tots(total_count, spisok):
    # сортировка по второму значению
    spisok.sort(key=takeSecond)
    # первая точка
    tot = spisok[0][1]
    # создания списка точек
    # и добавление первой точки - вторая координата отрезка
    answer = [tot]

    # перебор по списку
    for cut_ in spisok[1:]:
        if tot < cut_[0]:
            tot = cut_[1]
            answer.append(tot)
    return answer


def main():
    # получаем кол-во отрезков
    total_count = int(input())
    # получаем список
    spisok = [list(map(int, input().split())) for i in range(total_count)]

    answer = total_tots(total_count, spisok)
    print(len(answer))
    print(*answer)


if __name__ == "__main__":
    main()
