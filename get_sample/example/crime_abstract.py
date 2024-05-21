from abc import *

import pandas as pd

class EditorBase(metaclass=ABCMeta):
    @abstractmethod
    def dropna(self, this:pd.DataFrame) -> pd.DataFrame:
        pass

class PrinterBase(metaclass=ABCMeta):
    @abstractmethod
    def print(self, message):
        pass

class ReaderBase(PrinterBase):
    
    @abstractmethod
    def csv(self, file):
        pass

    @abstractmethod
    def json(self, file):
        pass

    @abstractmethod
    def xls(self, file):
        pass

    @abstractmethod
    def gmaps(self):
        pass

class ScraperBase(metaclass=ABCMeta):
    @abstractmethod
    def driver(self):
        pass
