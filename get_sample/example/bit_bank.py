import random
import utils

class BitBank:
    name : str
    account_number : str
    money : int
    BANK_NAME = '비트은행'

    def __init__(self,name) -> None:
        self.name = name
        self.account_number = self.create_account_number()
        self.money = utils.myRandom(100, 999)
        '''
        [요구사항(RFP)]
        은행이름은 비트은행이다.
        입금자 이름(name), 계좌번호(account_number), 금액(money) 속성값으로 계좌를 생성한다.
        계좌번호는 3자리-2자리-6자리 형태로 랜덤하게 생성된다.
        예를들면 123-12-123456 이다.
        금액은 100 ~ 999 사이로 랜덤하게 입금된다. (단위는 만단위로 암묵적으로 판단한다)
        '''
    def create_account_number(self) -> str:
        return f'{utils.myRandom(100,1000)}-{utils.myRandom(10,100)}-{utils.myRandom(100000,1000000)}'
    
    def deposit(self):
        print('계좌번호: ???? 입금액: ?? ')

    @staticmethod
    def find_account(ls, account_number):
        return [i for i in ls if i.account_number == account_number][0] # 리스트로 반환되기 때문에 [0]을 붙여서 객체로 반환
    @staticmethod
    def del_account(ls, account_number):
        [ls.remove(i) for i in ls if i.account_number == account_number]

def myRandom(start, end): return random.randint(start, end-1)
if __name__ == '__main__':
    list = []
    while True:
        menu = input('0.종료 1.계좌개설 2.계좌목록 3.입금 4.출금 5.계좌해지 6.계좌조회\n')
        if menu == '0': 
            print('프로그램을 종료합니다.') 
            exit()
        if menu == '1':
            name = input('입금자 이름을 입력하세요: ')
            this = BitBank(name)
            list.append(this)
            print('계좌가 생성되었습니다.')
            print(f'은행이름: {this.BANK_NAME}\n입금자: {this.name}\n계좌번호: {this.account_number}\n금액: {this.money}만원 입금되었습니다.')
        if menu == '2':
            for i in list:
                print(f'은행이름: {this.BANK_NAME}, 입금자: {i.name}, 계좌번호: {i.account_number}, 금액: {i.money}만원\n')
        if menu == '3':
            account_number = input('입금하실 계좌번호를 입력하세요: ')
            money = int(input('입금하실 금액을 입력하세요: '))
            this = BitBank.find_account(list, account_number)
            this.money += money
            print(f'계좌번호: {this.account_number} 입금액: {money}만원')
        if menu == '4':
            account_number = input('출금하실 계좌번호를 입력하세요: ')
            money = int(input('출금하실 금액을 입력하세요: '))
            this = BitBank.find_account(list, account_number)
            this.money -= money
            print(f'계좌번호: {this.account_number} 출금액: {money}만원')
        if menu == '5':
            account_number = input('해지하실 계좌번호를 입력하세요: ')
            BitBank.del_account(list, account_number)
            print('계좌가 해지되었습니다.')
        if menu == '6':
            account_number = input('조회하실 계좌번호를 입력하세요: ')
            this = BitBank.find_account(list, account_number)
            print(f'은행이름: {this.BANK_NAME}\n입금자: {this.name}\n계좌번호: {this.account_number}\n금액: {this.money}만원\n')