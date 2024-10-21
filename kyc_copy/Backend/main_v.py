from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import io
from langchain import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from transformers import logging
import json
from fastapi.middleware.cors import CORSMiddleware
# Load environment variables from the .env file
load_dotenv()

# Get OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)

app = FastAPI()
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\\Rahul\AppData\Local\Tesseract-OCR\tesseract.exe'
app.add_middleware(
    CORSMiddleware,
    # Change this to the correct origin of your React app
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_image(image: Image.Image):
    return pytesseract.image_to_string(image)


def extract_info_from_text(text: str):
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

    # Convert the string response into a JSON object
    try:
        extracted_data = json.loads(llm_response)
    except json.JSONDecodeError:
        # Handle the case where the LLM response is not a valid JSON
        extracted_data = {"error": "Invalid JSON response from LLM"}

    return extracted_data


@app.post("/extract-kyc-info/")
async def extract_kyc_info(file: UploadFile = File(...)):
    try:
        # Read and open the uploaded image
        image = Image.open(io.BytesIO(await file.read()))

        # Step 1: Extract text from the image
        text = extract_text_from_image(image)

        # Step 2: Use LangChain LLM to extract KYC information from the text
        extracted_data = extract_info_from_text(text)

        return {"status": "success", "data": extracted_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/process_odc/{doc_id}")
async def process_odc(doc_id: str, file: UploadFile = File(...)):
    try:
        # Add your logic for processing the ODC file
        pass
    except Exception as e:
        return {"status": "error", "message": str(e)}
