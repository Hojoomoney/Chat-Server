from fastapi import APIRouter
from pydantic import BaseModel
from icecream import ic

from app.api.titanic.service.titanic_service import TitanicService

CONTEXT = 'C:\\Users\\bitcamp\\Aws\\chat-server\\backend\\app\\api\\context\\'

router = APIRouter()
service = TitanicService()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

@router.post("/titanic")
async def titanic(req: Request):
    ic(f"titanic dictionary is called")
    hello = f"{CONTEXT}data\\hello.txt"
    f = open(hello, "r", encoding="utf-8")
    data = f.read()
    ic(data)
    f.close()
    service.preprocess()
    ic(req)

    return Response(answer="그림 바꾼거 만족스럽네요.")



