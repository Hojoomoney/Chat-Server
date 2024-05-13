import pandas as pd

from app.api.titanic.model.titanic_model import TitanicModel


class TitanicService:    
    model = TitanicModel()

    def process(self): #self를 하면 인스턴스 변수를 사용할 수 있음 즉 등록된 변수를 사용할 수 있음 
        print('프로세스 시작')
        this = self.model # this는 property 자바에서는 getter setter ,self는 자바에서는 this
        this.train = self.new_model('train.csv') # this.train_model은 자바에서는 this.trainModel
        this.test = self.new_model('test.csv')
        self.df_info(this) # 데이터 프레임의 정보를 출력
        
        this.id = this.test['PassengerId'] # 문제를 제출할 때 필요한 id

        this = self.drop_feature(this, 'Name', 'SibSp', 'Parch', 'Cabin', 'Ticket')
        
        self.df_info(this)

        this = self.create_train(this)

    @staticmethod
    def df_info(this): #self가 없으면 static 메소드
        [print(i.info()) for i in [this.train, this.test]]

    def new_model(self, payload) -> object:
        this = self.model
        this.context = './app/api/titanic/data/'
        this.fname = payload
        return pd.read_csv(this._context + this._fname)

    @staticmethod
    def create_train(this) -> str:  
        return this.train.drop('Survived', axis=1) # axis=1 열을 기준으로 삭제, axis=0 행을 기준으로 삭제 ,평가를 위한 데이터셋
    
    @staticmethod
    def create_label(this) -> str:
        return this.train['Survived'] # 결과데이터셋
    
    @staticmethod
    def drop_feature(this, *feature) -> object: # feature는 가변인자 자바에서는 필드라고 함 db에서는 컬럼이라고 함
        
        # for i in feature:
        #     this.train = this.train.drop(i, axis=1) # feature에 있는 컬럼을 삭제 [i]이렇게 하면 인덱스로 인식
        #     this.test = this.test.drop(i, axis=1)
        
        # for i in [this.train, this.test]:
        #     for j in feature:
        #         i.drop(j, axis=1, inplace=True) # inplace=True 원본을 삭제하겠다는 의미
        
        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train, this.test]]

        return this
        