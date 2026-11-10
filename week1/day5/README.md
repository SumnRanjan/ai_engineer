# AI Resume Matcher

An AI-powered resume screening project built with Python, Groq, and
Pydantic. It extracts requirements from a job description, parses
candidate resumes, compares candidate profiles with the requirements,
and ranks candidates by an AI-generated match score.

## Features

-   Extracts structured job requirements from an embedded job
    description.
-   Reads resumes in PDF and DOCX formats.
-   Extracts candidate details: name, email, phone, experience, skills,
    education, projects, and certifications.
-   Compares each candidate profile with the job requirements using an
    LLM.
-   Generates a match score and matching details.
-   Displays the top 2 and lowest 2 candidates.

## Tech Stack

-   Python
-   Groq API
-   Pydantic
-   pypdf
-   python-docx
-   python-dotenv
-   uv

## Project Structure

``` text
ai-resume-matcher/
├── .venv/
├── .env
├── main.py
├── pyproject.toml
├── uv.lock
└── resumes/
    ├── candidate-1.pdf
    ├── candidate-2.docx
    └── ...
```

The application is implemented in a single Python file, `main.py`. Put
candidate resumes in the `resumes` directory.

## Requirements

-   Python
-   uv
-   A Groq API key

## Setup

### 1. Create the project

``` powershell
mkdir ai-resume-matcher
cd ai-resume-matcher
uv init
```

### 2. Install dependencies

``` powershell
uv add python-dotenv groq pydantic pypdf python-docx
```

### 3. Configure the API key

Create a `.env` file in the project root:

``` env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your actual Groq API key. Do not commit
`.env` or share your key.

### 4. Create the resumes directory

``` powershell
mkdir resumes
```

Place candidate `.pdf` and `.docx` files inside this directory.

### 5. Add the code

Save the application code in `main.py`. The job description is currently
embedded in the `job_description` variable in that file. Replace it when
evaluating candidates for another role.

## Run

From the project root:

``` powershell
uv run python main.py
```

The application extracts the job requirements, processes supported files
in `resumes/`, parses each resume, generates a match score, sorts
candidates, and prints the top 2 and lowest 2 results.

## How It Works

### Part 1 --- Job Description Extraction

The `jobD` Pydantic model defines the expected job information:

-   Role
-   Required skills
-   Preferred skills
-   Minimum experience
-   Education requirements
-   Responsibilities

The Groq model extracts these fields from the job description and
returns JSON. The JSON is parsed and validated with Pydantic.

### Part 2 --- Resume Parsing and Matching

The `Resume` model defines the candidate information:

-   Name, email, and phone
-   Total experience in years
-   Skills
-   Work experiences and internships
-   Education
-   Projects
-   Certifications

`parse_resume()` extracts this information from resume text.
`final_score()` asks the LLM to compare the parsed candidate profile
with the extracted job requirements and return a score with details.

### Part 3 --- Reading Files and Ranking Candidates

-   `read_pdf()` extracts text using `pypdf`.
-   `read_docx()` extracts paragraph text and table-cell text using
    `python-docx`.
-   `read_resume()` chooses a reader based on the file extension.
-   The program processes each PDF or DOCX file in `resumes/`.
-   A five-second pause is added between LLM calls.
-   Results are sorted by score in descending order.

## Limitations and Responsible Use

-   Only PDF and DOCX files are supported.
-   Scanned/image-only PDFs may not produce text because OCR is not
    implemented.
-   The match score is an LLM-generated estimate, not an objective
    measure of ability.
-   Review extracted details and scoring explanations. Do not use this
    tool as the sole basis for hiring decisions.
-   Obtain appropriate permission before sending resumes to an external
    API, and protect candidate personal information.

## Future Improvements

-   Load job descriptions from a separate file or user input.
-   Add OCR for scanned resumes.
-   Export rankings to CSV or Excel.
-   Add a web interface for resume uploads.
-   Make scoring criteria configurable and evidence-based.
-   Add robust handling for unreadable files and invalid model
    responses.
