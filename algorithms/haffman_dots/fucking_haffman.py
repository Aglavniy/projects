def code_haffman(letters):
    # уникальные значения
    spisok = list(set(letters))

    # для построени дереева и сортировки
    voca_letters = {}
    # для ответа
    code = {}
    for letter in spisok:
        voca_letters[letter] = letters.count(letter)
        code[letter] = ''

    if len(voca_letters) == 1:
        code[spisok[0]] = '0'


    while len(voca_letters) != 1:

        # вводим первую и вторую пременную 0 и 1
        first = '0'
        second = '1'

        # сортируем наши буквы по частотности
        sorted_letters = sorted(voca_letters,
                                key=lambda x: voca_letters.get(x))

        # считаем сумму наименьших значений
        total = voca_letters[sorted_letters[0]]+voca_letters[sorted_letters[1]]

        # добавляем в наш answer данные
        if voca_letters[sorted_letters[0]] < voca_letters[sorted_letters[1]]:
            first = '1'
            second = '0'
        
        for key in code:
            if key in sorted_letters[0]:
                code[key] = first + code[key]
            if key in sorted_letters[1]:
                code[key] = second + code[key]

        # добавляем значения и удаляем из списка наименьшие значения
        voca_letters[sorted_letters[1]+sorted_letters[0]] = total
        voca_letters.pop(sorted_letters[0])
        voca_letters.pop(sorted_letters[1])


    # нужно закодировать
    for key, value in code.items():

        letters = letters.replace(key, value)
    return code, letters

code, letters = code_haffman(input())

print(len(code), len(letters))

for key, value in code.items():
    print("{0}: {1}".format(key, value))

print(letters)
