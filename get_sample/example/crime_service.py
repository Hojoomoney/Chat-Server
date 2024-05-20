from dotenv import load_dotenv
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from example.crime_util import Reader
from example.crime_model import CrimeModel
from icecream import ic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class CrimeService:
    def __init__(self):
        self.data = CrimeModel()
        this = self.data
        this.dname = 'C:\\Users\\bitcamp\\Aws\\chat-server\\get_sample\\example\\data\\'
        this.sname = 'C:\\Users\\bitcamp\\Aws\\chat-server\\get_sample\\example\\save\\'
        self.crime_rate_columns = ['살인 검거율,강도 검거율,강간 검거율,절도 검거율,폭력 검거율']
        self.crime_columns = ['살인 발생,강도 발생,강간 발생,절도 발생,폭력 발생']
        self.arrest_columns = ['살인 검거,강도 검거,강간 검거,절도 검거,폭력 검거']

    def get_sname(self):
        return self.data.sname
    
    def new_dframe_idx(self, fname: str) -> pd.DataFrame:
        this = self.data
        # index_col=0 해야 기존 index 값이 유지된다
        # 0은 컬럼명 중 첫번째를 의미한다(배열구조)
        # pd.read_csv('경로/파일명.csv', index_col = '인덱스로 지정할 column명') Index 지정
        return pd.read_csv(f'{this.dname}{fname}', index_col=0)

    def new_dframe(self, fname: str) -> pd.DataFrame:
        this = self.data
        # pd.read_csv('경로/파일명.csv') Index 지정하지 않음
        return pd.read_csv(f'{this.dname}{fname}')

    def save_model(self, fname: str, dframe: pd.DataFrame):
        this = self.data
        dframe.to_csv(f'{this.sname}{fname}', sep=',', na_rep='NaN')

    def save_police_position(self) -> None:
        station_name = []
        crime = self.new_dframe('crime_in_seoul.csv')
        for name in crime['관서명']:
            station_name.append('서울'+str(name[:-1]+'경찰서'))
        station_address = []
        station_lat = []
        station_lng = []
        gmaps = Reader().gmaps(os.environ.get('api_key'))

        for name in station_name:
            t = gmaps.geocode(name, language='ko')
            station_address.append(t[0].get("formatted_address"))
            t_loc = t[0].get("geometry")
            station_lat.append(t_loc['location']['lat'])
            station_lng.append(t_loc['location']['lng'])
        
        gu_names = []
        for name in station_address:
            tmp = name.split()
            gu_name = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(gu_name)

        crime['구별'] = gu_names
        # 구와 경찰서의 위치가 다른 경우 수작업
        crime.loc[crime['관서명'] == '혜화경찰서', ['구별']] = '종로구'
        crime.loc[crime['관서명'] == '서부경찰서', ['구별']] = '은평구'
        crime.loc[crime['관서명'] == '강서경찰서', ['구별']] = '강서구'
        crime.loc[crime['관서명'] == '종암경찰서', ['구별']] = '성북구'
        crime.loc[crime['관서명'] == '방배경찰서', ['구별']] = '서초구'
        crime.loc[crime['관서명'] == '수서경찰서', ['구별']] = '강남구'
        crime.to_csv(f'{self.data.sname}police_position.csv', sep=',', na_rep='NaN')
        for i in range(len(station_name)):
            ic(f'관서명:{station_name[i]},주소:{station_address[i]},위도:{station_lat[i]},경도:{station_lng[i]}')

if __name__ == '__main__':
    service = CrimeService()
    cctv_df = service.new_dframe('cctv_in_seoul.csv')
    crime_df = service.new_dframe('crime_in_seoul.csv')
    ic(cctv_df)
    ic(crime_df)
    service.save_police_position()