# получаем список списков
spisok = [input().strip().split(' ') for _ in range(int(input()))]

# словарь с ответами
answer = {}

# проходиимся по строкам
for row in spisok:
    if row[0] in answer.keys():

        if row[1] in answer[row[0]].keys():
            # смотрим на кол-во попыток
            count_attempt = answer[row[0]][row[1]][0]
            # смотрим на результат
            result = answer[row[0]][row[1]][1]

            # если результат уже 'OK' то увеличиваем колзво попыток на 1 
            # есои нет тоже на 1 и меняем на row
            if result == 'OK':
                answer[row[0]][row[1]] = [count_attempt+1,
                                            result]
            else:
                # заходим во внутренний словапь и добавляем значение
                answer[row[0]][row[1]] = [count_attempt+1, row[2]]
        else:
            answer[row[0]][row[1]] = [1, row[2]]

    else:
        answer[row[0]] = {row[1]: [1, row[2]]}


# сортируем
answer = dict(sorted(answer.items(), key=lambda x: x[0]))

# вывод

for key, value in answer.items():
    counter = sum(map(lambda x: x[0], value.values()))

    result = sum(map(lambda x: x[1] == 'OK', value.values()))
    print(key, counter, result)
