import pandas as pd
import numpy as np
from icecream import ic

from app.api.context.data_sets import DataSets
from app.api.context.models import Models


class TitanicModel(object):
    model = Models()
    dataset = DataSets()

    def preprocess(self, train_fname, test_fname) -> pd.DataFrame: # 데이터 전처리
        ic(f'--- TitanicModel 전처리 시작 ----')
        this =  self.dataset
        that = self.model
        ic(this)
        ic(that)
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        # 데이터셋은 Train과 Test, Validation 3종류로 나뉘어져 있다.
        this.train = that.new_dataframe_no_index(f'{train_fname}')
        this.test = that.new_dataframe_no_index(f'{test_fname}')
        this.id = this.test['PassengerId']
        this.label = this.train['Survived']
        this.train = this.train.drop('Survived', axis=1)
        this = self.drop_feature(this,'PassengerId', 'SibSp', 'Parch', 'Cabin', 'Ticket')
        # this = self.drop_feature(this, 'SibSp', 'Parch', 'Cabin', 'Ticket')
        this = self.extract_title_from_name(this)
        title_mapping = self.remove_duplicate_title(this)
        this = self.title_nominal(this, title_mapping)
        this = self.drop_feature(this, 'Name')
        this = self.sex_nominal(this)
        this = self.drop_feature(this, 'Sex')
        this = self.embarked_nominal(this)  
        this = self.age_ratio(this)
        this = self.drop_feature(this, 'Age')
        this = self.fare_ratio(this)
        this = self.drop_feature(this, "Fare")
        self.df_info(this)
        self.learning(this)

        return this
    
    @staticmethod
    def drop_feature(this, *feature) -> pd.DataFrame: # feature는 가변인자 자바에서는 필드라고 함 db에서는 컬럼이라고 함
        
        # for i in feature:
        #     this.train = this.train.drop(i, axis=1) # feature에 있는 컬럼을 삭제 [i]이렇게 하면 인덱스로 인식
        #     this.test = this.test.drop(i, axis=1)
        
        # for i in [this.train, this.test]:
        #     for j in feature:
        #         i.drop(j, axis=1, inplace=True) # inplace=True 원본을 삭제하겠다는 의미
        
        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train, this.test]]

        return this
    
    @staticmethod
    def df_info(this):
        ic('='*50)
        ic(type(this.train))
        ic(this.train.columns)
        ic(this.train.head())
        ic(this.train.isnull().sum())
        ic(this.train.isin([0, 1, 2, 3, 4, 5, 6, 7, 8]).sum() == this.train.count())
        ic(type(this.test))
        ic(this.test.columns)
        ic(this.test.head())
        ic(this.test.isnull().sum())
        ic(this.test.isin([0, 1, 2, 3, 4, 5, 6, 7, 8]).sum() == this.test.count())
        ic('='*50)
       

    @staticmethod
    def null_check(this):
        [ic(f'{i.isnull().sum()}') for i in [this.train, this.test]]

    @staticmethod
    def id_info(this):
        ic(f'id 의 타입  {type(this.id)}')
        ic(f'id 의 상위 3개 {this.id[:3]}')
    
    @staticmethod
    def title_nominal(this) -> None:
        return this
    
    @staticmethod
    def create_train(this) -> str:
        return this.train.drop('Survived', axis=1) # 0 : 행, 1 : 열
    

    @staticmethod
    def create_label(this) -> str:
        return this.train['Survived']
    
    # ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']

    # @staticmethod
    # def kwargs_sample(**kwargs) -> None:
    #     # ic(type(kwargs))
    #     {ic(''.join(f'key:{i}, val:{j}')) for i, j in kwargs.items()} # key:name, val:이순신

    @staticmethod
    def extract_title_from_name(this) -> pd.DataFrame:
        for i in [this.train, this.test]:
            i['Title'] = i['Name'].str.extract('([A-Za-z]+)\.', expand=False) #Mr. Mrs. Miss. Master. Dr. Capt. 등을 추출
        return this
    
    @staticmethod
    def remove_duplicate_title(this) -> pd.DataFrame:
        a = []
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        print(a)
        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        title_mapping = {'Mr':1, 'Ms':2, 'Mrs':3, 'Master':4, 'Royal':5, 'Rare':6}
        return title_mapping
    
    @staticmethod
    def title_nominal(this,title_mapping) -> pd.DataFrame:
        for these in [this.train, this.test]:
            these['Title'] = these['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            these['Title'] = these['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 'Rare')
            these['Title'] = these['Title'].replace(['Mlle'], 'Mr')
            these['Title'] = these['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            these['Title'] = these['Title'].fillna(0)
            these['Title'] = these['Title'].map(title_mapping)
        return this

    @staticmethod
    def age_ratio(this) -> pd.DataFrame:
        train = this.train
        test = this.test
        age_mapping = {'Unknown':0 , 'Baby': 1, 'Child': 2, 'Teenager' : 3, 'Student': 4,
                       'Young Adult': 5, 'Adult':6,  'Senior': 7}
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5) # 왜 NaN 값에 -0.5 를 할당할까요 ?
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf] # 이것을 이해해보세요 bins란 구간를 나타냄 
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']

        for these in train, test:
            pass # pd.cut() 함수를 사용해보세요 다른 곳은 고치지 말고 다음 두 줄만 완성하세요
            these['Age'] = pd.cut(these['Age'], bins, labels=labels) # Age를 구간화 시킴 
            these['AgeGroup'] = these['Age'].map(age_mapping) # AgeGroup을 만들어서 Age를 매핑시킴 Nominal로 만들어줌

        return this
    
    @staticmethod
    def sex_nominal(this) -> pd.DataFrame:
        
        sex_mapping = {'male' : 0, 'female' : 1}
        for i in [this.train, this.test]:
            i['Gender'] = i['Sex'].map(sex_mapping)
        
        return this
    
    @staticmethod
    def embarked_nominal(this) -> pd.DataFrame:
        
        embarked_mapping = {'X' : 0, 'S' : 1, 'Q' : 2, 'C' : 3}
        for i in [this.train, this.test]:
            i['Embarked'] = i['Embarked'].fillna("X").map(embarked_mapping)
        
        return this
    
    @staticmethod
    def fare_ratio(this) -> pd.DataFrame:
        bins = [-1, 8, 15, 31, np.inf]
        labels = [0, 1, 2, 3] # 0: Unknown, 1: Low, 2: Mid, 3: High
        for i in [this.train, this.test]:
            i['FareBand'] = pd.cut(i['Fare'].fillna(-0.5), bins, labels=labels)
        return this
    
    # @staticmethod
    # def kwargs_sample(**kwargs) -> None:
    #     # ic(type(kwargs))
    #     {ic(''.join(f'key:{i}, val:{j}')) for i, j in kwargs.items()} # key:name, val:이순신

    '''
    Categorical vs. Quantitative
    Cate -> nominal (이름) vs. ordinal (순서)
    Quan -> interval (상대) vs. ratio (절대)
    '''
    
    @staticmethod
    def learning(this) :
        ic(f'학습 시작')
        # k_fold = self.create_k_fold()
        # accuracy = self.get_accuracy(this, k_fold)
        accuracy = '70'
        ic(f'사이킷런 알고리즘 정확도: {accuracy}')
