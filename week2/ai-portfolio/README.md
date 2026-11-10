# AI Resume Chatbot 🤖

An AI-powered Resume Chatbot built using **Python, FastAPI, Groq, Pydantic, and PyPDF**. The application extracts information from a candidate's PDF resume, converts it into structured data using an LLM, and answers HR interview questions based on the candidate's profile.

## 🚀 Features

- **PDF Resume Extraction:** Extracts text from PDF resumes using PyPDF.
- **AI Resume Parsing:** Uses Groq LLM to extract structured candidate information.
- **Structured Data Validation:** Uses Pydantic models to validate parsed resume data.
- **AI Candidate Chatbot:** Answers HR interview questions based on resume information.
- **Hallucination Control:** Instructs the LLM to answer only using available resume information.
- **REST API:** Provides endpoints using FastAPI.
- **Interactive API Documentation:** Test endpoints through Swagger UI.

## 🛠️ Tech Stack

- Python
- FastAPI
- Groq API
- Pydantic
- PyPDF
- Uvicorn
- python-dotenv

## 📁 Project Structure

```text
ai-portfolio/
│
├── backend/
│   ├── main.py
│   └── suman-sde.pdf
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Setup

### 2. Create a virtual environment

```bash
uv venv --python 3.14
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
uv sync
```

Alternatively, install the packages manually:

```bash
uv add python-dotenv fastapi groq pydantic pypdf python-docx uvicorn
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

### 6. Run the application

From the project root directory:

```bash
uv run uvicorn backend.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## 📡 API Endpoints

### 1. Home

**GET /**

Checks whether the API is running.

Example response:

```json
{
  "message": "AI Portfolio API is running"
}
```

### 2. Chat with Candidate

**POST /chat**

Accepts an HR interview question and generates an AI-powered response using the candidate's resume.

Request body:

```json
{
  "question": "Tell me about your technical skills."
}
```

Example response:

```json
{
  "answer": "The candidate has experience with JavaScript, React.js, Node.js, Python, and other technologies mentioned in the resume."
}
```

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧠 How It Works

1. The application reads the candidate's PDF resume.
2. PyPDF extracts the text from the document.
3. Groq LLM analyzes the extracted resume content.
4. The LLM converts the information into structured JSON.
5. Pydantic validates the extracted information against the Resume schema.
6. HR submits questions through the `/chat` endpoint.
7. Groq generates answers using the structured candidate profile.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to access Groq LLM services |

**Important:** Never commit your `.env` file or expose your API key publicly.

## 🔮 Future Improvements

- Upload resumes dynamically instead of using a fixed PDF.
- Support multiple candidate resumes.
- Cache parsed resume data to reduce API calls.
- Add conversation history.
- Build a frontend chatbot interface.
- Add authentication and authorization.
- Deploy the application to a cloud platform.
