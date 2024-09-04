

def subsets(lst):

    # возвращаем первое значение
    yield []
    # создаем список ответов
    answer = []
    # проверка множеств
    set_answer = []

    # вносим одинарные значения в список
    for num in lst:
        value = set([num])
        if value not in answer:
            set_answer.append(value)
            answer.append([num])
            yield [num]


    # проходим по списку списков
    for num in answer:

        for number in lst:

            values = set(num)
            values.add(number)

            if values not in set_answer:
                set_answer.append(values)
                answer.append([*list(num), number])

                yield [*list(num), number]

lst = [1,2,3,4]  
k=0
for subset in subsets(lst):  
    print(subset)
    k+=1
print(k)