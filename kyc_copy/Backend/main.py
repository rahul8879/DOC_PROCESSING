from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import io
from transformers import pipeline
import torch
from transformers import logging

logging.set_verbosity_error()

# Initialize FastAPI app
app = FastAPI()

# Configure tesseract command path (change based on your system configuration)

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\\Rahul\AppData\Local\Tesseract-OCR\tesseract.exe'

# Initialize Hugging Face NER model and tokenizer
device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER",
                        tokenizer="dslim/bert-base-NER", device=device)

# Function to extract information from the image


def extract_info_from_image(image: Image.Image):
    # Extract text from image using pytesseract
    text = pytesseract.image_to_string(image)

    # Use Hugging Face's NER pipeline to identify entities
    ner_results = ner_pipeline(text)

    extracted_data = {
        "Legal Name": None,
        "Date of Birth": None,
        "Nationality": None,
        "Residential Address": None,
        "Unique Identification Number": None,
        "Source of Fund": "Not available - Will request from Client"
    }

    # Process extracted entities
    for entity in ner_results:
        entity_text = entity['word']
        entity_label = entity['entity'].upper()

        # Map the recognized entities to our fields
        if entity_label == "B-PER" and extracted_data["Legal Name"] is None:
            extracted_data["Legal Name"] = entity_text
        elif entity_label == "DATE" and extracted_data["Date of Birth"] is None:
            extracted_data["Date of Birth"] = entity_text
        elif entity_label == "B-LOC" and extracted_data["Residential Address"] is None:
            extracted_data["Residential Address"] = entity_text
        elif entity_label == "ID" and extracted_data["Unique Identification Number"] is None:
            extracted_data["Unique Identification Number"] = entity_text
        elif entity_label == "NATIONALITY" and extracted_data["Nationality"] is None:
            extracted_data["Nationality"] = entity_text

    return extracted_data

# FastAPI route for KYC info extraction


@app.post("/extract-kyc-info/")
async def extract_kyc_info(file: UploadFile = File(...)):
    try:
        # Read and open the uploaded image
        image = Image.open(io.BytesIO(await file.read()))

        # Extract the required KYC info
        extracted_data = extract_info_from_image(image)

        return {"status": "success", "data": extracted_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Placeholder for another endpoint if needed (expand functionality as required)


@app.post("/process_odc/{doc_id}")
async def process_odc(doc_id: str, file: UploadFile = File(...)):
    try:
        # Add your logic for processing the ODC file
        pass
    except Exception as e:
        return {"status": "error", "message": str(e)}
