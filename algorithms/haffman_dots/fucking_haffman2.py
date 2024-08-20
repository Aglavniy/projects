def code_haffman(voca_code, code):
    # сортировка
    voca_code.sort(key=lambda x: x[1])

    # ответ
    answer = ''

    while len(code) > 0:
        for row in voca_code:
            if row[1] == code[:len(row[1])]:
                answer += row[0]
                code = code[len(row[1]):]

    print(answer)


# кол-во и длина кода
counter, length = map(int, input().split())

# вводим списко с значением и кодом
voca_code = [(input().split(': ')) for row in range(counter)]

# ввод кода
code = input()

code_haffman(voca_code, code)