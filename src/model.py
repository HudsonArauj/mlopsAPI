import pickle
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.DEBUG)

def load_encoder():
    try:
        with open("../models/ohe.pkl", "rb") as f:
            encoder = pickle.load(f)
        return encoder
    except Exception as e:
        logging.error(f"Error loading encoder: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading encoder: {e}")

def load_model():
    try:
        with open("../models/model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading model: {e}")    

