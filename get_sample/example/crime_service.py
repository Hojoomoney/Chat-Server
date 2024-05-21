from dotenv import load_dotenv
import numpy as np
import pandas as pd
import os
import sys
import folium

from sklearn import preprocessing

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from example.crime_util import Editor, Reader
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
        self.crime_rate_columns = ['살인검거율','강도검거율','강간검거율','절도검거율','폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        self.arrest_columns = ['살인 검거','강도 검거','강간 검거','절도 검거','폭력 검거']

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
    
    def new_sframe(self, fname: str) -> pd.DataFrame:
        this = self.data
        return pd.read_csv(f'{this.sname}{fname}')

    def save_model(self, fname: str, dframe: pd.DataFrame):
        this = self.data
        dframe.to_csv(f'{this.sname}{fname}', na_rep='NaN')

    def save_police_position(self) -> None:
        station_name = []
        crime = self.new_dframe('police_position.csv')
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
        crime.to_csv(f'{self.data.sname}police_position.csv',sep=',', na_rep='NaN')
        for i in range(len(station_name)):
            ic(f'관서명:{station_name[i]},주소:{station_address[i]},위도:{station_lat[i]},경도:{station_lng[i]}')
    
    def save_cctv_population(self) -> None:
        population = Reader().xls(f'{self.data.dname}pop_in_seoul', 2, 'B, D, G, J, N')
        ic(population)
        cctv = self.new_dframe('cctv_in_seoul.csv')
        cctv.rename(columns={cctv.columns[0]:'구별'}, inplace=True) # inplace=True 원본을 수정
        population.rename(columns={population.columns[0]:'구별',
                                   population.columns[1]:'인구수',
                                   population.columns[2]:'한국인',
                                   population.columns[3]:'외국인',
                                   population.columns[4]:'고령자'}, inplace=True)
        ic(population.head(2))
        ic(cctv.head(2))
        # population에서 nan값이 있는지 확인 후 제거
        # population.dropna(how='all',inplace=True) # Nan값이 있는 행을 삭제
        population.drop(26,axis=0, inplace=True) #26번째 행 삭제
        population['외국인비율'] = population['외국인'].astype(int) / population['인구수'].astype(int) * 100
        population['고령자비율'] = population['고령자'].astype(int) / population['인구수'].astype(int) * 100
        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1, inplace=True)
        cctv_per_population = pd.merge(cctv, population, on='구별')
        cor1 = np.corrcoef(cctv_per_population['고령자비율'], cctv_per_population['소계']) #고령자비율과 cctv수의 상관계수 
        cor2 = np.corrcoef(cctv_per_population['외국인비율'], cctv_per_population['소계'])
        ic(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
              f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
        """
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]                        
         """
        cctv_per_population.to_csv(f'{self.data.sname}cctv_population.csv', sep=',', na_rep='NaN') # csv 파일로 저장

    def save_crime_arrest_normalization(self) -> None:
        crime = self.new_dframe('crime_in_seoul.csv')
        reader = Reader()
        police_position = reader.csv(f'{self.data.sname}police_position')
        police = pd.pivot_table(police_position, index='구별', aggfunc=np.sum)
        print('피봇 결과 :')
        ic(police)

        police['살인검거율'] = police['살인 검거'].astype(int) / police['살인 발생'].astype(int) * 100
        police['강도검거율'] = police['강도 검거'].astype(int) / police['강도 발생'].astype(int) * 100
        police['강간검거율'] = police['강간 검거'].astype(int) / police['강간 발생'].astype(int) * 100
        police['절도검거율'] = police['절도 검거'].astype(int) / police['절도 발생'].astype(int) * 100
        police['폭력검거율'] = police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int) * 100
        police.drop(['강간 검거', '강도 검거', '살인 검거', '절도 검거', '폭력 검거'], axis=1, inplace=True)

        ic(police)
        for i in self.crime_rate_columns:
            police.loc[police[i] > 100, i] = 100
        
        police.rename(columns={'강간 발생': '강간',
                               '강도 발생': '강도',
                               '살인 발생': '살인',
                               '절도 발생': '절도',
                               '폭력 발생': '폭력'}, inplace=True)
        print('loc 결과 :')
        ic(police)
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """     
        피쳐 스케일링(Feature scalining)은 해당 피쳐들의 값을 일정한 수준으로 맞춰주는 것이다.
        이때 적용되는 스케일링 방법이 표준화(standardization) 와 정규화(normalization)다.
        
        1단계: 표준화(공통 척도)를 진행한다.
            표준화는 정규분포를 데이터의 평균을 0, 분산이 1인 표준정규분포로 만드는 것이다.
            x = (x - mu) / sigma
            scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        2단계: 이상치 발견 및 제거
        3단계: 정규화(공통 간격)를 진행한다.
            정규화에는 평균 정규화, 최소-최대 정규화, 분위수 정규화가 있다.
             * 최소최대 정규화는 모든 데이터를 최대값을 1, 최솟값을 0으로 만드는 것이다.
            도메인은 데이터의 범위이다.
            스케일은 데이터의 분포이다.
            목적은 도메인을 일치시키거나 스케일을 유사하게 만든다.     
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_rate_columns, index=police.index)
        police_norm[self.crime_columns] = police[self.crime_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        police_norm.to_csv(f'{self.data.sname}police_norm.csv', sep=',', encoding='UTF-8')

        # occur = police_position.loc[:,[ '살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생']]
        # arrest = police_position.loc[:,['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']]
        # occur['발생 건수'] = occur.sum(axis=1)
        # arrest['검거 건수'] = arrest.sum(axis=1)
        # police_position['발생 건수'] = occur['발생 건수']
        # police_position['검거 건수'] = arrest['검거 건수']
        # police_position['검거율'] = police_position['검거 건수'] / police_position['발생 건수'] * 100
        # ic(police_position)
        # cctv_per_crime = pd.merge(cctv, police_position, on='구별')
        # cor1 = np.corrcoef(cctv_per_crime['소계'], cctv_per_crime['검거율'])
        # cor2 = np.corrcoef(cctv_per_crime['소계'], cctv_per_crime['발생 건수']) 
        # ic(f'cctv와 검거율 상관계수 {str(cor1)}') 
        # ic(f'cctv와 발생건수 상관계수 {str(cor2)}') 
        # cctv_per_crime.to_csv(f'{self.data.sname}cctv_per_crime.csv', sep=',', na_rep='NaN')

    def folium_test(self):
        reader = Reader()
        state_geo = reader.json(f'{self.data.dname}us-states')
        state_data = reader.csv(f'{self.data.dname}us_unemployment')
        m = folium.Map(location=[48, -102], zoom_start=3)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=state_data,
            columns=["State", "Crime_Rate"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Unemployment Rate (%)",
        ).add_to(m)

        folium.LayerControl().add_to(m)

        m.save(f'{self.data.sname}us_states.html')

    def draw_crime_map(self):
        reader = Reader()
        state_geo = reader.json(f'{self.data.dname}kr-states')
        state_data = reader.csv(f'{self.data.sname}police_norm')
        m = folium.Map(location=[37.5502, 126.982], zoom_start=12, title="Stamen Toner")
        police_position = reader.csv(f'{self.data.sname}police_position')
        police_norm = reader.csv(f'{self.data.sname}police_norm')
        crime = self.new_dframe('crime_in_seoul.csv')
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        station_addreess = []
        station_lats = []
        station_lngs = []
        gmaps = reader.gmaps(os.environ["api_key"])
        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            station_addreess.append(t[0].get("formatted_address"))
            t_loc = t[0].get("geometry")
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        police_position['lat'] = station_lats
        police_position['lng'] = station_lngs

        temp = police_position[self.arrest_columns] / police_position[self.arrest_columns].max()
        police_position['검거' ] = np.sum(temp, axis=1)



        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=tuple(zip(police_norm['구별'], police_norm['범죄'])),
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Crime Rate (%)",
            reset=True
        ).add_to(m)
        for i in police_position.index:
            folium.CircleMarker([police_position['lat'][i], police_position['lng'][i]],
                          radius=police_position['검거'][i] * 10,
                          fill_color='#0a0a32').add_to(m)

        folium.LayerControl().add_to(m)
        m.save(f'{self.data.sname}kr_states.html')

if __name__ == '__main__':
    service = CrimeService()
    # cctv_df = service.new_dframe('cctv_in_seoul.csv')
    # crime_df = service.new_dframe('crime_in_seoul.csv')
    # ic(cctv_df)
    # ic(crime_df)
    #service.save_police_position()
    # service.save_cctv_population()
    # service.save_crime_arrest_normalization()
    #service.folium_test()
    service.draw_crime_map()