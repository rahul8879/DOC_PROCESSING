
from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import io
import os
import re
import cv2
import matplotlib.pyplot as plt
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json
load_dotenv()

regex_DOB = re.compile(r'\d{2}[-/]\d{2}[-/]\d{4}')
passport_regex = re.compile(r'[A-Z]{1}[0-9]{6,8}')
dl_regex = re.compile(r'[A-Z0-9]{5,15}')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)


def preprocess_image(image_bytes):
    """Preprocess image using OpenCV and PIL for better OCR results."""
    image = Image.open(io.BytesIO(image_bytes))

    # Convert to OpenCV format
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    enhanced_image = cv2.convertScaleAbs(gray_image, alpha=1.5, beta=20)

    return enhanced_image


def extract_text_from_image(image_bytes):
    """Use Tesseract to extract text from image bytes."""
    processed_image = preprocess_image(image_bytes)

    # Extract text with Tesseract
    text = pytesseract.image_to_string(processed_image, lang='eng')
    text = text.replace("\n", " ").replace("  ", " ")

    # We will return 0 confidence here for now as we don't have confidence from tesseract
    return text, 0


def extract_info_from_text(text: str):
    """Use LangChain to extract specific KYC details from the text."""
    prompt_template = """
    Extract the following KYC details from the given text: 
    - Legal Name
    - Date of Birth
    - Nationality
    - Residential Address
    - Unique Identification Number

    Text: {text}
    
    Please return the information in the following JSON format:
    {{
        "Legal Name": "Full Name",
        "Date of Birth": "DD/MM/YYYY",
        "Nationality": "Country",
        "Residential Address": "Address",
        "Unique Identification Number": "ID"
    }}
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    llm_response = llm(prompt.format(text=text))

    try:
        extracted_data = json.loads(llm_response)
    except json.JSONDecodeError:
        extracted_data = {"error": "Invalid JSON response from LLM"}

    return extracted_data


def calculate_confidence(extracted_value: str, expected_length: int, max_confidence: float = 0.95) -> float:
    """
    Calculate confidence based on how well the extracted value matches the expected format.
    """
    if not extracted_value:
        return 0.0

    length_score = len(extracted_value) / \
        expected_length if len(extracted_value) <= expected_length else 0
    regex_score = 1.0
    final_score = (length_score * 0.5) + \
        (regex_score * 0.5)  # Weight both equally
    return final_score * max_confidence


def validate_passport_or_dl(text: str):
    """Check if the document is a valid passport or driving license and calculate confidence dynamically."""
    passport_match = re.search(passport_regex, text)
    dl_match = re.search(dl_regex, text)

    if passport_match:
        passport_number = passport_match.group()
        confidence = calculate_confidence(passport_number, expected_length=8)
        return {"document_type": "Passport", "valid": True, "confidence": confidence}
    elif dl_match:
        dl_number = dl_match.group()
        confidence = calculate_confidence(dl_number, expected_length=15)
        return {"document_type": "Driving License", "valid": True, "confidence": confidence}
    else:
        return {"document_type": "Unknown", "valid": False, "confidence": 0.0}
