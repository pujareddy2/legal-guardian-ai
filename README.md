# 📄 Legal Guardian AI: A Proactive AI Legal Assistant and Financial Guardian

Legal Guardian AI is a revolutionary hackathon solution designed to **empower individuals and small businesses** by demystifying complex legal documents. The platform leverages **Google's advanced generative AI** to provide clear, actionable insights and proactive protection against legal and financial risks.

The backend is built with **FastAPI**, serving as a robust and scalable foundation that integrates multiple **Google Cloud services** to deliver an intelligent, secure, and user-friendly experience.

***

## ✨ Key Features

- **Intelligent Document Processing**  
  Uses **Google Document AI** for parsing legal documents and **Gemini AI** for generating simplified summaries and analyses.

- **Predictive "What-If" Simulations**  
  Users can ask hypothetical questions about a contract. The AI provides predictive analysis of potential consequences based on clauses and a personalized user profile.

- **Secure Data Storage**  
  Seamless integration with **Firestore** to securely store document summaries, enabling features like a crowd-sourced legal risk index.

- **Robust API Endpoints**  
  A complete suite of RESTful APIs for frontend integration with the backend.

***

## 🚀 Getting Started (For Developers)

Follow the steps below to set up the development environment.

### 1. Clone the Repository
```bash
git clone https://github.com/pujareddy2/legal-guardian-ai-hackathon.git
cd legal-guardian-ai-hackathon
```

### 2. Create a Development Branch
```bash
git checkout -b <your-feature-name>
```

### 3. Set Up Python Virtual Environment
```bash
python -m venv venv
```
Activate the environment:
- **Windows (PowerShell):**
  ```bash
  .\venv\Scripts\Activate.ps1
  ```
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Your Credentials
Create a `.env` file in the project root directory and add your credentials:
```env
GOOGLE_API_KEY="YOUR_AI_STUDIO_API_KEY"
GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\credentials-file.json"
```
### 6. Set Up the Frontend (React)
This installs all the JavaScript libraries.
```bash
npm install
```

### 7. Run the Development Server
You need to run two servers in two separate terminals from your project folder.
Terminal 1: Start the Backend
```bash
uvicorn main:app --reload
```
Terminal 2: Start the Frontend
```bash
npm start
```
The server will be available at:  
👉 `http://127.0.0.1:8000`

Interactive API documentation:  
👉 `http://127.0.0.1:8000/docs`

The Frontend Website:
👉 `http://localhost:3000`

***

## 📌 API Reference

### **GET /**
- **Description:** Welcome message to confirm the server is running.

### **GET /status**
- **Description:** Checks if the API key and other configurations are correctly set.

### **POST /analyze-document**
- **Description:** Upload a file (`.txt` or `.pdf`) to receive an AI-generated summary.

### **POST /what-if-simulation**
- **Description:** Send a JSON payload with document text and a user's question for predictive analysis.

### **POST /store-document**
- **Description:** Upload a file to get an AI summary and store the data in Firestore.

### **GET /get-all-documents**
- **Description:** Retrieves a list of all stored document summaries from Firestore.

***

## 🤖 AI/ML Ops Features & Implementation

### 1. Environment Setup
- Created a **Python virtual environment** (`venv`) and installed dependencies from `requirements.txt`.
- Configured `.env` with Google Cloud credentials:
```env
GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
GCP_PROJECT="your-gcp-project-id"
```

### 2. Firestore Setup
- Connected the application to **Google Firestore**.
- Added sample documents to the `legal-documents` collection (case summaries, outcomes).
- Verified documents and their IDs using:
```bash
python list_firestore_docs.py
```

### 3. Predictive Legal Outcome Model
- Trained and saved ML models:
  - `legal_outcome_model.pkl`
  - `legal_outcome_vectorizer.pkl`
- Integrated models with FastAPI (`main.py`) to enable endpoint predictions.
- Tested `/predict-outcome` endpoint that returns predictions such as:
  - `"civil"`
  - `"criminal"`
  - `"won"`
  - `"lost"`

### 4. Risk Index Analysis
- Implemented `/risk-index` endpoint in `legal_risk_index.py`.
- Verified via **Swagger UI** returning total document count.
- Risk Index currently empty; next step is adding contract-like text to Firestore for real risk percentages.

### 5. Human-in-the-Loop Feedback
- Implemented `/feedback` endpoint in `human_in_loop.py`.
- Feedback posting tested using PowerShell:
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/feedback -Method POST -Body '{"doc_id": "123", "feedback": "Useful summary"}'
```

### 6. API Testing
- Server run command:
```bash
uvicorn main:app --reload --env-file .env
```
- Verified Firestore entries for documents and feedback.

### 7. Working Files in Repository

| File                         | Purpose                          |
|------------------------------|---------------------------------|
| `add_sample_data.py`          | Inserts initial Firestore documents |
| `train_predictive_model.py`   | Trains and saves ML models       |
| `predictive_legal_outcome_model.py` | Prediction logic for outcomes |
| `legal_risk_index.py`         | Computes clause-based risk index |
| `human_in_loop.py`            | Handles human feedback           |
| `check_feedback.py`           | Verifies feedback entries        |
| `list_firestore_docs.py`      | Lists all Firestore documents    |
| `verify_firestore_data.py`    | Checks inserted data correctness |
| `main.py`                    | FastAPI entry point with all routes |
| `contract.txt`               | Sample contract for testing risk clauses |

### 8. Key Implementations
- **ML model integration:** Trained and integrated with FastAPI.
- **Outcome prediction:** Fully functional endpoint.
- **Risk Index:** Live endpoint needing realistic contract data.
- **Human feedback loop:** Tested and stored in Firestore.
- **Firestore scripts:** Insert, verify, and fetch documents and feedback.

***

## 🛡 Privacy, Security, and Integrations

Run the following commands and scripts to enable privacy, security features, and integrations:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

setx GOOGLE_API_KEY "AIzaSyDfrf2FlKVlG5D168azTpJoIyBXM93XoJc"
setx GOOGLE_APPLICATION_CREDENTIALS "C:\legal_guardian_ai\legal-guardian-ai-f17d58e71811.json"
```

1) **Dynamic Privacy Shield (PII Redaction)**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\ADMIN\legal-guardian-ai-hackathon\legal-guardian-ai-f17d58e71811.json"
python redact_entities.py
```

2) **Homomorphic Encryption (HE) Integration**
```bash
python homomorphic_encryption_test.py
```

3) **Blockchain-Based Document Integrity**
```bash
python blockchain.py
```

4) **Biometric Signature Verification**
Run app and upload images/signature via API docs:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Select images and upload signature.

5) **External Service Integrations (Mocked APIs for Lawyer Networks)**
```bash
python lawyer_api_integration.py
```

6) Additional NLP entity processing:
```bash
python nlp_entities.py
```

***

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)  
- **AI Models:** Google Generative AI (Gemini), Google Document AI  
- **Database:** Google Firestore  
- **Hosting/Infra:** Google Cloud Platform  

***

## 👥 Contribution Guidelines

1. Fork the repo and create a new feature branch.  
2. Commit your changes with clear messages.  
3. Push the branch and create a Pull Request.

***

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

***

## 💡 Acknowledgements

- **Google Cloud AI** for providing advanced AI capabilities.  
- **FastAPI** for making backend development fast and efficient.

***

This combined README merges project introduction, features, setup instructions, technical and AI/ML operation details, plus privacy/security implementation instructions for ease of reference and development guidance.
