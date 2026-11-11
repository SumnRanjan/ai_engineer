# RAG Implementation using Qdrant, Sentence Transformers & Groq

A Retrieval-Augmented Generation (RAG) application that retrieves relevant information from a vector database using semantic similarity and metadata filtering, then generates answers using an LLM.

## 1. What is RAG?

RAG (Retrieval-Augmented Generation) is a technique that combines information retrieval with Large Language Models (LLMs).

Instead of depending entirely on the LLM's pre-trained knowledge, RAG retrieves relevant information from an external knowledge source and provides it as context to the LLM.

This helps the LLM generate answers based on the provided information.

## 2. Technologies Used

- **Python** – Main programming language.
- **Qdrant Cloud** – Vector database for storing and searching embeddings.
- **Sentence Transformers** – Converts text into numerical vectors (embeddings).
- **all-MiniLM-L6-v2** – Embedding model that generates 384-dimensional vectors.
- **Groq** – LLM inference API.
- **OpenAI GPT-OSS 120B** – Language model used for answer generation.
- **Python-dotenv** – Manages environment variables.

## 3. How RAG Works

The RAG pipeline consists of two major stages:

### A. Indexing (Document Processing)

This stage prepares documents and stores them in the vector database.

1. Load documents from `knowledge.json`.
2. Extract the text from each document.
3. Convert documents into embeddings using Sentence Transformers.
4. Each document is represented as a 384-dimensional vector.
5. Store the vectors and their metadata (payload) in Qdrant.
6. Create a payload index on the category field for efficient metadata filtering.

**Example:**

Input document:

```json
{
  "text": "Employees receive 20 days of annual leave.",
  "category": "leave"
}
```

The embedding model converts the document text into a numerical vector.

Qdrant stores:

- Document ID
- Embedding vector
- Payload (original text and category)

### B. Retrieval (Question Processing)

When a user asks a question, the retrieval process begins.

1. Receive the user's question.
2. Convert the question into an embedding using the same Sentence Transformer model.
3. Send the query vector to Qdrant.
4. Qdrant compares the query vector with stored document vectors using cosine similarity.
5. Apply metadata filters to restrict the search to a specific category.
6. Retrieve the top matching documents.

**Important:** Both the stored documents and the user's question are converted into vectors using the same embedding model.

### C. Generation (LLM Processing)

After retrieving relevant documents:

1. Extract the original text from the retrieved Qdrant payloads.
2. Combine the retrieved documents into a context string.
3. Pass the original question and retrieved context to the LLM.
4. The LLM generates an answer based on the provided context.

## 4. RAG Architecture

```text
             INDEXING STAGE
                    |
             knowledge.json
                    |
                    v
             Extract Document Text
                    |
                    v
           Sentence Transformer
                    |
                    v
           Document Embeddings
             (384 Dimensions)
                    |
                    v
              Qdrant Cloud
          (Vectors + Payloads)
                    |
                    |
                    |
             RETRIEVAL STAGE
                    |
                    v
              User Question
                    |
                    v
           Sentence Transformer
                    |
                    v
             Query Embedding
             (384 Dimensions)
                    |
                    v
              Qdrant Search
                    |
          Cosine Similarity
                    |
          Metadata Filtering
                    |
                    v
          Top Matching Documents
                    |
                    v
             Retrieved Context
                    |
                    v
                    LLM
           (Question + Context)
                    |
                    v
              Final Answer
```

## 5. Important Concepts

### Embeddings

Embeddings convert text into numerical vector representations.

In this project, we use `all-MiniLM-L6-v2`, which generates 384-dimensional vectors.

We create embeddings for:
- Documents during indexing.
- User questions during retrieval.

### Cosine Similarity

Cosine similarity is used to measure how similar two vectors are based on the angle between them.

Qdrant uses cosine distance to identify documents that are semantically similar to the user's question.

### Vector Database

Qdrant stores document embeddings along with their payloads.

It allows us to search for semantically similar documents using query vectors.

### Payload

Payload is additional information stored alongside a vector.

Example:

```python
payload = {
    "text": "Employees receive 20 days of annual leave.",
    "category": "leave"
}
```

### Payload Filtering

Filtering allows us to restrict vector searches using metadata conditions.

For example:

```python
Filter(
    must=[
        FieldCondition(
            key="category",
            match=MatchValue(value="leave")
        )
    ]
)
```

This retrieves matching documents only from the `leave` category.

### Payload Indexing

Payload indexing helps Qdrant perform metadata filtering more efficiently.

In this project, we create a keyword index on the `category` field.

## 6. Project Structure

```text
RAG/
│
├── knowledge.json
├── main.py
├── .env
├── .gitignore
└── requirements.txt
```

## 7. Environment Variables

Create a `.env` file:

```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
GROQ_API_KEY=your_groq_api_key
```

Never commit your API keys to GitHub.

## 8. Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install qdrant-client sentence-transformers groq python-dotenv
```

Alternatively:

```bash
pip install -r requirements.txt
```

## 9. Run the Project

```bash
python qdrant-filter.py
```

The application will:

1. Connect to Qdrant Cloud.
2. Create a collection.
3. Create a payload index.
4. Load documents and generate embeddings.
5. Upload vectors and payloads to Qdrant.
6. Convert the user's question into a vector.
7. Perform similarity search with metadata filtering.
8. Retrieve relevant context.
9. Send the question and context to Groq.
10. Display the generated answer.

## 10. Key Takeaways

- RAG combines information retrieval with LLM generation.
- Embeddings represent text as numerical vectors.
- Document embeddings are generated during indexing.
- Query embeddings are generated during retrieval.
- Both use the same embedding model.
- Cosine similarity helps identify semantically similar documents.
- Qdrant stores and retrieves vectors.
- Payload filtering restricts searches using metadata.
- Payload indexing improves metadata-filtering efficiency.
- The LLM generates answers using the original question and retrieved context.

## 11. Future Improvements

- Implement document chunking for large documents.
- Add more metadata filters.
- Implement conversation memory.
- Experiment with different embedding models.
- Add a frontend for interacting with the RAG application.
- Implement hybrid search combining semantic and keyword retrieval.

---
