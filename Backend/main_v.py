from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import os
import matplotlib.pyplot as plt
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import utils
load_dotenv()




app = FastAPI()
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\\Rahul\AppData\Local\Tesseract-OCR\tesseract.exe'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/extract-kyc-info/")
async def extract_kyc_info(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        text, confidence = utils.extract_text_from_image(image_bytes)
        document_validation = utils.validate_passport_or_dl(text)
        extracted_data = utils.extract_info_from_text(text)
        return {
            "status": "success",
            "data": {
                "extracted_data": extracted_data,
                "document_validation": document_validation,
                "ocr_confidence": confidence
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
