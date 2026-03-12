import os
import sys
import certifi
import pymongo

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("mongodb_connecting_url")

from network_security.exception.exception import CustomeException
from network_security.logging.logger import logging
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.utils.ml_utils.model.estimator import NetworkModel

from network_security.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


import pandas as pd
import numpy as np

ca = certifi.where()

## Global variables

preprocessor = None
model = None
network_model = None


from network_security.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def load_model():
    global preprocessor, model, network_model

    preprocessor = load_object("final_model/preprocessor.pkl")
    model = load_object("final_model/model.pkl")

    network_model = NetworkModel(
        preprocessor=preprocessor,
        model=model
    )

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipline = TrainingPipeline()
        training_pipline.run_pipeline()
        return Response("Training is Successful")
    except Exception as e:
         raise CustomeException(e,sys)
    
@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:

        if not file.filename.endswith(".csv"):
            return Response("Only CSV files allowed")
        
        df = pd.read_csv(file.file)

        y_pred = network_model.predict(df)

        df["predicted_column"] = y_pred

        df.to_csv("predictions_output/output.csv",index=False,header=True)
        
        table_html = df.to_html(classes="table table-striped")
        
        return templates.TemplateResponse("table.html",{"request":request, "table":table_html})
    except Exception as e:
        raise CustomeException(e,sys)
    
if __name__ == "__main__":
    app_run(app,host="0.0.0.0",port=8000)


