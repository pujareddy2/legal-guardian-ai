Legal Guardian AI - Hackathon Solution
This is the core backend for our hackathon project, Legal Guardian AI. This solution is designed to demystify complex legal documents and provide proactive, AI-powered insights to users.

The core of this project is a FastAPI backend that acts as the central hub for all our services, including powerful Google AI models.

🚀 Key Features Implemented
API Endpoints: A full set of RESTful APIs for the frontend to interact with.

AI Integration: Connections to Google's Gemini AI for analysis and Document AI for document parsing.

Data Storage: The ability to both store and retrieve data from a Firestore database, which is the foundation for our "Crowd-Sourced Legal Risk Index."

"What-If" Simulation: A unique feature that provides predictive analysis based on user questions.

🛠️ Getting Started for Teammates
Follow these steps to get a local copy of the project running on your machine:

Clone the Repository: This gets a copy of the project onto your local machine.

git clone https://github.com/pujareddy2/legal-guardian-ai-hackathon.git
cd legal-guardian-ai-hackathon

Create a Branch: Create a new branch for your work to avoid conflicts.

git checkout -b your-feature-name

Set Up the Python Environment: Create a virtual environment and install all the required libraries from the requirements.txt file.

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Configure Your Credentials: You must create a .env file and a credentials JSON file to securely access Google's services.

Create a file named .env in the project directory.

Add your credentials to the file:

GOOGLE_API_KEY="YOUR_AI_STUDIO_API_KEY"
GOOGLE_APPLICATION_CREDENTIALS="C:\legal-guardian-ai-hackathon\your-credentials-file.json"

Make sure you have your credentials JSON file saved in the project directory.

Run the Server: Start the FastAPI server.

uvicorn main:app --reload --env-file .env

The server will be running at http://127.0.0.1:8000.

📌 API Endpoints
GET /: Welcome message.

GET /status: Checks if the API key is configured.

POST /analyze-document: Upload a .txt or .pdf file.

POST /what-if-simulation: Send a JSON body with a document and a question for AI analysis.

POST /store-document: Upload a file to get an AI-powered summary and save it to Firestore.

GET /get-all-documents: Retrieve all saved document summaries from Firestore.

For any questions, please ask the team lead or refer to the documentation.
