import json
import os
import pandas as pd
from example.crime_abstract import EditorBase, PrinterBase, ReaderBase, ScraperBase
from icecream import ic
from selenium import webdriver
import googlemaps

class Printer(PrinterBase):
    def dframe(self, this: pd.DataFrame) -> None:
        print('*' * 100)
        ic(f'Type: {type(this)}')
        ic(f'Columns: {this.columns}')
        ic(f'Head1: {this.head(1)}')
        ic(f'null count: {this.isnull().sum()}')
        print(f'Printer: {this}')
    

class Reader(ReaderBase):
    def __init__(self) -> None:
        pass

    def print(self, message):
        ic(message)

    def csv(self, file) -> pd.DataFrame:
        return pd.read_csv(f'{file}.csv', encoding='utf-8', thousands=',')
    
    def xls(self, file, header, usecols) -> pd.DataFrame:
        return pd.read_excel(f'{file}.xls',header=header, usecols = usecols)
    
    def json(self, file) -> pd.DataFrame:
        return json.load(open(f'{file}.json', encoding='utf-8'))
    
    def gmaps(self, api_key) -> pd.DataFrame:
        return googlemaps.Client(key=api_key)

class Scraper(ScraperBase):
    def __init__(self) -> None:
        pass

    def driver(self) -> object:
        return webdriver.Chrome('C:/Program Files/Google/Chrome/chromedriver')
    
    def auto_login(self,driver,url,selector,data) -> None:
        driver.get(url)
        driver.find_element_by_css_selector(selector).send_keys(data)
        driver.find_element_by_css_selector(selector).submit()

class Editor(EditorBase):
    def dropna(self, this: pd.DataFrame) -> pd.DataFrame:
        this = this.dropna()
        return this