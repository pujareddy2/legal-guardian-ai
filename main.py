from collections import defaultdict
import os

from dotenv import load_dotenv
from fastapi import Body, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.api_core.client_options import ClientOptions
from google.cloud.documentai_v1 import (
    DocumentProcessorServiceClient,
    ProcessRequest,
    RawDocument,
)
import google.generativeai as genai

load_dotenv()


def _load_cors_origins():
    configured = os.getenv("CORS_ORIGINS", "").strip()
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=_load_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ID = os.getenv("GCP_PROJECT") or os.getenv("PROJECT_ID") or "legal-guardian-ai"
PROCESSOR_ID = os.getenv("DOCAI_PROCESSOR_ID", "28999c7f79f9582d")
LOCATION = os.getenv("DOCAI_LOCATION", "us")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def parse_document_pdf(file_content: bytes):
    """Processes a PDF with a custom Document AI processor."""
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
            entities.append(
                {
                    "label": entity.type_,
                    "value": entity.mention_text,
                    "confidence": entity.confidence,
                }
            )

        return {"status": "SUCCESS", "entities": entities, "full_text": doc.text}
    except Exception as exc:
        return {"status": "ERROR", "message": str(exc)}


def structure_entities(entities_list):
    """Groups raw entities into a cleaner object for the frontend."""
    grouped_entities = defaultdict(list)
    for entity in entities_list:
        cleaned_value = entity.get("value", "").replace("\n", " ").strip()
        grouped_entities[entity.get("label")].append(cleaned_value)

    final_data = {}
    for label, values in grouped_entities.items():
        final_data[label] = values[0] if len(values) == 1 else values
    return final_data


def _generate_gemini_text(prompt: str):
    if not GEMINI_API_KEY:
        return {
            "status": "ERROR",
            "message": "GOOGLE_API_KEY is not set on the backend.",
        }

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return {"status": "SUCCESS", "text": response.text}
    except Exception as exc:
        return {"status": "ERROR", "message": str(exc)}


@app.get("/")
def read_root():
    return {"message": "Legal Guardian AI backend is running."}


@app.get("/status")
def status_check():
    return {
        "status": "ok",
        "project_id": PROJECT_ID,
        "docai_processor_configured": bool(PROCESSOR_ID),
        "gemini_key_configured": bool(GEMINI_API_KEY),
    }


@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    """Receives a PDF, parses entities, and generates a plain-English summary."""
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
            prompt = (
                "Please provide a simple, one-paragraph plain-English summary of this legal "
                "document. Focus on the main purpose and key obligations:\n\n"
                f"{full_text}"
            )
            summary_result = _generate_gemini_text(prompt)
            if summary_result["status"] == "SUCCESS":
                summary = summary_result["text"]
            else:
                summary = f"Error generating summary: {summary_result['message']}"

        return {
            "status": "SUCCESS",
            "filename": file.filename,
            "structured_data": structured_output,
            "summary": summary,
            "full_text": full_text,
        }
    except Exception as exc:
        return {
            "status": "ERROR",
            "message": f"An unexpected error occurred: {str(exc)}",
        }


@app.post("/ask-question")
async def ask_question(request: dict = Body(...)):
    """Receives document text and a question, and returns a grounded answer."""
    document_text = request.get("document_text")
    question = request.get("question")

    if not all([document_text, question]):
        return {"status": "ERROR", "message": "Missing document text or question."}

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
    result = _generate_gemini_text(prompt)
    if result["status"] == "SUCCESS":
        return {"status": "SUCCESS", "answer": result["text"]}
    return {"status": "ERROR", "message": result["message"]}


