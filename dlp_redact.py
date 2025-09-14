from google.cloud import dlp_v2
from google.cloud.dlp_v2 import types

def redact_pii(text: str, project_id: str) -> str:
    # Initialize DLP client
    client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}"

    # Configure info types to detect
    info_types = [
        types.InfoType(name="EMAIL_ADDRESS"),
        types.InfoType(name="PHONE_NUMBER"),
        types.InfoType(name="PERSON_NAME"),
    ]

    inspect_config = types.InspectConfig(info_types=info_types)

    # Define how to transform detected info types: replace with type name
    replace_transformation = types.PrimitiveTransformation(
        replace_with_info_type_config=types.ReplaceWithInfoTypeConfig()
    )

    info_type_transformation = types.InfoTypeTransformation(
        info_types=info_types,
        primitive_transformation=replace_transformation,
    )

    info_type_transformations = types.InfoTypeTransformations(
        transformations=[info_type_transformation]
    )

    deidentify_config = types.DeidentifyConfig(
        info_type_transformations=info_type_transformations
    )

    # Item to be inspected and deidentified
    item = {"value": text}

    # Call the DLP API
    response = client.deidentify_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "deidentify_config": deidentify_config,
            "item": item,
        }
    )

    return response.item.value


if __name__ == "__main__":
    import os

    # Replace this with your Google Cloud project ID
    PROJECT_ID = "legal-guardian-ai"

    # Example text containing PII to redact
    sample_text = "My name is John Doe. Email: john@example.com. Phone: 555-123-4567."

    # Run redaction function and print result
    redacted_text = redact_pii(sample_text, PROJECT_ID)
    print(redacted_text)
