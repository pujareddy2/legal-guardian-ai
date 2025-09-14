from fastapi import FastAPI, UploadFile, Form, Body
from fastapi.responses import StreamingResponse
import os
from google.oauth2 import service_account
from google.cloud import firestore

# Generative AI imports
import google.generativeai as genai
from vertexai.generative_models import GenerativeModel
from google.cloud.documentai_v1 import DocumentProcessorServiceClient, RawDocument

# Presidio redaction
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Accessibility (replace with your implementations)
from accessibility import synthesize_text_to_speech, transcribe_audio_to_text

# --- FastAPI App ---
app = FastAPI()

# --- Google Cloud & Model Configuration ---
PROJECT_ID = "legal-guardian-ai"
PROCESSOR_ID = "28999c7f79f982d"
LOCATION = "us-central1"
GEMINI_MODEL_NAME = "models/gemini-1.5-flash-latest"

# --- API Keys & Credentials ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Database Initialization ---
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credentials_path:
    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        db = firestore.Client(project=PROJECT_ID, credentials=credentials)
    except Exception as e:
        print("Failed to initialize Firestore client:", e)
        db = None
else:
    db = None

# --- Presidio Engines Initialization ---
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def redact_sensitive_data(text):
    results = analyzer.analyze(
        text=text,
        language='en',
        entities=["PERSON", "CREDIT_CARD", "PHONE_NUMBER", "EMAIL_ADDRESS"]
    )
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={"DEFAULT": {"type": "replace", "new_value": "[REDACTED]"}}
    )
    return anonymized.text

def parse_document_pdf(file_content: bytes):
    try:
        client = DocumentProcessorServiceClient()
        processor_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
        raw_document = RawDocument(content=file_content, mime_type="application/pdf")
        request = {"name": processor_name, "raw_document": raw_document}
        response = client.process_document(request=request)
        document = response.document
        return document.text
    except Exception as e:
        return f"ERROR: {str(e)}"

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
        simplified_text = getattr(response, "text", str(response))
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
            parsed_text = parse_document_pdf(content)
        else:
            parsed_text = content.decode("utf-8", errors="replace")

        if parsed_text is None:
            return {"status": "ERROR", "message": "No text parsed from document."}
        if isinstance(parsed_text, str) and parsed_text.lower().startswith("error"):
            return {"status": "ERROR", "message": parsed_text}

        # Redact sensitive data before analysis
        redacted_text = redact_sensitive_data(parsed_text)

        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        prompt = f"Analyze the following legal document and provide a summary of the key points in simple language:\n\n{redacted_text}"
        response = model.generate_content(prompt)
        simplified_summary = getattr(response, "text", str(response))

        return {
            "filename": file.filename,
            "summary": simplified_summary,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/what-if-simulation")
async def what_if_simulation(request: dict = Body(...)):
    try:
        document_text = request.get("document_text")
        user_question = request.get("user_question")
        user_profile = request.get("user_profile", {})

        if not document_text or not user_question:
            return {"status": "ERROR", "message": "Missing 'document_text' or 'user_question'."}

        personalization_details = ""
        if user_profile:
            occupation = user_profile.get('occupation', 'person')
            location = user_profile.get('location', 'their local area')
            personalization_details = f"The user is a {occupation} in {location}."

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
        simulation_result = getattr(response, "text", str(response))

        return {
            "user_question": user_question,
            "simulation_result": simulation_result,
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/store-document")
async def store_document(file: UploadFile, outcome_label: int = Form(...)):
    try:
        if db is None:
            return {"status": "ERROR", "message": "Firestore client not initialized. Check your credentials."}

        content = await file.read()
        parsed_text = content.decode("utf-8", errors="replace")

        # Redact sensitive data before processing
        redacted_text = redact_sensitive_data(parsed_text)

        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        prompt = f"Summarize this document:\n\n{redacted_text}"
        response = model.generate_content(prompt)
        summary = getattr(response, "text", str(response))

        doc_ref = db.collection("legal-documents").document()
        doc_ref.set({
            "filename": file.filename,
            "summary": summary,
            "outcome_label": outcome_label,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        return {
            "document_id": doc_ref.id,
            "message": "Document, summary, and label saved successfully.",
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.get("/get-all-documents")
def get_all_documents():
    try:
        if db is None:
            return {"status": "ERROR", "message": "Firestore client not initialized. Check your credentials."}
        docs = db.collection('legal-documents').stream()
        documents = []
        for doc in docs:
            doc_data = doc.to_dict()
            created_at = doc_data.get("created_at")
            documents.append({
                "document_id": doc.id,
                "filename": doc_data.get("filename"),
                "summary": doc_data.get("summary"),
                "created_at": created_at.isoformat() if created_at else None
            })
        return {
            "status": "SUCCESS",
            "count": len(documents),
            "documents": documents
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/text-to-speech")
async def get_audio_from_text(request: dict = Body(...)):
    try:
        simplified_text = request.get("simplified_text")
        if not simplified_text:
            return {"status": "ERROR", "message": "Missing 'simplified_text' in the request."}

        audio_content = synthesize_text_to_speech(simplified_text)
        if not isinstance(audio_content, (bytes, bytearray)):
            return {"status": "ERROR", "message": "synthesize_text_to_speech must return bytes audio content."}

        return StreamingResponse(
            iter([audio_content]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=output.mp3"}
        )
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/speech-to-text")
async def transcribe_audio_file(file: UploadFile):
    try:
        audio_content = await file.read()
        transcribed_text = transcribe_audio_to_text(audio_content)

        if transcribed_text:
            return {
                "status": "SUCCESS",
                "transcribed_text": transcribed_text
            }
        else:
            return {
                "status": "ERROR",
                "message": "Transcription failed or no text found."
            }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

# Optional: Include routers if modules exist
try:
    from legal_risk_index import router as risk_router
    app.include_router(risk_router)
except Exception as e:
    print("Could not include legal_risk_index router:", e)

try:
    from predictive_legal_outcome_model import router as plom_router
    app.include_router(plom_router)
except Exception as e:
    print("Could not include predictive_legal_outcome_model router:", e)

try:
    from human_in_loop import router as hil_router
    app.include_router(hil_router)
except Exception as e:
    print("Could not include human_in_loop router:", e)
