Legal Guardian AI
A Proactive AI Legal Assistant and Financial Guardian
📄 Project Overview
Legal Guardian AI is a revolutionary hackathon solution designed to empower individuals and small businesses by demystifying complex legal documents. The platform leverages Google's advanced generative AI to provide clear, actionable insights and proactive protection against legal and financial risks.

Our core backend is built with FastAPI, serving as a robust and scalable foundation that integrates multiple Google Cloud services to deliver an intelligent, secure, and user-friendly experience.

✨ Key Features
Intelligent Document Processing: Utilizes Google's Document AI for accurate parsing of various legal documents and Gemini AI for generating simplified summaries and analyses.

Predictive "What-If" Simulations: A unique feature that allows users to ask hypothetical questions about a contract. The AI provides a detailed, predictive analysis of potential consequences based on the document's clauses and a personalized user profile.

Secure Data Storage: Seamlessly integrates with a Firestore database to securely store document summaries. This lays the groundwork for advanced features like a crowd-sourced legal risk index.

Robust API Endpoints: A comprehensive suite of RESTful APIs provides a clear interface for the frontend application to interact with the core logic.

🚀 Getting Started for the Development Team
This project is designed for collaborative development. Follow these steps to set up your local environment and begin contributing.

Clone the Repository:

git clone https://github.com/pujareddy2/legal-guardian-ai-hackathon.git
cd legal-guardian-ai-hackathon


Create Your Development Branch:

git checkout -b <your-feature-name>


Set Up the Python Environment:

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt


Configure Your Credentials: Securely store your API keys and credentials.

Create a file named .env in the project directory.

Add your credentials to the file:

GOOGLE_API_KEY="YOUR_AI_STUDIO_API_KEY"
GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\credentials-file.json"


Run the Server:

uvicorn main:app --reload --env-file .env


The server will be running at http://127.0.0.1:8000. You can view the interactive API documentation at http://127.0.0.1:8000/docs.

📌 API Reference
Method

Endpoint

Description

GET

/

A welcome message to confirm the server is running.

GET

/status

Checks if the API key and other configurations are correctly set.

POST

/analyze-document

Upload a file (.txt or .pdf) to receive an AI-generated summary.

POST

/what-if-simulation

Send a JSON payload with document text and a user's question for predictive analysis.

POST

/store-document

Upload a file to get an AI summary and save the data to Firestore.

GET

/get-all-documents

Retrieves a list of all stored document summaries from Firestore.

