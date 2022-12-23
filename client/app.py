import pickle
from enum import Enum
from io import StringIO

import pandas as pd

# import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sklearn.pipeline import Pipeline


class Item_Fat_Content(str, Enum):
    low_fat = "Low Fat"
    regular = "Regular"


class Outlet_Size(str, Enum):
    medium = "Medium"
    high = "High"
    small = "Small"


class Feature(BaseModel):
    item_identifier: str = Field(max_length=6)
    item_weight: float
    item_fat_content: Item_Fat_Content
    item_visibility: float
    item_type: str
    item_mrp: float = Field(gt=0, description="MRP needs to be greater than 0", title=" MRP of product")
    outlet_identifier: str
    outlet_establishment_year: float
    outlet_size: Outlet_Size
    outlet_location_type: str
    outlet_type: str


def load_bin(file_path):
    with open(file_path, "rb") as f:
        obj = pickle.load(f)
    return obj


def get_model():
    preprocessing_obj = load_bin("./preprocessed.pkl")
    model = load_bin("./model.pkl")
    pipeline = Pipeline(steps=[("preprocessing", preprocessing_obj), ("model", model)])
    return pipeline


app = FastAPI(title="Sales Price Prediction", description="## Predict sales price with XGBoost")


@app.get("/")
def root():
    return RedirectResponse(url="/docs#")


@app.post("/predict")
def predict_one(feature: Feature):
    pipeline = get_model()
    data = jsonable_encoder(feature.dict())
    df = pd.DataFrame([data])
    y_pred = pipeline.predict(df.values)
    return {"prediction": y_pred.tolist()[0]}


@app.post("/predictcsv")
async def predict_csv(file: UploadFile):
    if file.content_type != "text/csv":
        raise HTTPException(415, "Requires csv file")
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode("utf-8")))
    # Validate Schema with same functionality as in Validate Schema Pipeline
    pipeline = get_model()
    y_pred = pipeline.predict(df.values)
    return {"prediction": y_pred.tolist()}


# if __name__ == "__main__":
# uvicorn.run(app=app,host="127.0.0.1",port='5000')
# uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
