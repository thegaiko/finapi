from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from endpoints import check_token, triple
import uvicorn

processes = []
thread_author_list = []

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenModel(BaseModel):
    token: str;


class TripleModel(BaseModel):
    bankList: list;
    assetList: list;
    amount: int;
    fiat: str;


@app.post("/api/check_token/")
async def request_bundle(model: TokenModel):
    return check_token(model.token)


@app.post("/api/get_triple/")
async def request_bundle(model: TripleModel):
    return triple(model.assetList, model.bankList, model.amount, model.fiat)


@app.get("/api/get_news/")
def read_item():
    return get_news()


if __name__ == '__main__':
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
                )
