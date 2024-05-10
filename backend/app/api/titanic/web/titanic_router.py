from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

@router.post("/titanic")
async def titanic(req: Request):
    print("titanic dictionary is called")
    print(req)

    print("titanic router에 들어갔음")
    
    return Response(answer="타이타닉 생존자수는 100명이야")



