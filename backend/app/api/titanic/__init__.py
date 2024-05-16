from app.api.titanic.service.titanic_service import TitanicService


if __name__ == "__main__":
    service = TitanicService()
    service.preprocess()