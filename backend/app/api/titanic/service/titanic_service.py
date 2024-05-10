from backend.app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd

class TitanicService:    
    model = TitanicModel()

    def new_model(self, payload) -> object:
        this = self.model
        this.context = 'titanic/data/'
        this.fname = payload
        return pd.read_csv(this.context + this.fname)
