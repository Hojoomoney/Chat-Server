from urllib.request import urlopen

from bs4 import BeautifulSoup


class ScrapBugs:

    def __init__(self):
        pass

    def scrap(self):
        print('벅스 뮤직 사이트에서 데이터를 수집합니다.')
        url = 'https://music.bugs.co.kr/chart/track/realtime/total?'
        html_doc = urlopen(url) # 해당 url에 접속하여 html 문서를 가져옴
        soup = BeautifulSoup(html_doc, 'lxml') # html 문서를 파싱하여 BeautifulSoup 객체로 변환
        list1 = self.find_music(soup, 'title') # 제목을 가져옴
        list2 = self.find_music(soup, 'artist') # 가수를 가져옴
        a = [i if i == 0 or i == 0 else i for i in range(1)] # 0으로 초기화된 리스트를 생성
        b = [i if i == 0 or i == 0 else i for i in []] # 빈 리스트를 생성
        c = [(i,j) for i, j in enumerate([])] # 빈 리스트를 enumerate로 변환 
        d = {i : j for i, j in zip(list1, list2)} # list1과 list2를 zip으로 묶어서 dict로 변환
        l = [i + j for i, j in zip(list1, list2)] # list1과 list2를 zip으로 묶어서 더함
        l2 = list(zip(list1, list2)) # list1과 list2를 zip으로 묶음
        d1 = dict(zip(list1, list2)) # list1과 list2를 zip으로 묶어서 dict로 변환 
        print(d1) # dict 출력
        return d 
    
    def find_music(self, soup:BeautifulSoup, classname:str) -> []: # soup과 classname을 받아서 []로 반환
        list = soup.find_all('p', {'class': classname}) # soup에서 p태그와 classname을 찾아서 list에 저장
        
        return [i.get_text() for i in list] # list에서 text만 가져와서 반환
    
if __name__ == '__main__':
    bugs = ScrapBugs() # ScrapBugs 객체 생성
    bugs.scrap() # scrap 메소드 호출
    