from fastapi import FastAPI
import uvicorn

from example.bmi import BMI

app = FastAPI()


@app.get("/")
async def root():
    m = BMI()
    return {"message": "Hello World 3"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)