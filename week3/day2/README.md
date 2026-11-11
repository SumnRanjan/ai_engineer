# Understanding RAG (Retrieval-Augmented Generation)

A beginner-friendly Python project to understand the fundamental concept of **Retrieval-Augmented Generation (RAG)** using Groq API and an LLM.

This project demonstrates how an LLM can answer questions using external information (a knowledge base) instead of relying entirely on its pre-trained knowledge.

## 1. What is RAG?

**RAG stands for Retrieval-Augmented Generation.**

It is a technique in which an application retrieves relevant information from an external knowledge source and provides that information to an LLM as context to generate an answer.

In simple terms:

- **Retrieval:** Find relevant information from a knowledge base.
- **Augmentation:** Add the retrieved information to the LLM prompt as context.
- **Generation:** The LLM uses the provided context to generate an answer.

## 2. Project Overview

In this project, we create a small knowledge base containing information about Batman.

```python
knowledge_base = {
    "age": "Batman is 35 years old",
    "net worth": "Batman has a net worth of 9.2 billion dollars"
}
```

The user asks questions, and the application retrieves relevant information from the knowledge base before sending the question and context to the LLM.

## 3. How Does It Work?

The application follows three main steps:

### Step 1: Create a Knowledge Base

We create a Python dictionary that stores external information.

```python
knowledge_base = {
    "age": "Batman is 35 years old",
    "net worth": "Batman has a net worth of 9.2 billion dollars"
}
```

This acts as our external knowledge source.

### Step 2: Retrieve Relevant Information

We create a `retrieve_info()` function that searches the knowledge base based on the user's question.

```python
def retrieve_info(question):
    question = question.lower()

    if "age" in question:
        return knowledge_base["age"]

    elif "net worth" in question:
        return knowledge_base["net worth"]

    else:
        return "Information not found."
```

For example:

| User Question | Retrieved Context |
|---|---|
| Who is Batman's age? | Batman is 35 years old |
| What is Batman's net worth? | Batman has a net worth of 9.2 billion dollars |
| Is he rich? | Information not found |

**Important:** This project uses simple keyword-based retrieval, not semantic search or vector embeddings.

### Step 3: Augment the Prompt and Generate an Answer

After retrieving the relevant information, we pass it to the LLM through a system prompt.

```python
context = retrieve_info(question)

system_prompt = f"""
Answer in one sentence.
Answer based on context.
Do not hallucinate.

Context: {context}
"""
```

We send two messages to the LLM:

- **System message:** Defines the instructions and provides retrieved context.
- **User message:** Contains the original user question.

The LLM generates an answer using the provided context.

## 4. Project Architecture

```text
User Question
     |
     v
retrieve_info()
     |
     v
Knowledge Base
     |
     v
Relevant Context
     |
     v
System Prompt + User Question
     |
     v
Groq API
     |
     v
LLM (GPT-OSS-120B)
     |
     v
Generated Answer
```

## 5. Understanding the Role of Each Component

| Component | Responsibility |
|---|---|
| Knowledge Base | Stores external information |
| Retrieval Function | Finds relevant information |
| Context | Provides retrieved information to the LLM |
| System Prompt | Defines how the LLM should behave |
| User Prompt | Contains the user's actual question |
| Groq API | Provides access to the language model |
| LLM | Generates the final response |

## 6. Example Execution

**Input:**

```python
print(ask_llm("who is batman age ?"))
print(ask_llm("what is batman net worth ?"))
print(ask_llm("is he rich ?"))
```

**Expected responses (illustrative):**

```text
Batman is 35 years old.

Batman has a net worth of 9.2 billion dollars.

Information not found.
```

The actual response may vary depending on the LLM.

## 7. Important Concepts Learned

### What is Context?

Context is the relevant information provided to the LLM so it can generate an answer based on specific external data.

### What is Retrieval?

Retrieval is the process of finding relevant information from an external knowledge source based on a user's query.

### What is Augmentation?

Augmentation means adding the retrieved information to the LLM's input prompt.

### What is Hallucination?

Hallucination occurs when an LLM generates incorrect or unsupported information.

In this project, we instruct the LLM to answer only using the retrieved context to reduce hallucinations.

However, a prompt instruction alone cannot guarantee that hallucinations will never occur.

## 8. Is This a Complete RAG System?

This is a **basic RAG learning implementation**.

It demonstrates the core RAG workflow but does not implement advanced retrieval techniques.

| Basic Implementation | Advanced RAG |
|---|---|
| Python dictionary | Document-based knowledge base |
| Keyword matching | Semantic search |
| No embeddings | Embedding models |
| No vector database | ChromaDB, FAISS, Pinecone |
| Simple context injection | Context ranking and optimization |
| Groq LLM | Groq or other LLM providers |

## 9. What I Plan to Learn Next

- Document loading (PDF, TXT, DOCX)
- Text chunking and chunk overlap
- Text embeddings
- Vector databases
- Cosine similarity
- Semantic search
- Retrieval optimization
- Building a complete RAG pipeline

## 10. Technologies Used

- Python
- Groq API
- GPT-OSS-120B
- python-dotenv

## 11. Environment Setup

Install the required dependencies:

```bash
pip install groq python-dotenv
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Run the application:

```bash
python embedded_rag.py
```

**Learning Objective:** Understand how external knowledge can be retrieved, injected into an LLM prompt, and used to generate context-aware responses. This project is the first step toward building a complete RAG application.