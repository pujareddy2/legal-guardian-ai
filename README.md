Legal Guardian AI - Hackathon Solution
This is the core backend for our hackathon project, Legal Guardian AI. This solution is designed to demystify complex legal documents and provide proactive, AI-powered insights to users.

The core of this project is a FastAPI backend that acts as the central hub for all our services, including powerful Google AI models.

🚀 Key Features Implemented
Document Analysis: An endpoint that receives a document, parses it using Google's Document AI, and provides a simplified summary using the Gemini model.

"What-If" Simulation: An endpoint that takes a legal document and a user's question, then provides a predictive analysis of the legal consequences.

API Health Check: A simple endpoint to confirm that the server and API keys are working correctly.

🛠️ Getting Started (For Teammates)
Follow these steps to get a local copy of the project running on your machine:

Clone the Repository:

git clone https://github.com/pujareddy2/legal-guardian-ai-hackathon.git
cd legal-guardian-ai-hackathon

Set Up the Python Environment: Create a virtual environment to manage dependencies and install all the required libraries.

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Configure Your API Key: You must set your Google AI Studio API Key as an environment variable called GOOGLE_API_KEY.

On Windows (PowerShell): $env:GOOGLE_API_KEY = "YOUR_API_KEY"

On macOS/Linux: export GOOGLE_API_KEY="YOUR_API_KEY"

(Note: You will also need to configure your Google Cloud credentials for Document AI, as outlined in the project documentation.)

Run the Server: Start the FastAPI server.

uvicorn main:app --reload

The server will be running at http://127.0.0.1:8000.

📌 API Endpoints
GET /: Welcome message.

GET /status: Checks if the API key is working.

POST /analyze-document: Upload a .txt or .pdf file.

POST /what-if-simulation: Send a JSON body with a document and question for AI analysis.

