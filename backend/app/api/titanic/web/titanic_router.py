from fastapi import APIRouter
from pydantic import BaseModel

from app.api.titanic.service.titanic_service import TitanicService

router = APIRouter()
service = TitanicService()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

@router.post("/titanic")
async def titanic(req: Request):
    print("titanic dictionary is called")
    hello = 'C:\\Users\\bitcamp\\Aws\\chat-server\\backend\\app\\api\\titanic\\data\\hello.txt'
    f = open(hello, "r", encoding="utf-8")
    data = f.read()
    print(data)
    f.close()
    service.process()
    print(req)

    return Response(answer="타이타닉 생존자수는 100명이야")



