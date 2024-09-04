spisok = []
# Открытие файла для чтения
with open("text_test.txt", "r") as file:
    while True:
        # Чтение одной строки
        line = file.readline()
        if not line:  # Если строка пустая, конец файла
            break

        spisok.append(list(line.split(' '))[:3])
# словарь с ответами
answer = {}
# print(spisok)

# проходиимся по строкам
for row in spisok:

    surname = row[0]
    exercise = row[1]
    werdict = row[2]

    if surname in answer.keys():

        if exercise in answer[surname].keys():

            # смотрим на кол-во попыток
            count_attempt = answer[surname][exercise][0]
            # смотрим на результат
            result = answer[surname][exercise][1]

            # если результат уже 'OK' то увеличиваем колзво попыток на 1 
            # есои нет тоже на 1 и меняем на row
            if result == 'OK':
                answer[surname][exercise] = [count_attempt+1,
                                            result]
            else:
                # заходим во внутренний словапь и добавляем значение
                answer[surname][exercise] = [count_attempt+1, werdict]
        else:
            answer[surname][exercise] = [1, werdict]

    else:
        answer[surname] = {exercise: [1, werdict]}


# сортируем
answer = dict(sorted(answer.items(), key=lambda x: x[0]))

print(answer)
# вывод

for key, value in answer.items():
    counter = sum(map(lambda x: x[0], value.values()))

    result = sum(map(lambda x: x[1] == 'OK', value.values()))
    print(key, counter, result)
