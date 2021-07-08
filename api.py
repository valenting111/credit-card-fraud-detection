from fastapi import FastAPI
from typing import Optional, Dict, List
from pydantic import BaseModel
from joblib import load
import pandas as pd
import uvicorn
import os

app = FastAPI()

trained_svc = load("svc.joblib")


class NewRequest(BaseModel):
    """
    Request should arrive as a dict of {feature name: value}
    Name is just to identify the request
    """
    name: str = ""
    features: Dict[str, float]


class ResponseBody(BaseModel):
    """
    Response body for a predictions request: a Dict of metrics messages and their values
    """
    output: Optional[Dict[str, int]]
    name: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
def read_root():
    return "You can access you credit card fraud detector at the /predict endpoint"


@app.get("/testing_out_stuff/{user_id}/{user_age}")
def testing_fastapi(user_id: str = "SomeID", user_age: int = 20) -> str:
    return f"Your ID is {user_id} and your age is {user_age}"


@app.post("/predict")
def predict_fraud(card_transaction: NewRequest):
    input_features = card_transaction.features
    name = card_transaction.name
    input_features = pd.DataFrame.from_dict(
        {k: [v] for k, v in input_features.items()})
    pred = trained_svc.predict(input_features)[0]
    return ResponseBody(output={"Prediction is:": pred}, name=name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get('PORT', 8000))
