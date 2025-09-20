import os
import json
from google.cloud import documentai

# -------------------------------
# 🔑 Your processor details
# -------------------------------
project_id = "legal-guardian-ai"
processor_id = "405243f97e7c8f7b"   # <-- replace with Contract Parser ID later
location = "us"

client = documentai.DocumentProcessorServiceClient()
name = client.processor_path(project_id, location, processor_id)

# -------------------------------
# 📂 Input / Output folders
# -------------------------------
sample_folder = "sample"
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

# -------------------------------
# 🔁 Process all PDFs in /sample/
# -------------------------------
for filename in os.listdir(sample_folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(sample_folder, filename)
        print(f"\n📄 Processing: {filename}")

        # Read file
        with open(file_path, "rb") as f:
            file_content = f.read()

        document = {"content": file_content, "mime_type": "application/pdf"}
        request = {"name": name, "raw_document": document}

        try:
            result = client.process_document(request=request)
            doc = result.document

            print(f"✅ Done. Extracted text length: {len(doc.text)} characters")

            # -------------------------------
            # 💾 Save plain text
            # -------------------------------
            text_path = os.path.join(output_folder, f"{filename}.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(doc.text)

            # -------------------------------
            # 💾 Save entities (if any)
            # -------------------------------
            entities = [
                {"type": e.type_, "mention_text": e.mention_text}
                for e in doc.entities
            ]
            json_path = os.path.join(output_folder, f"{filename}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(entities, f, indent=2, ensure_ascii=False)

            print(f"💾 Saved to: {text_path} and {json_path}")

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
