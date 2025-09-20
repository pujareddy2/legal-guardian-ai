from google.cloud import documentai

# Your processor details
project_id = "legal-guardian-ai"
processor_id = "28999c7f79f9582d"
location = "us"

client = documentai.DocumentProcessorServiceClient()

# Construct the full resource name
name = client.processor_path(project_id, location, processor_id)

# ---------------- Processor Details ----------------
processor = client.get_processor(name=name)
print("Processor name:", processor.name)
print("Processor display name:", processor.display_name)
print("Processor type:", processor.type_)
print("Processor state:", processor.state)

# ---------------- Process a PDF ----------------
file_path = "test/sample.pdf"  # put your PDF inside a 'test' folder

with open(file_path, "rb") as f:
    file_content = f.read()

document = {"content": file_content, "mime_type": "application/pdf"}
request = {"name": name, "raw_document": document}

result = client.process_document(request=request)
doc = result.document

print("\n✅ Document processing complete.")
print(f"Text length: {len(doc.text)} characters")

if doc.entities:
    print("\nEntities found:")
    for entity in doc.entities:
        print(f" - {entity.type_}: {entity.mention_text}")
else:
    print("\n(No entities were extracted)")
