import pickle
from enum import Enum

import pandas as pd
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


class Item_Fat_Content(str, Enum):
    low_fat = "Low Fat"
    regular = "Regular"


class Outlet_Size(str, Enum):
    medium = "Medium"
    high = "High"
    small = "Small"


class Feature(BaseModel):
    item_identifier: str
    item_weight: float
    item_fat_content: Item_Fat_Content
    item_visibility: float
    item_type: str
    item_mrp: float
    outlet_identifier: str
    outlet_establishment_year: float
    outlet_size: Outlet_Size
    outlet_location_type: str
    outlet_type: str


def load_bin(file_path):
    print(file_path)
    with open(file_path, "rb") as f:
        obj = pickle.load(f)
    return obj


app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse(url="/docs#")


@app.post("/predict")
async def predict_one(feature: Feature):
    preprocessing_obj = load_bin("./preprocessed.pkl")
    model = load_bin("./model.pkl")
    pipeline = Pipeline(steps=[("preprocessing", preprocessing_obj), ("model", model)])
    data = jsonable_encoder(feature.dict())
    df = pd.DataFrame([data])
    y_pred = pipeline.predict(df.values)
    return {"prediction": y_pred.tolist()[0]}
