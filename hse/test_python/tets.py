spisok = [1,2,3]

def func(spisok):
    for i in range(len(spisok)):

        slice = spisok[:i+1]
        if len(spisok) - len(slice) >=2:
            print('here')
            func([1, [2,3]])
            # func(spisok[i:])
        print(spisok[:i+1])

func(spisok)