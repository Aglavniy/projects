class Student:

    def __init__(self,
                 name,
                 surname,
                 grade):
        self.name = name
        self.surname = surname
        self.grade = grade

    def add_grade(self):
        self.grade += 1

    def print_info(self):
        print(f'Student: {self.name} {self.surname}')
        print(f'Grade: {self.grade}')


class PythonStudent(Student):

    def __init__(self,
                 name,
                 surname,
                 grade,
                 python_mark=0):
        super().__init__(name, surname, grade)
        self.python_mark = python_mark

    def learn_python(self):
        self.open = True

    def get_mark_python(self, hw1, hw2, hw3, hw4):
        try:
            if self.open:
                self.python_mark = round(0.3*hw1 + 0.3*hw2 + 0.3*hw3 + 0.1*hw4)
        except:
            print("Надо пойти учить питон")
            return 0
        return self.python_mark

    def print_info(self):
        super().print_info()
        print(f'Python mark: {self.python_mark}')


s1 = Student("Ivan", "Ivanov", 3)
s2 = PythonStudent("Petr", "Ivanov", 2)
print(s1.name, s1.surname, s1.grade)
print(s2.name, s2.surname)
print(s2.grade)
