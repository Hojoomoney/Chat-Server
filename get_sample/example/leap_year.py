class LeapYear:

    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 윤년계산기 객체를 생성합니다')
        print ('(ex) 2020년은 윤년입니다. 단 컴프리헨션을 사용합니다')

    def is_leap_year(self, year):
        if year % 4 != 0:
            return False
        elif year % 100 == 0 and year % 400 != 0:
            return False
        else:
            return True
