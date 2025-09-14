from fastapi import FastAPI, File, UploadFile
import hashlib
import os

app = FastAPI()

# Directory to save uploaded signatures
SIGNATURE_DIR = "uploaded_signatures"
os.makedirs(SIGNATURE_DIR, exist_ok=True)

@app.post("/upload_signature/")
async def upload_signature(file: UploadFile = File(...)):
    # Save the uploaded file
    file_location = os.path.join(SIGNATURE_DIR, file.filename)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    # Calculate SHA256 hash of the saved file
    sha = hashlib.sha256()
    sha.update(content)
    signature_hash = sha.hexdigest()

    return {"filename": file.filename, "hash": signature_hash}
