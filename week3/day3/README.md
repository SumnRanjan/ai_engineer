# RAG (Retrieval-Augmented Generation) – Employee Policy Assistant

A beginner-friendly Python project that demonstrates how to build a basic Retrieval-Augmented Generation (RAG) application using Sentence Transformers, NumPy, and the Groq API.

The application retrieves relevant information from an employee policy knowledge base using semantic similarity and passes the retrieved information to an LLM to generate an answer.

## 1. Project Overview

Imagine an organization has several employee policies:

- Paid leave policy
- Work-from-home policy
- Gym reimbursement policy
- Internet reimbursement policy
- Notice period policy

Instead of manually searching through these policies, users can ask questions in natural language.

For example:

**User Question:**

```text
How much vacation do I get?
```

**Retrieved Context:**

```text
Employees receive 24 days of paid leave per year.
```

**LLM Response:**

```text
You receive 24 days of paid leave per year.
```

The application retrieves the relevant policy and uses it as context for the LLM.

## 2. What is RAG?

RAG stands for **Retrieval-Augmented Generation**.

It is an AI architecture that combines information retrieval with the text-generation capabilities of an LLM.

It consists of three main stages:

1. **Retrieval:** Find relevant information from an external knowledge base.
2. **Augmentation:** Add the retrieved information to the LLM prompt as context.
3. **Generation:** The LLM generates an answer using the provided context.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Sentence Transformers | Converts text into embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| NumPy | Performs vector calculations |
| Groq API | Provides access to an LLM |
| GPT-OSS-120B | Generates answers |
| python-dotenv | Loads environment variables |

## 4. Understanding the Code Step by Step

### Step 1: Import Required Libraries

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
```

**Purpose of each library:**

- `os`: Access environment variables.
- `Path`: Provides filesystem path utilities (not used elsewhere in this implementation).
- `load_dotenv`: Loads environment variables from the `.env` file.
- `Groq`: Connects to the Groq API.
- `NumPy`: Performs mathematical operations on vectors.
- `SentenceTransformer`: Generates text embeddings.

### Step 2: Initialize the Embedding Model

```python
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
```

This model converts text into numerical vectors.

The `all-MiniLM-L6-v2` model generates embeddings with **384 dimensions**.

For example:

```python
text = "Employees receive 24 days of paid leave per year."

embedding = model.encode(text)

print(embedding.shape)
```

Output:

```text
(384,)
```

Each document is represented by a 384-dimensional vector.

### Step 3: Configure the Groq LLM

```python
groq_model = "openai/gpt-oss-120b"
```

We use GPT-OSS-120B through the Groq API to generate natural-language answers.

### Step 4: Load API Credentials

```python
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND")

client = Groq(api_key=my_api_key)
```

The API key is loaded securely from the `.env` file instead of hardcoding it in the Python script.

### Step 5: Create the Knowledge Base

```python
documents = [
    "Employees receive 24 days of paid leave per year.",

    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",

    "Employees receive Rs 3000 per month for gym reimbursement.",

    "Employees can claim Rs 2000 per month for home internet.",

    "Employees have a 90 day notice period."
]
```

This list acts as our external knowledge base.

It contains five employee policies.

The application uses these documents as its source of information rather than relying entirely on the LLM's pre-trained knowledge.

### Step 6: Generate Document Embeddings

```python
document_embeddings = model.encode(documents)
```

This is an important step in RAG.

The embedding model converts every document into a numerical vector.

Since we have five documents and each embedding has 384 dimensions, the resulting array has this shape:

```text
(5, 384)
```

This means:

- 5 = Number of documents.
- 384 = Dimensions of each document embedding.

These embeddings are generated before the user asks a question.

This avoids generating document embeddings repeatedly for every query.

### Step 7: Implement Cosine Similarity

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
```

Cosine similarity measures how similar two vectors are based on the angle between them.

**Understanding the NumPy operations:**

- `np.dot(a, b)`: Calculates the dot product.
- `np.linalg.norm(a)`: Calculates the magnitude of vector A.
- `np.linalg.norm(b)`: Calculates the magnitude of vector B.

The result is a similarity score.

A higher score generally indicates that two embedding vectors have more similar directions.

### Step 8: Retrieve the Most Relevant Document

```python
def retrieve(qembedding):
    scores = []

    for i, document in enumerate(document_embeddings):

        score = cosine_similarity(qembedding, document)

        scores.append((score, documents[i]))

    scores.sort(reverse=True)

    return scores[0]
```

This function performs semantic search.

Let's understand it line by line.

**1. Initialize an empty list**

```python
scores = []
```

This list stores similarity scores and their corresponding original documents.

**2. Iterate through document embeddings**

```python
for i, document in enumerate(document_embeddings):
```

- `i` represents the document index.
- `document` represents the embedding vector of that document.

**3. Calculate similarity**

```python
score = cosine_similarity(qembedding, document)
```

It compares the user's query embedding with the current document embedding.

**4. Store the score and original document**

```python
scores.append((score, documents[i]))
```

We store a tuple containing:

```python
(similarity_score, original_document)
```

For example:

```python
(0.92, "Employees receive 24 days of paid leave per year.")
```

**5. Sort the documents**

```python
scores.sort(reverse=True)
```

This sorts the tuples in descending order based on their similarity scores.

The most similar document comes first.

**6. Return the best match**

```python
return scores[0]
```

This returns the first tuple containing:

- The highest similarity score.
- The corresponding original document.

For example:

```python
(
    0.92,
    "Employees receive 24 days of paid leave per year."
)
```

### Step 9: Generate an Answer Using the LLM

```python
def ask_llm(question, context):

    system_prompt = f"""
    Answer in one sentence.
    Answer based on context.
    Do not hallucinate.

    Context: {context}
    """

    system_message = {
        "role": "system",
        "content": system_prompt
    }

    message = {
        "role": "user",
        "content": question
    }

    messages = [system_message, message]

    response = client.chat.completions.create(
        model=groq_model,
        messages=messages
    )

    answer = response.choices[0].message.content

    return answer
```

This function is responsible for generating the final answer.

It accepts two arguments:

- `question`: The original question asked by the user.
- `context`: The document retrieved from the knowledge base.

**Understanding the messages:**

System message:

Provides instructions and the retrieved context to the LLM.

User message:

Contains the actual question.

The LLM receives both messages and generates an answer using the retrieved information.

### Step 10: Execute the RAG Pipeline

```python
query = "How much vacation do I get?"

qembedding = model.encode(query)

score, context = retrieve(qembedding)

answer = ask_llm(query, context)

print(f"Answer: {answer}")
```

Let's understand the execution sequence.

| Code | Responsibility |
|---|---|
| `query` | Stores the user's question |
| `model.encode(query)` | Converts the question into an embedding |
| `retrieve(qembedding)` | Searches for the most relevant document |
| `score, context` | Extracts similarity score and document |
| `ask_llm(query, context)` | Sends question and context to the LLM |
| `print(answer)` | Displays the generated answer |

## 5. Complete RAG Architecture

```text
              KNOWLEDGE BASE
                     |
                     v
             Employee Documents
                     |
                     v
             Embedding Model
                     |
                     v
             Document Embeddings
                     |
                     |
                     |
USER QUERY           |
     |               |
     v               |
Embedding Model      |
     |               |
     v               |
Query Embedding      |
     |               |
     +---------------+
             |
             v
      Cosine Similarity
             |
             v
      Semantic Retrieval
             |
             v
      Best Matching Document
             |
             v
      Retrieved Context
             |
             v
    System Prompt + User Query
             |
             v
          Groq API
             |
             v
        GPT-OSS-120B
             |
             v
       Generated Answer
```

## 6. Example Execution

**Input:**

```python
query = "How much vacation do I get?"
```

**Retrieved Context:**

```text
Employees receive 24 days of paid leave per year.
```

**Expected Answer:**

```text
You receive 24 days of paid leave per year.
```

The similarity score is also available:

```python
print(f"Score: {score}")
print(f"Context: {context}")
```

Note: The exact similarity score and LLM response may vary.

## 7. Important Concepts Learned

| Concept | What I Learned |
|---|---|
| Knowledge Base | Stores external information |
| Embeddings | Converts text into numerical vectors |
| Sentence Transformers | Generates semantic embeddings |
| Vector Representation | Represents documents numerically |
| Cosine Similarity | Measures similarity between vectors |
| Semantic Search | Retrieves information based on meaning |
| Retrieval | Finds the most relevant document |
| Context | Provides retrieved information to the LLM |
| Prompt Augmentation | Adds retrieved context to the prompt |
| Generation | LLM generates the final answer |

## 8. Current Project Limitations

This is a basic RAG implementation designed for learning.

Some limitations include:

1. **In-memory storage:** Document embeddings are stored in a NumPy array rather than a persistent vector database.
2. **Top-1 retrieval:** Only the single highest-scoring document is retrieved.
3. **No similarity threshold:** The system always returns a document, even when the query is unrelated to the knowledge base.
4. **No hybrid search:** It uses semantic similarity without keyword-based retrieval.
5. **No document chunking:** Documents are currently stored as predefined text entries.
6. **No reranking:** Retrieved documents are not passed through a separate reranking model.
7. **No zero-vector handling:** The cosine similarity function should handle zero-length vectors to avoid division by zero.
8. **Limited hallucination protection:** Asking the LLM not to hallucinate does not guarantee factual accuracy.

## 9. Future Improvements

- Integrate ChromaDB or FAISS for vector storage.
- Implement top-K document retrieval.
- Add a similarity threshold.
- Implement hybrid search using BM25 and embeddings.
- Support PDF and DOCX document loading.
- Implement text chunking and chunk overlap.
- Explore reranking models.
- Improve retrieval accuracy.
- Build a complete document-based RAG chatbot.

## 10. Installation and Setup

Install dependencies:

```bash
pip install groq python-dotenv numpy sentence-transformers
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Create a `.gitignore` file:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Run the application:

```bash
python full_rag.py
```

The embedding model is downloaded on its first use, so an internet connection is required initially.

## 11. Learning Objective

The objective of this project is to understand how semantic retrieval works in a RAG system.

It demonstrates how:

1. Documents are converted into embeddings.
2. User queries are converted into embeddings.
3. Cosine similarity identifies relevant documents.
4. Retrieved information is passed to an LLM as context.
5. The LLM generates an answer grounded in the retrieved information.

**Key takeaway:** Embeddings help retrieve relevant information, cosine similarity helps rank document relevance, and the LLM uses retrieved context to generate a natural-language response.