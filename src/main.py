from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import Annotated
from model import load_model, load_encoder
import pandas as pd
from contextlib import asynccontextmanager



ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_models["ohe"] = load_encoder()
    ml_models["models"] = load_model()
    yield
    ml_models.clear()


app = FastAPI(lifespan=lifespan)

bearer = HTTPBearer()

def get_username_for_token(token):
    if token == "abc123":
        return "pedro1"
    return None


async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    token = credentials.credentials

    username = get_username_for_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"username": username}

class Person(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    balance: int
    housing: str
    duration: int
    campaign: int

@app.get("/")
async def root():
    return "Model API is alive!"

@app.post("/predict")
async def predict(
    person: Annotated[
        Person,
        Body(
            examples=[
                {
                    "age": 42,
                    "job": "entrepreneur",
                    "marital": "married",
                    "education": "primary",
                    "balance": 558,
                    "housing": "yes",
                    "duration": 186,
                    "campaign": 2,
                }
            ],
        ),
    ],
    user=Depends(validate_token),
):  
    
    ohe = ml_models["ohe"]
    model = ml_models["models"]
    person_t = ohe.transform(pd.DataFrame([person.dict()]))
    pred = model.predict(person_t)[0]

    return {
        "prediction": str(pred),
        "username": user["username"]
        }