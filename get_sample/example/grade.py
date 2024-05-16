from example.utils import myRandom

class Grade:

    def __init__(self) -> None:
        # 아래 주석된 부분을 완성합니다.
        kor = myRandom(0,100)
        eng = myRandom(0, 100)
        math = myRandom(0, 100)
        # sum = self.sum(kor, eng, math)
        # avg = self.agv(kor, eng, math)
        # grade = self.getGrade()
        # passChk = self.passChk()
        # return [sum, avg, grade, passChk]

    def sum(self, kor, eng, math):
        return kor + eng + math
    
    def avg(self, kor, eng, math):
        return (kor + eng + math) / 3
    
    def getGrade(self):
        pass

    def passChk(self):
        pass

