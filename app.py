
import sys
import os
from typing import Optional
from datetime import datetime
import pandas as pd

from fastapi.responses import RedirectResponse,Response

from src.logging.custom_logging import logger
from src.utils.other_utils import load_object
from src.exceptions.custom_exception import CustomException
from fastapi import FastAPI, HTTPException,Request
from pydantic import BaseModel,Field,field_validator
from src.inference.request_validation import PredictionRequest,PredictionResponse
from src.inference.preprocessing import preprocessing,get_top_3_shap_features
import uvicorn
import uuid


app = FastAPI(title="Credit Risk API", description="API to predict credit risk", version="0.1")


MODEL_PATH ="models/xgboost_model.pkl"
EXPLAINER_PATH = "models/explainer.pkl"

model = load_object(MODEL_PATH)
explainer = load_object(EXPLAINER_PATH)


@app.get("/",tags= ["autentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.post("/predict",response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    request_id = str(uuid.uuid4())
    logger.info(f"Received prediction request {request_id}")
    timestamp =datetime.now().isoformat()

    if model is None or explainer is None:
        raise HTTPException(status_code=500,detail="Model or explainer not loaded")
    
    response = PredictionResponse(request_id=request_id,
                                raw_feature_values=request.model_dump(),
                                model_features={},
                                prediction_prob=None,
                                failure_reason={},
                                top_3_reason_codes={},
                                shap_values={},
                                status="processing",
                                timestamp=timestamp)
    
    try:
        input_data = pd.DataFrame([request.model_dump()])
        input_data = preprocessing(input_data)
        print(input_data)
        print(input_data.dtypes)

        response.model_features = input_data.to_dict(orient="records")[0]
        logger.info(f"Preprocessed input data for request {request_id}")

        prediction_prob = model.predict_proba(input_data)[:,1][0]
        response.prediction_prob = float(prediction_prob)
        logger.info(f"Prediction successful for request {request_id}")
        
        shap_values = explainer.shap_values(input_data)[0,:]

        # Create the full SHAP values dictionary
        all_shap_dict = {name: float(value) for name, value in zip(input_data.columns, shap_values)}
        response.shap_values = all_shap_dict

        # Get the top 3 reasons for the prediction
        top_shap_dict = get_top_3_shap_features(shap_values= all_shap_dict,prob= prediction_prob)
        
        response.top_3_reason_codes = top_shap_dict

        response.status = "Success"

        return response


    except Exception as e:
        logger.error(f"Prediction failed for request {request_id}")
        logger.error(e,exc_info=True)
        raise HTTPException(status_code=500,detail="Prediction failed")



if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)