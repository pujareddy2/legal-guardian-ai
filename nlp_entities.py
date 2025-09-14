import re

def redact_entities(text):
    """
    Simple PII redaction using regex.
    Replaces names (example), emails, and phone numbers.
    """

    redacted_text = text

    # Example: redact 'Barack Obama' explicitly; you can list more names or patterns.
    redacted_text = re.sub(r'\bBarack Obama\b', 'PERSON', redacted_text, flags=re.IGNORECASE)

    # Redact emails
    redacted_text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', 'EMAIL', redacted_text)

    # Redact phone numbers (simple pattern)
    redacted_text = re.sub(r'(\+?\d[\d\-\s]{7,}\d)', 'PHONE_NUMBER', redacted_text)

    return redacted_text


if __name__ == "__main__":
    sample_text = "Barack Obama was the 44th President of the United States. Contact at barack.obama@example.com or +1 555-123-4567."
    print("Original:")
    print(sample_text)
    print("\nRedacted:")
    print(redact_entities(sample_text))
