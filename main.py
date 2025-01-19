from fastapi import FastAPI
from uvicorn import run

app : FastAPI = FastAPI()

if __name__ == '__main__':
    run(app)