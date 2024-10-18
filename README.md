# Document AI Admin Portal

This project is for extracting KYC information from documents, built using **FastAPI** as the backend and **ReactJS** for the frontend. The application allows users to upload KYC documents, extract necessary information, and display it in a professional, user-friendly interface.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup (FastAPI)](#backend-setup-fastapi)
  - [Frontend Setup (ReactJS)](#frontend-setup-reactjs)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

## Features

- **File Upload**: Upload KYC documents in image format.
- **Data Extraction**: Extract details such as Legal Name, Date of Birth, Nationality, Residential Address, and Unique Identification Number.

## Technologies Used

- **Backend**: FastAPI (Python), Tesseract for OCR, LangChain for text extraction
- **Frontend**: ReactJS, Redux, React Bootstrap
- **Styling**: SCSS, Bootstrap

## Project Structure

```
kyc_doc/
│
├── backend/                   # FastAPI backend
│   ├── main.py                # Main FastAPI app
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│
├── frontend/                  # React frontend
│   ├── public/                # Public assets
│   ├── src/                   # Source code
│   │   ├── components/        # React components
│   │   │   └── AdminPortal.jsx
│   │   ├── redux/             # Redux store
│   │   │   └── store.js
│   │   ├── App.js             # Main app component
│   │   └── index.js           # Entry point
│
└── README.md                  # Project documentation
```

## Setup Instructions

### Backend Setup (FastAPI)

1. **Navigate to the backend directory**:

   ```bash
   cd admin-portal-kyc/backend
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup (ReactJS)

1. **Navigate to the frontend directory**:

   ```bash
   cd admin-portal-kyc/frontend
   ```

2. **Install the dependencies**:

   ```bash
   npm install
   ```

3. **Start the React application**:

   ```bash
   npm start
   ```

   The app will run on `http://localhost:3000`.

## Usage

1. **Upload Image**: Use the upload form to select a KYC document image.
2. **Extract Data**: Click on "Extract KYC Data" to process the image.
3. **View Extracted Data**: The extracted information will be displayed below the form.

## Screenshots

1. **Initial Page**: Upload KYC document form.
   ![Initial Page](./screenshots/upload.png)

2. **File Selected and Extracted Data Displayed**:
   ![Extracted Data](./screenshots/final_output.png)

## Future Improvements

- **Authentication**: Add login and authentication to ensure only authorized users can access the portal.
- **Multi-File Upload**: Add support for batch processing of documents.
- **Deployment**: Deploy the application using Docker and container orchestration tools like Kubernetes.
