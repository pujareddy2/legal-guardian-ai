from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from collections import defaultdict

# --- NEW: We only need the dotenv library to find our secure JSON key ---
# ... your existing imports
import os 
from dotenv import load_dotenv
load_dotenv()

# --- ADD THESE FOUR LINES ---
print("--- DEBUGGING AUTH ---")
key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f"Attempting to use key file from path: {key_path}")
print("----------------------")

# Google Cloud
from google.cloud.documentai_v1 import DocumentProcessorServiceClient, RawDocument, ProcessRequest
# ... rest of your code

# Google Cloud
from google.cloud.documentai_v1 import DocumentProcessorServiceClient, RawDocument, ProcessRequest
from google.api_core.client_options import ClientOptions
# --- GEMINI API IMPORT ---
import google.generativeai as genai

# --- FastAPI App Initialization ---
app = FastAPI()

# --- CORS Configuration ---
origins = [ "http://localhost:3000", "http://127.0.0.1:3000" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Google Cloud & Model Configuration ---
# NOTE: We no longer need the GOOGLE_API_KEY. 
# The genai library will automatically use your GOOGLE_APPLICATION_CREDENTIALS file.
PROJECT_ID = "legal-guardian-ai"
PROCESSOR_ID = "28999c7f79f9582d"
LOCATION = "us"

# --- Helper Function 1: Calls Document AI ---
def parse_document_pdf(file_content: bytes):
    """Processes PDF with your custom Document AI model."""
    try:
        opts = ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
        client = DocumentProcessorServiceClient(client_options=opts)
        processor_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

        raw_document = RawDocument(content=file_content, mime_type="application/pdf")
        request = ProcessRequest(name=processor_name, raw_document=raw_document)
        result = client.process_document(request=request)
        doc = result.document

        entities = []
        for entity in doc.entities:
            entities.append({
                "label": entity.type_, "value": entity.mention_text, "confidence": entity.confidence,
            })
        return {"status": "SUCCESS", "entities": entities, "full_text": doc.text}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

# --- Helper Function 2: Organizes the Results ---
def structure_entities(entities_list):
    """Takes the raw list of entities and groups them for a clean output."""
    grouped_entities = defaultdict(list)
    for entity in entities_list:
        cleaned_value = entity.get("value", "").replace("\n", " ").strip()
        grouped_entities[entity.get("label")].append(cleaned_value)
    
    final_data = {}
    for label, values in grouped_entities.items():
        if len(values) == 1:
            final_data[label] = values[0]
        else:
            final_data[label] = values
    return final_data

# --- API Routes (Endpoints) ---

@app.get("/")
def read_root():
    return {"message": "✅ Legal Guardian AI backend is running."}

@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    """Receives a PDF, gets structured data from Document AI, AND gets a summary from Gemini."""
    try:
        content = await file.read()
        parsed_result = parse_document_pdf(content)
        if parsed_result["status"] == "ERROR":
            return parsed_result

        entities = parsed_result.get("entities", [])
        structured_output = structure_entities(entities)
        full_text = parsed_result.get("full_text", "")
        
        summary = "Summary could not be generated."
        if full_text:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                prompt = f"Please provide a simple, one-paragraph 'plain English' summary of this legal document. Focus on the main purpose and key obligations:\n\n---\n\n{full_text}"
                response = model.generate_content(prompt)
                summary = response.text
            except Exception as e:
                summary = f"Error generating summary: {str(e)}"

        return {
            "status": "SUCCESS", "filename": file.filename, "structured_data": structured_output,
            "summary": summary, "full_text": full_text
        }
    except Exception as e:
        return {"status": "ERROR", "message": f"An unexpected error occurred: {str(e)}"}

@app.post("/ask-question")
async def ask_question(request: dict = Body(...)):
    """Receives document text and a question, and gets an answer from Gemini."""
    document_text = request.get("document_text")
    question = request.get("question")

    if not all([document_text, question]):
        return {"status": "ERROR", "message": "Missing document text or question."}
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        You are a helpful legal assistant. Based ONLY on the provided document text below, answer the user's question.
        If the answer cannot be found in the document, state that clearly. Do not make up information.

        DOCUMENT TEXT:
        ---
        {document_text}
        ---

        USER'S QUESTION:
        "{question}"
        """
        response = model.generate_content(prompt)
        return {"status": "SUCCESS", "answer": response.text}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


