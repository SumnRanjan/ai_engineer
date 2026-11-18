# RAG Evaluation (Retrieval-Augmented Generation)

## 1. Introduction

RAG (Retrieval-Augmented Generation) combines information retrieval with Large Language Models (LLMs).

A RAG system retrieves relevant information from a knowledge base and provides that information as context to an LLM to generate an accurate answer.

However, building a RAG pipeline is not enough. We also need to evaluate whether the system retrieves relevant information and generates accurate, contextually supported answers.

**RAG Evaluation** is the process of measuring the performance and reliability of a RAG system.

It helps us identify:
- Whether the retriever fetches relevant documents.
- Whether important information is missing.
- Whether the LLM generates answers based on retrieved context.
- Whether the generated answer is correct and relevant.

---

## 2. RAG Architecture

A typical RAG pipeline works as follows:

1. Load documents from a knowledge base.
2. Split documents into smaller chunks.
3. Generate embeddings for each chunk.
4. Store embeddings in a vector database.
5. Convert the user query into an embedding.
6. Retrieve the most relevant chunks using similarity search.
7. Pass retrieved context to the LLM.
8. Generate an answer using the retrieved context.

### Architecture

```text
              User Query
                  |
                  v
           Generate Embedding
                  |
                  v
          Vector Database
               Qdrant
                  |
                  v
          Retrieve Top-K Chunks
                  |
                  v
          Relevant Context
                  |
                  v
             Groq LLM
                  |
                  v
           Generated Answer
                  |
                  v
            RAG Evaluation
```

---

## 3. Why RAG Evaluation?

A RAG system can generate a grammatically correct answer but still provide incorrect information.

There are two major possibilities:

**1. Retrieval Problem**

The retriever returns irrelevant chunks or fails to retrieve important information.

**2. Generation Problem**

The retriever returns the correct information, but the LLM generates an incorrect answer or introduces unsupported information.

RAG evaluation helps identify these problems separately.

---

## 4. Two Major Types of RAG Evaluation

### A. Retrieval Evaluation

Retrieval evaluation checks whether the retriever fetches relevant information from the vector database.

Important metrics:

- Context Precision
- Context Recall
- Precision@K
- Recall@K
- MRR (Mean Reciprocal Rank)
- Hit Rate

### B. Generation Evaluation

Generation evaluation checks whether the LLM generates a good answer using the retrieved context.

Important metrics:

- Faithfulness
- Answer Relevancy
- Answer Correctness

---

# 5. Retrieval Evaluation Metrics

## 5.1 Context Precision

Context Precision measures how many retrieved chunks are relevant to the user's question.

It checks whether the retriever is returning useful information instead of irrelevant chunks.

### Formula

```text
Context Precision =
Number of Relevant Retrieved Chunks
------------------------------------
Total Retrieved Chunks
```

### Example

User Query:

"What is Qdrant used for?"

Retrieved chunks:

- Chunk 1: RAG combines retrieval and generation.
- Chunk 2: Qdrant is a vector database.
- Chunk 3: Docker is a containerization platform.

Only Chunk 2 is relevant.

```text
Context Precision = 1 / 3

Context Precision = 0.33
```

A higher score indicates that a larger proportion of retrieved chunks are relevant.

**Note:** This is the simple, unranked precision calculation. Ranking-aware Context Precision also considers the positions of relevant chunks.

---

## 5.2 Context Recall

Context Recall measures whether the retrieved context contains the information required to answer the question.

It compares the retrieved context against the ground-truth answer.

### Example

Question:

"How many vacation days do employees get?"

Ground Truth:

"Employees receive 24 days of paid leave per year."

Retrieved Context:

"Employees in India receive 24 days of paid leave annually."

The required information is available in the retrieved context.

Therefore, Context Recall should be high.

### Interpretation

- 1.0 = All important information is present.
- 0.7 = Most important information is present.
- 0.5 = Some important information is present.
- 0.0 = Required information is absent.

---

## 5.3 Precision@K

Precision@K measures the proportion of relevant documents among the top K retrieved documents.

### Formula

```text
Precision@K =
Relevant Documents in Top K
---------------------------
K
```

### Example

Suppose Qdrant returns 5 chunks:

| Chunk | Relevant? |
|---|---|
| C1 | Yes |
| C2 | No |
| C3 | Yes |
| C4 | No |
| C5 | Yes |

```text
Precision@5 = 3 / 5 = 0.60
```

---

## 5.4 Recall@K

Recall@K measures how many of all relevant documents are retrieved in the top K results.

### Formula

```text
Recall@K =
Relevant Documents in Top K
---------------------------
Total Relevant Documents
```

### Example

Suppose there are 5 relevant chunks in the knowledge base, and the retriever returns 3 relevant chunks in the top 5.

```text
Recall@5 = 3 / 5 = 0.60
```

---

## 5.5 Mean Reciprocal Rank (MRR)

MRR measures how high the first relevant document appears in the retrieved results.

It gives more importance to relevant documents appearing at higher positions.

### Formula

```text
MRR = Average of Reciprocal Ranks
```

For one query:

```text
Reciprocal Rank = 1 / Rank of First Relevant Result
```

### Example

Retrieved results:

| Rank | Relevant? |
|---|---|
| 1 | No |
| 2 | Yes |
| 3 | No |

```text
MRR = 1 / 2 = 0.50
```

For multiple queries, calculate the average reciprocal rank.

---

## 5.6 Hit Rate

Hit Rate measures whether at least one relevant document appears in the top K retrieved results.

### Formula

```text
Hit Rate =
Queries with at least one relevant result
-----------------------------------------
Total Queries
```

Example:

If 8 out of 10 queries retrieve at least one relevant chunk:

```text
Hit Rate = 8 / 10 = 0.80
```

---

# 6. Generation Evaluation Metrics

## 6.1 Faithfulness

Faithfulness measures whether the generated answer is supported by the retrieved context.

It helps identify hallucinations.

### Example

Retrieved Context:

"Qdrant is a vector database used for similarity search."

Generated Answer:

"Qdrant is a vector database used for similarity search."

This answer is faithful to the context.

However:

"Qdrant is a relational database developed by Google."

This answer contains unsupported information.

### Interpretation

- 1.0 = All claims are supported.
- 0.7 = Mostly supported with minor issues.
- 0.5 = Some claims are supported.
- 0.0 = Unsupported or contradictory.

---

## 6.2 Answer Relevancy

Answer Relevancy checks whether the generated answer actually addresses the user's question.

### Example

Question:

"What is an embedding?"

Answer:

"An embedding represents data such as text as a numerical vector."

This answer is relevant.

An answer explaining how Docker containers work would be irrelevant.

### Interpretation

- 1.0 = Directly answers the question.
- 0.7 = Mostly answers the question.
- 0.5 = Partially answers the question.
- 0.0 = Completely off-topic.

---

## 6.3 Answer Correctness

Answer Correctness measures whether the generated answer is factually correct compared with the ground-truth answer.

### Example

Question:

"How many vacation days do employees receive?"

Ground Truth:

"Employees receive 24 days of paid leave per year."

Generated Answer:

"Employees receive 24 paid vacation days annually."

The generated answer is semantically correct.

### Interpretation

- 1.0 = Completely correct.
- 0.7 = Mostly correct with minor omissions.
- 0.5 = Partially correct.
- 0.0 = Incorrect or contradictory.

---

# 7. Golden Dataset

A Golden Dataset contains predefined questions and their expected answers.

It is used as a reference for evaluating the RAG pipeline.

### Example

```python
golden_dataset = [
    {
        "id": 1,
        "question": "How many vacation days do I get?",
        "ground_truth": "Employees receive 24 days of paid leave per year.",
        "expected_information": "24 days of paid leave per year."
    },
    {
        "id": 2,
        "question": "What is the work from home policy?",
        "ground_truth": "Employees work from the office three days every week.",
        "expected_information": "Tuesday, Wednesday and Thursday are office days."
    }
]
```

### Why do we need it?

- Provides reference answers.
- Helps compare generated answers.
- Makes evaluation repeatable.
- Helps identify retrieval and generation problems.

A good Golden Dataset should contain representative questions, accurate answers and reliable reference information.

---

# 8. LLM-as-a-Judge

LLM-as-a-Judge is a technique in which an LLM evaluates the output of another LLM or RAG system.

Instead of manually checking every generated answer, we provide an evaluation prompt to an LLM judge.

The judge evaluates the response according to predefined criteria.

### Working

```text
       User Question
             |
             v
      Retrieved Context
             |
             v
       Generated Answer
             |
             v
         LLM Judge
             |
             v
      Evaluation Metrics
             |
             v
       JSON Evaluation
```

### Example

```python
def llm_judge(prompt):

    response = groq_client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        response_format={
            "type": "json_object"
        },

        temperature=0
    )

    return json.loads(
        response.choices[0].message.content
    )
```

The judge returns structured JSON containing evaluation scores and explanations.

**Important:** LLM judges can make mistakes and produce inconsistent scores. Validate their results against manually evaluated examples.

---

# 9. Performance Optimization

RAG evaluation can become slow because multiple LLM API calls are required for each question.

For example, with 5 questions:

| Operation | API Calls |
|---|---:|
| Generate answers | 5 |
| Context Precision | 15 |
| Context Recall | 5 |
| Faithfulness | 5 |
| Answer Relevancy | 5 |
| Answer Correctness | 5 |
| Total | 40 |

The actual number of calls depends on the implementation.

### Optimization Techniques

**1. Combine evaluation metrics**

Instead of making separate LLM calls for every metric, evaluate multiple metrics in one structured LLM request.

**2. Separate ingestion and evaluation**

Create two scripts:

```text
project/
│
├── ingest.py
├── rag_evaluation.py
├── knowledge.json
├── .env
└── pyproject.toml
```

- `ingest.py`: Generate embeddings and upload documents to Qdrant.
- `rag_evaluation.py`: Retrieve existing documents and evaluate answers.

This avoids generating embeddings and uploading documents every time.

**3. Cache embeddings**

Avoid generating embeddings repeatedly for unchanged documents.

**4. Reduce Top-K**

Retrieve only the number of chunks needed for evaluation.

**5. Use timing**

Measure how much time is spent in embedding generation, retrieval and LLM calls.

```python
import time

start = time.time()

answer = ask_llm(question, context)

print(
    f"LLM Time: {time.time() - start:.2f} seconds"
)
```

---

# 10. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Sentence Transformers | Generate text embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| Qdrant | Vector database |
| Groq | LLM inference |
| JSON | Golden dataset and evaluation output |
| python-dotenv | Environment variable management |

### Embedding Model

```python
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
```

This model generates 384-dimensional embeddings.

These vectors are stored in Qdrant and used for similarity search.

### Qdrant Collection

```python
client.create_collection(

    collection_name="rag_eval",

    vectors_config=VectorParams(

        size=384,

        distance=Distance.COSINE
    )
)
```

Cosine similarity measures the similarity between vectors based on their direction.

---

# 11. Installation and Setup

### Step 1: Create a project

```bash
mkdir week4/day1
cd week4/day1
```

### Step 2: Initialize UV

```bash
uv init
```

### Step 3: Install dependencies

```bash
uv add python-dotenv qdrant-client sentence-transformers groq
```

### Step 4: Configure environment variables

Create a `.env` file:

```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
GROQ_API_KEY=your_groq_api_key
```

Never upload your `.env` file or API keys to GitHub.

Add `.env` to `.gitignore`.

### Step 5: Run the project

```bash
uv run python ingest.py
```

After ingestion:

```bash
uv run python rag_evaluation.py
```

---

# 12. Evaluation Workflow

For every question in the Golden Dataset:

1. Retrieve the top K chunks from Qdrant.
2. Display retrieved documents and similarity scores.
3. Combine retrieved chunks into context.
4. Generate an answer using Groq.
5. Evaluate Context Precision.
6. Evaluate Context Recall.
7. Evaluate Faithfulness.
8. Evaluate Answer Relevancy.
9. Evaluate Answer Correctness.
10. Store evaluation scores.
11. Calculate average scores.
12. Print the final evaluation report.

---

# 13. Final Evaluation Report

A RAG evaluation report can look like this:

```text
==================================================
                 RAG EVALUATION
==================================================

QUESTION: How many vacation days do I get?

Retrieved Documents:
Chunk 1: Employees receive 24 days of paid leave.
Chunk 2: Employees can apply for sick leave.
Chunk 3: Employees receive internet reimbursement.

Generated Answer:
Employees receive 24 days of paid leave per year.

Scores:

Context Precision : 0.33
Context Recall    : 1.00
Faithfulness      : 1.00
Answer Relevancy  : 1.00
Answer Correctness: 1.00

Diagnosis:
Retrieval is returning irrelevant chunks.

==================================================
                 FINAL SUMMARY
==================================================
```

The values above are illustrative, not actual evaluation results.

---

# 14. Key Learnings

Through this project, I learned:

- What RAG Evaluation is and why it is important.
- Difference between Retrieval Evaluation and Generation Evaluation.
- Context Precision and Context Recall.
- Precision@K and Recall@K.
- Mean Reciprocal Rank (MRR).
- Hit Rate.
- Faithfulness and hallucination detection.
- Answer Relevancy and Answer Correctness.
- Golden Dataset creation.
- LLM-as-a-Judge.
- Structured JSON evaluation using Groq.
- Performance optimization by reducing API calls.
- Separating document ingestion from evaluation.
- Evaluating a complete RAG pipeline.

---

# 15. Conclusion

RAG Evaluation helps measure the quality, reliability and accuracy of Retrieval-Augmented Generation systems.

A good RAG system should not only retrieve relevant information but also generate answers that are accurate, relevant and supported by the retrieved context.

The most important concept I learned is:

**We must evaluate retrieval and generation separately because an incorrect final answer can be caused by either poor retrieval or poor generation.**

This project demonstrates how to evaluate a RAG pipeline using Qdrant, Sentence Transformers and Groq.
