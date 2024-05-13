from fastapi import FastAPI
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.main_router import router


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from pydantic import BaseModel


class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

app = FastAPI()

app.include_router(router, prefix="/api")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

#@app.post("/chat")
def chatting(req: Request):
    print(req)


    chat = ChatOpenAI(
        openai_api_key=os.environ["api_key"],
        temperature=0.1,               # 창의성 (0.0 ~ 2.0) 
        max_tokens=2048,             # 최대 토큰수
        model_name='gpt-3.5-turbo-0613',  # 모델명
        )


    # 질의
    print(f'{chat.predict(req.question)}')

    # message = [
    #     SystemMessage(content="You are a traveler, you know the capitals of every country in the world.", type="system"),
    #     HumanMessage(content="한국의 수도는 어디야 ?", type="human"),
    #     AIMessage(content="서울 입니다.", type="ai"),
    # ]
    # print('[답변] : ', chat.predict_messages(message))

    return Response(answer=chat.predict(req.question))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)