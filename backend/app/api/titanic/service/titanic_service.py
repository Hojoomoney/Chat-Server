import pandas as pd

from app.api.titanic.model.titanic_model import TitanicModel


class TitanicService:    
    model = TitanicModel()

    def process(self): #self를 하면 인스턴스 변수를 사용할 수 있음 즉 등록된 변수를 사용할 수 있음 
        print('프로세스 시작')
        this = self.model # this는 property 자바에서는 getter setter ,self는 자바에서는 this
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name','Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        this.train = self.new_model('train.csv') 
        this.test = self.new_model('test.csv')
        self.df_info(this) # 데이터 프레임의 정보를 출력
        
        this.id = this.test['PassengerId'] # 문제를 제출할 때 필요한 id

        this = self.name_nominal(this)

        this = self.drop_feature(this, 'Name', 'SibSp', 'Parch', 'Cabin', 'Ticket')

        this = self.pclass_ordinal(this)
        this = self.embarked_nominal(this)
        this = self.age_ratio(this)
        this = self.sex_nominal(this)
        this = self.fare_ratio(this)
        
        self.df_info(this)

        this = self.create_train(this)

    @staticmethod
    def df_info(this): #self가 없으면 static 메소드
        [print(i.info()) for i in [this.train, this.test]]



    @staticmethod
    def create_train(this) -> str:  
        return this.train.drop('Survived', axis=1) # axis=1 열을 기준으로 삭제, axis=0 행을 기준으로 삭제 ,평가를 위한 데이터셋
    
    @staticmethod
    def create_label(this) -> str:
        return this.train['Survived'] # 결과데이터셋
    

    
    @staticmethod
    def pclass_ordinal(this) -> object:
        return this
    @staticmethod
    def extract_title_from_name(this) -> object:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i['Name'].str.extract('([A-Za-z]+)\.', expand=False)
        return this

    @staticmethod
    def name_nominal(this) -> object:
        return this
    @staticmethod
    def sex_nominal(this) -> object:
        return this
    @staticmethod
    def age_ratio(this) -> object:
        return this
    @staticmethod
    def embarked_nominal(this) -> object:
        return this
    @staticmethod
    def fare_ratio(this) -> object:
        return this