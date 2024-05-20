from dataclasses import dataclass
import pandas as pd


@dataclass
class CrimeModel:
    _dname : str = ''
    _sname : str = ''
    _fname : str = ''
    _cctv : str = ''
    _crime : str = ''
   
    @property
    def dname(self) -> str : return self._dname
    @dname.setter
    def dname(self, dname: str) : self._dname = dname
    @property
    def sname(self) -> str: return self._sname
    @sname.setter
    def sname(self, sname: str): self._sname = sname
    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname: str): self._fname = fname

    @property
    def cctv(self) -> str: return self.cctv

    @cctv.setter
    def cctv(self, cctv: pd.DataFrame): self.cctv = cctv

    @property
    def crime(self) -> str: return self.crime

    @crime.setter
    def crime(self, crime: pd.DataFrame): self.crime = crime
