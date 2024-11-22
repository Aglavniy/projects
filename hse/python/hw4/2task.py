from sys import stdin
import copy

class MatrixError(BaseException):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2

class Matrix():

    def __init__(self, spisok):
        self.spisok = copy.deepcopy(spisok)

    def __str__(self):
        # проходим по вложенным спискам
        stroka = ''
        for iter_row in range(len(self.spisok)):
            row = self.spisok[iter_row]
            # заходим внутрь списка
            for iter in range(len(row)):
                number = row[iter]

                if len(row) > iter+1:
                    stroka += f'{number}\t'
                elif (len(row) == iter+1) & (iter_row+1 != len(self.spisok)):
                    stroka += f'{number}\n'
                else:
                    stroka += f'{number}'
        return stroka

    def size(self):
        rows = len(self.spisok)
        columns = len(self.spisok[0])
        return (rows, columns)
    
    def __add__(self, other):
        # proverka
        if self.size() != other.size():
            raise MatrixError(self, other)

        # итоговая мтарица
        c = []
        for index in range(len(self.spisok)):
            row_len = len(self.spisok[index])
            num_spisok = []
            for index_num in range(row_len):
                num = self.spisok[index][index_num]+other.spisok[index][index_num]
                num_spisok.append(num)
            c.append(num_spisok)
        
        return Matrix(c)

    def __mul__(self, other):
        if isinstance(other, (int,float)):
            return Matrix([[num * i for i in row] for row in self.spisok])
        
        elif isinstance(other, Matrix):
            # proverka
            if self.size()[1] != other.size()[0]:
                raise MatrixError(self, other)
            else:
                result = [[sum(x * y for x, y in zip(row_a, col_b)) for col_b in zip(*other.spisok)] for row_a in self.spisok]
                return Matrix(result)

    def __rmul__(self, rnum):

        return Matrix([[rnum * i for i in row] for row in self.spisok])
    
    def transpose(self):
        n = len(self.spisok)
        m = len(self.spisok[0])

        for i in range(m):
            temp = []
            for j in range(n):
                temp.append(self.spisok[j][i])
            self.spisok.append(temp)

        for i in range(n):
            del self.spisok[0]

        return Matrix(self.spisok)



"""
Измените метод __mul__ таким образом, чтобы матрицы можно было умножать как на скаляры, 
так и на другие матрицы. В случае, если две матрицы перемножить невозможно, 
то тогда выбросьте ошибку MatrixError. Первая матрице в ошибке – это self, вторая – это второй операнд умножения.
"""
# Task 4 check 1
mid = Matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
print(mid * m1)
print(mid * m2)
print(m2 * m1)
try:
    m = m1 * m2
    print("WA It should be error")
except MatrixError as e:
    print(e.matrix1)
    print(e.matrix2)