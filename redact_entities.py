import re

def redact_entities_simple(text):
    """
    Redacts common personally identifiable information (PII) from text
    using simple regex-based heuristics.
    This includes example person names, emails, and phone numbers.
    """

    redacted_text = text

    # Example redaction for the name 'John Doe' (add more names as needed)
    redacted_text = re.sub(r'\bJohn Doe\b', 'PERSON', redacted_text, flags=re.IGNORECASE)

    # Redact email addresses
    redacted_text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', 'EMAIL', redacted_text)

    # Redact phone numbers (basic pattern for digits, spaces, dashes, optional +)
    redacted_text = re.sub(r'(\+?\d[\d\-\s]{7,}\d)', 'PHONE_NUMBER', redacted_text)

    return redacted_text

if __name__ == "__main__":
    SAMPLE_TEXT = "My name is John Doe. Contact me at john@example.com or 555-123-4567."
    print("Original:")
    print(SAMPLE_TEXT)
    print("\nRedacted:")
    print(redact_entities_simple(SAMPLE_TEXT))
