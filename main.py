from fastapi import FastAPI, UploadFile
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import google.generativeai as genai
import os

# Create an instance of the FastAPI class.
app = FastAPI()

# --- Google Cloud & Model Configuration ---
PROJECT_ID = "legal-guardian-ai"
PROCESSOR_ID = "28999c7f79f9582d"
LOCATION = "us-central1"
GEMINI_MODEL_NAME = "models/gemini-2.5-pro"

# --- API Keys & Credentials ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- AI & Parsing Functions ---
def parse_document_pdf(file_content: bytes):
    """
    Parses a document using Google Cloud's Document AI service.
    This function is specifically for PDFs.
    """
    try:
        from google.cloud.documentai_v1 import DocumentProcessorServiceClient, RawDocument
        
        client = DocumentProcessorServiceClient()
        processor_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
        
        # The API needs the content as a raw byte stream.
        raw_document = RawDocument(content=file_content, mime_type="application/pdf")

        request = {"name": processor_name, "raw_document": raw_document}
        response = client.process_document(request=request)
        document = response.document

        return document.text
            
    except Exception as e:
        return str(e)

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Hello, World! Legal Guardian AI backend is running."}

@app.get("/analyze-legal-text")
def analyze_legal_text():
    sample_text = "This Agreement shall be governed by and construed in accordance with the laws of the State of California."
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        prompt = f"Explain this legal sentence in simple, easy-to-understand language for a beginner:\n\n'{sample_text}'"
        response = model.generate_content(prompt)
        simplified_text = response.text
        
        return {
            "original_text": sample_text,
            "simplified_explanation": simplified_text,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.get("/status")
def read_status():
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return {"status": "SUCCESS", "message": "Google AI Studio API key is set and ready."}
    else:
        return {"status": "ERROR", "message": "GOOGLE_API_KEY environment variable not found."}

@app.post("/analyze-document")
async def analyze_document(file: UploadFile):
    try:
        content = await file.read()
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            # This part is for when you test with a PDF.
            parsed_text = parse_document_pdf(content)
        else:
            # This part will handle your contract.txt file.
            parsed_text = content.decode("utf-8")

        if "error" in parsed_text.lower():
            return {"status": "ERROR", "message": parsed_text}

        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        prompt = f"Analyze the following legal document and provide a summary of the key points in simple language:\n\n'{parsed_text}'"
        response = model.generate_content(prompt)
        simplified_summary = response.text

        return {
            "filename": file.filename,
            "summary": simplified_summary,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/what-if-simulation")
async def what_if_simulation(request: dict):
    """
    Simulates a "what-if" scenario based on document text and a user's question.
    """
    try:
        document_text = request.get("document_text")
        user_question = request.get("user_question")

        if not document_text or not user_question:
            return {"status": "ERROR", "message": "Missing 'document_text' or 'user_question' in the request."}

        prompt = f"""
        As an AI legal assistant, analyze the following legal document and answer the user's "what-if" question in simple, easy-to-understand language. Provide a clear explanation of the legal consequences based on the provided text.

        Document:
        {document_text}

        User's "What-if" Question:
        {user_question}

        Answer:
        """
        
        model = genai.GenerativeModel(GEMINI_MODEL_NAME) 
        response = model.generate_content(prompt)
        simulation_result = response.text

        return {
            "user_question": user_question,
            "simulation_result": simulation_result,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
