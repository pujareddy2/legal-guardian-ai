import requests

def call_lawyer_service(message, specialization="criminal", language="en", jurisdiction="india"):
    """
    Calls an external Lawyer-on-Demand API using RapidAPI.

    Args:
        message (str): User's legal question or request.
        specialization (str): Lawyer specialization.
        language (str): Language for the response (default English "en").
        jurisdiction (str): Legal jurisdiction applicable (default India).

    Returns:
        dict or None: JSON response from API or None if error occurs.
    """
    url = "https://ai-lawyer-online-legal-advice-attorney-consultation.p.rapidapi.com/chat"
    params = {"noqueue": "1"}  # Added query parameter as in curl command

    payload = {
        "message": message,
        "specialization": specialization,
        "language": language,
        "jurisdiction": jurisdiction
    }

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "ai-lawyer-online-legal-advice-attorney-consultation.p.rapidapi.com",
        "x-rapidapi-key": "2ac8ab2b02msh7ccb10e276e6c02p190474jsnac326b9571e9"  # Use your actual key here
    }

    try:
        response = requests.post(url, params=params, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error calling lawyer service: {e}")
        return None

def pretty_print_lawyer_response(api_response):
    try:
        result = api_response.get('result', {})
        response = result.get('response', {})

        message = response.get('message', 'No message available')
        legal_refs = response.get('legalReferences', [])
        recommendations = response.get('recommendations', [])

        print("\n--- Lawyer Service Response ---\n")
        print("Message:\n", message)

        if legal_refs:
            print("\nLegal References:")
            for ref in legal_refs:
                print(f" - {ref}")

        if recommendations:
            print("\nRecommendations:")
            for rec in recommendations:
                print(f" - {rec}")
        print("\n----------------------------\n")

    except Exception as e:
        print("Error parsing lawyer response:", str(e))

# Example usage
if __name__ == "__main__":
    query = "What are the legal rights of a person arrested in India?"
    result = call_lawyer_service(query)

    if result:
        pretty_print_lawyer_response(result)
    else:
        print("Failed to get lawyer service info")
