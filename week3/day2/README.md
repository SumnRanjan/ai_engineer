# Understanding Text Embeddings & Cosine Similarity

A beginner-friendly Python project to understand how text is converted into numerical vectors (embeddings) and how semantic similarity between two sentences can be measured using cosine similarity.

This project uses **Sentence Transformers, NumPy, and the all-MiniLM-L6-v2 embedding model**.

## 1. What are Text Embeddings?

Text embeddings are numerical representations of text (words, sentences, or paragraphs) in the form of vectors.

An embedding model converts human-readable text into a list of numbers that captures its semantic meaning.

For example:

```text
Input:
"Machine learning is fun."

Output:
[0.21, -0.45, 0.67, 0.12, ...]
```

These numerical vectors help machines understand semantic relationships between different pieces of text.

## 2. What is Sentence Transformer?

Sentence Transformers is a Python library used to generate embeddings for sentences and paragraphs.

In this project, we use:

```python
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
```

### Understanding all-MiniLM-L6-v2

- **MiniLM:** A compact language model.
- **L6:** Contains 6 Transformer layers.
- **384:** Generates embeddings with 384 dimensions.
- **v2:** Second version of this model.

This model converts a sentence into a vector containing 384 numerical values.

## 3. Generating Text Embeddings

We use the `encode()` method to convert text into embeddings.

```python
text = "Machine learning is fun."

embedding = model.encode(text)

print(f"Embedding shape: {embedding.shape}")
print(f"Embedding: {embedding[:10]}")
```

### Explanation

- `model.encode(text)` converts text into a numerical vector.
- `embedding.shape` returns the dimensions of the vector.
- `embedding[:10]` displays the first 10 values.

Expected shape:

```text
(384,)
```

This means one sentence is represented by 384 numerical values.

## 4. What is Cosine Similarity?

Cosine similarity is a mathematical technique used to measure how similar two vectors are by calculating the cosine of the angle between them.

In NLP and RAG, it is commonly used to measure the semantic similarity between text embeddings.

### Formula

```text
                 A . B
Cosine Similarity = ----------------
                    ||A|| * ||B||
```

Where:

- A = First embedding vector.
- B = Second embedding vector.
- A . B = Dot product of both vectors.
- ||A|| = Magnitude (norm) of vector A.
- ||B|| = Magnitude (norm) of vector B.

### Understanding the Similarity Score

| Score | Interpretation |
|---|---|
| Close to 1 | Highly similar direction |
| Close to 0 | Little directional similarity |
| Close to -1 | Opposite direction |

For typical semantic embedding models, scores are often positive, but the exact interpretation depends on the model and dataset.

## 5. Implementing Cosine Similarity Using NumPy

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
```

### Explanation of NumPy Functions

**1. np.dot(a, b)**

Calculates the dot product of two vectors.

**2. np.linalg.norm(a)**

Calculates the magnitude (length) of vector A.

**3. np.linalg.norm(b)**

Calculates the magnitude (length) of vector B.

Finally, we divide the dot product by the product of both vector magnitudes.

## 6. Comparing Two Sentences

In this project, we compare two different text inputs.

```python
t1 = "there are 24 paid leaves"
t2 = "cat"

v1 = model.encode(t1)
v2 = model.encode(t2)

print(
    f"Cosine similarity: {cosine_similarity(v1, v2)}"
)
```

### What happens internally?

1. The first sentence is passed to the embedding model.
2. The second sentence is passed to the embedding model.
3. Both sentences are converted into 384-dimensional vectors.
4. Cosine similarity calculates the similarity between the two vectors.
5. The result is a numerical similarity score.

Since the sentences discuss unrelated topics, we generally expect a lower semantic similarity score.

## 7. Project Workflow

```text
Text 1: "There are 24 paid leaves"
                  |
                  v
          Sentence Transformer
                  |
                  v
          Embedding Vector 1
                  |
                  |
                  |       Text 2: "cat"
                  |              |
                  |              v
                  |      Sentence Transformer
                  |              |
                  |              v
                  |      Embedding Vector 2
                  |              |
                  +--------------+
                         |
                         v
                Cosine Similarity
                         |
                         v
                 Similarity Score
```

## 8. Why are Embeddings Important in RAG?

Embeddings play an important role in Retrieval-Augmented Generation (RAG).

Imagine a knowledge base containing thousands of documents.

When a user asks a question:

1. The user's question is converted into an embedding.
2. The system compares the query embedding with stored document embeddings.
3. Cosine similarity or another similarity metric helps find relevant documents.
4. The most relevant information is retrieved.
5. The retrieved information is passed to an LLM as context.
6. The LLM generates the final answer.

This allows RAG applications to perform semantic search instead of relying only on exact keyword matching.

## 9. Technologies Used

- Python
- NumPy
- Sentence Transformers
- all-MiniLM-L6-v2

## 10. Installation

Install the required dependencies:

```bash
pip install numpy sentence-transformers
```

Run the application:

```bash
python embedded_rag.py
```

The first execution downloads the embedding model, so an internet connection is required.

## 11. Key Learnings

Through this project, I learned:

- What text embeddings are.
- How text is converted into numerical vectors.
- What Sentence Transformers are.
- How the all-MiniLM-L6-v2 model works.
- Why embeddings have 384 dimensions.
- What cosine similarity is.
- How NumPy calculates dot products and vector magnitudes.
- How semantic similarity helps retrieve relevant information in RAG.

## 12. Next Learning Steps

- Compare multiple sentences using embeddings.
- Understand semantic search.
- Learn vector databases such as ChromaDB and FAISS.
- Store and retrieve embeddings.
- Implement similarity-based document retrieval.
- Build a complete RAG application.

**Learning Objective:** Understand how machines represent human language numerically and how vector similarity helps identify semantically related text. This is a foundational concept for building semantic search engines and RAG-based AI applications.