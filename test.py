



class Student:
    def __init__(self, name, kor, eng, math):

        self.name = name
        self.kor = kor
        self.eng = eng
        self.math = math
    def average(self):
        self.avg = round((self.kor + self.eng + self.math) / 3, 2)




if __name__ == "__main__":
    john = Student("john", 11, 12, 12)
    john.average()
    print(john.__dict__)


