from example.utils import Member, myRandom


class BMI():

    def __init__(self) -> None:
        '''utils.py / Members(), myRandom() 를 이용하여 BMI 지수를 구하는 계산기를 작성합니다.'''
        self.get_bmi()

    def get_bmi(self):
        this = Member()
        this.name = '홍길동'
        this.height = myRandom(160, 180)
        this.weight = myRandom(60, 90)
        bmi = this.weight / (this.height/100)**2
        print(f'{this.name}님의 BMI 지수는 {bmi:.2f}입니다.')
        if bmi < 18.5:
            print(f'{this.name}님은 저체중입니다.')
        elif 18.5 <= bmi < 23:
            print(f'{this.name}님은 정상입니다.')
        elif 23 <= bmi < 25:
            print(f'{this.name}님은 과체중입니다.')
        elif bmi >= 25:
            print(f'{this.name}님은 비만입니다.')


