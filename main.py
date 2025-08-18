from fastapi import FastAPI, UploadFile
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import google.generativeai as genai
import os
from google.cloud import firestore
from google.oauth2 import service_account

# Create an instance of the FastAPI class.
app = FastAPI()

# --- Google Cloud & Model Configuration ---
PROJECT_ID = "legal-guardian-ai"
PROCESSOR_ID = "28999c7f79f982d"
LOCATION = "us-central1"
GEMINI_MODEL_NAME = "models/gemini-1.5-flash-latest"

# --- API Keys & Credentials ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Database Initialization ---
# Get the path to your credentials file from the environment variable.
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Check if the credentials path exists and create a Firestore client.
if credentials_path:
    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        db = firestore.Client(project=PROJECT_ID, credentials=credentials)
    except Exception:
        db = None
else:
    # Fallback in case the credentials are not found.
    db = None

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
    Simulates a "what-if" scenario based on document text and a user's question,
    with an optional user profile for personalization.
    """
    try:
        document_text = request.get("document_text")
        user_question = request.get("user_question")
        user_profile = request.get("user_profile", {}) # Get profile or an empty dict

        if not document_text or not user_question:
            return {"status": "ERROR", "message": "Missing 'document_text' or 'user_question' in the request."}

        # Dynamically build the prompt based on the user_profile.
        personalization_details = ""
        if user_profile:
            personalization_details = f"The user is a {user_profile.get('occupation', 'person')} in {user_profile.get('location', 'their local area')}."

        # Craft a specific prompt for the AI to handle the simulation.
        prompt = f"""
        As an AI legal assistant, analyze the following legal document and answer the user's "what-if" question in simple, easy-to-understand language.
        {personalization_details}
        Provide a clear explanation of the legal consequences based on the provided text.

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

@app.post("/store-document")
async def store_document(file: UploadFile):
    """
    Processes and stores a document in Firestore.
    """
    try:
        # Check if the database client is initialized.
        if db is None:
            return {"status": "ERROR", "message": "Firestore client not initialized. Check your credentials."}

        content = await file.read()
        parsed_text = content.decode("utf-8")
        
        # Use Gemini to generate a summary to save.
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        prompt = f"Summarize this document:\n\n'{parsed_text}'"
        response = model.generate_content(prompt)
        summary = response.text

        # Create a document in Firestore.
        doc_ref = db.collection("legal-documents").document()
        doc_ref.set({
            "filename": file.filename,
            "summary": summary,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        return {
            "document_id": doc_ref.id,
            "message": "Document and summary saved successfully.",
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
    
@app.get("/get-all-documents")
def get_all_documents():
    """
    Retrieves all stored documents from the Firestore database.
    """
    try:
        if db is None:
            return {"status": "ERROR", "message": "Firestore client not initialized. Check your credentials."}

        # Query the 'legal-documents' collection.
        docs = db.collection('legal-documents').stream()
        
        documents = []
        for doc in docs:
            doc_data = doc.to_dict()
            documents.append({
                "document_id": doc.id,
                "filename": doc_data.get("filename"),
                "summary": doc_data.get("summary"),
                "created_at": doc_data.get("created_at").isoformat() if doc_data.get("created_at") else None
            })

        return {
            "status": "SUCCESS",
            "count": len(documents),
            "documents": documents
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

