# Chunking in RAG

## 1. What is Chunking?

**Chunking** is the process of splitting a large document into smaller
pieces of text called *chunks*.

In Retrieval-Augmented Generation (RAG), documents are split into chunks
before generating embeddings. Each chunk is embedded and stored in a
vector database, such as Qdrant.

When a user asks a question, the system searches for the most relevant
chunks instead of retrieving the entire document.

### Why is chunking important?

-   It helps retrieve focused and relevant information.
-   It avoids embedding an entire large document as one piece.
-   It can reduce irrelevant text passed to the LLM.
-   It helps keep retrieved context within the LLM's context window.

Chunking can improve retrieval relevance, but it does not automatically
guarantee faster search. Search speed also depends on the vector
database, indexing strategy, and dataset size.

------------------------------------------------------------------------

## 2. Types of Chunking

### A. Fixed-Size Chunking

Splits text into chunks based on a target size.

For example, with a chunk size of 100 characters, the splitter tries to
combine text pieces into chunks of around 100 characters.

### B. Paragraph Chunking

Splits text at paragraph boundaries. A common separator is `"\n\n"`
because two newline characters often separate paragraphs.

This approach tries to keep each paragraph together. If a paragraph is
too large, it may be split further depending on the splitter's
configuration.

### C. Recursive Character Chunking

Tries a hierarchy of separators to split text while preserving larger
meaningful units whenever possible.

A common separator order is:

1.  `"\n\n"` --- paragraph boundary
2.  `"\n"` --- line boundary
3.  `" "` --- word boundary
4.  `""` --- character boundary

It tries paragraph boundaries first. If a piece is still too large, it
tries smaller boundaries.

------------------------------------------------------------------------

## 3. What Is Chunk Overlap?

**Chunk overlap** means repeating some text from the end of one chunk at
the beginning of the next chunk.

Example:

-   Chunk size: 150 characters
-   Chunk overlap: 30 characters

The next chunk can begin with text from the previous chunk's ending.
This helps preserve context when related information falls near a chunk
boundary.

Overlap is useful, but too much overlap creates redundant chunks and
increases storage and embedding work.

------------------------------------------------------------------------

## 4. Install the Required Package Using uv

Create a project if you do not already have one:

``` bash
uv init
```

Install LangChain's text-splitting package:

``` bash
uv add langchain-text-splitters
```

You do not need to install the complete `langchain` package for the
examples in this README.

------------------------------------------------------------------------

## 5. Complete Python Example

Create a file named `main.py`:

``` python
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter
)

text = """
The detective entered the abandoned house just before midnight.
The rooms were silent, and the windows were covered with dust.
On the table, he found a bloodstained letter.

The man who did the crime was John.
Nobody in the village trusted him, but he had disappeared
three days before the murder. The detective immediately realized
that something was suspicious.

The next morning, the detective returned to the house.
Behind a loose brick, he discovered a photograph of John
standing beside the victim. This finally connected John
to the mysterious murder.
"""


# ============================================================
# 1. FIXED-SIZE CHUNKING
# ============================================================

fixed = CharacterTextSplitter(
    separator=" ",
    chunk_size=100,
    chunk_overlap=0,
    length_function=len
)

print("\n========== FIXED SIZE ==========")

for i, chunk in enumerate(fixed.split_text(text), 1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("------------------------")


# ============================================================
# 2. PARAGRAPH CHUNKING
# ============================================================

paragraph = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=200,
    chunk_overlap=0,
    length_function=len
)

print("\n========== PARAGRAPH CHUNKING ==========")

for i, chunk in enumerate(paragraph.split_text(text), 1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("------------------------")


# ============================================================
# 3. RECURSIVE CHARACTER CHUNKING
# ============================================================

recursive = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30,
    separators=["\n\n", "\n", " ", ""],
    length_function=len
)

print("\n========== RECURSIVE CHUNKING ==========")

for i, chunk in enumerate(recursive.split_text(text), 1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("------------------------")
```

Run the file:

``` bash
uv run python main.py
```

------------------------------------------------------------------------

## 6. Understanding the Code

### Fixed-size chunking

``` python
fixed = CharacterTextSplitter(
    separator=" ",
    chunk_size=100,
    chunk_overlap=0,
    length_function=len
)
```

-   `separator=" "`: splits the text at spaces.
-   `chunk_size=100`: targets chunks of approximately 100 characters.
-   `chunk_overlap=0`: does not intentionally repeat text between
    chunks.
-   `length_function=len`: measures chunk length in characters.

### Paragraph chunking

``` python
paragraph = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=200,
    chunk_overlap=0,
    length_function=len
)
```

-   `separator="\n\n"`: splits at paragraph boundaries.
-   `chunk_size=200`: targets chunks of approximately 200 characters.
-   `chunk_overlap=0`: no intentional overlap.

### Recursive chunking

``` python
recursive = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30,
    separators=["\n\n", "\n", " ", ""],
    length_function=len
)
```

-   `chunk_size=150`: target chunk length of 150 characters.
-   `chunk_overlap=30`: tries to preserve 30 characters between
    consecutive chunks.
-   `separators`: defines the order in which splitting boundaries are
    tried.
-   `length_function=len`: measures length in characters.

**Important:** `CharacterTextSplitter` splits using its specified
separator and merges the resulting pieces up to the target size. It does
not necessarily split a single oversized piece.
`RecursiveCharacterTextSplitter` is more suitable when text can contain
sections larger than the target size.

------------------------------------------------------------------------

## 7. Comparison

  -----------------------------------------------------------------------
  Technique               Splitting approach      Main idea
  ----------------------- ----------------------- -----------------------
  Fixed-size              A chosen separator and  Create chunks of
                          target size             roughly similar size

  Paragraph               Paragraph separator     Keep paragraphs
                          such as `\n\n`          together where possible

  Recursive               Multiple separators in  Preserve larger text
                          a hierarchy             units before splitting
                                                  further
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 8. Important Parameters

  Parameter           Meaning
  ------------------- ----------------------------------------------------
  `chunk_size`        Target maximum chunk length
  `chunk_overlap`     Text repeated between consecutive chunks
  `separator`         Boundary used to split the text
  `separators`        Ordered list of boundaries for recursive splitting
  `length_function`   Function used to measure text length

In these examples, `length_function=len` means chunk sizes are measured
in **characters, not tokens**. Token-based chunking can be configured
separately when needed.

------------------------------------------------------------------------

## 9. How Chunking Fits into RAG

``` text
              DOCUMENT
                  |
                  v
              CHUNKING
                  |
                  v
          SMALL TEXT CHUNKS
                  |
                  v
            EMBEDDING MODEL
                  |
                  v
          VECTOR REPRESENTATIONS
                  |
                  v
          VECTOR DATABASE
               (Qdrant)


             USER QUESTION
                  |
                  v
           QUERY EMBEDDING
                  |
                  v
          SIMILARITY SEARCH
                  |
                  v
          RELEVANT TEXT CHUNKS
                  |
                  v
             LLM + CONTEXT
                  |
                  v
             FINAL ANSWER
```

### RAG ingestion process

1.  Load the document.
2.  Split the document into chunks.
3.  Generate an embedding for each chunk.
4.  Store each vector with its original text and metadata in Qdrant.

### RAG retrieval process

1.  Receive the user's question.
2.  Generate an embedding for the question using the same embedding
    model.
3.  Search the vector database for similar vectors.
4.  Retrieve the most relevant chunks.
5.  Pass the retrieved chunks and question to the LLM.
6.  Generate the final answer.

------------------------------------------------------------------------

## 10. Interview Questions

### Q1. What is chunking in RAG?

Chunking is the process of splitting large documents into smaller pieces
of text so that relevant information can be retrieved more effectively.

### Q2. Why do we need chunking?

It helps the retrieval system find focused pieces of information instead
of searching with one large document representation. It can also reduce
irrelevant context passed to the LLM.

### Q3. What is chunk overlap?

Chunk overlap repeats some text between consecutive chunks to help
preserve context across chunk boundaries.

### Q4. What is the difference between fixed-size and recursive chunking?

Fixed-size splitting uses a selected separator and target size.
Recursive splitting tries multiple separators in order, attempting to
preserve larger text structures before splitting into smaller units.

### Q5. Which chunking technique is useful for RAG?

`RecursiveCharacterTextSplitter` is a useful general starting point
because it tries to preserve paragraphs, lines, and words before
splitting further. The best strategy still depends on the document
structure and retrieval results.

### Q6. What happens if chunks are too small or too large?

-   Very small chunks can lose surrounding context.
-   Very large chunks can contain unrelated information and add
    unnecessary context.
-   Chunk size and overlap should be tested against the documents and
    questions in the application.

------------------------------------------------------------------------

## Quick Revision

-   **Chunking:** Splitting large text into smaller pieces.
-   **Fixed-size chunking:** Uses a selected separator and target size.
-   **Paragraph chunking:** Splits at paragraph boundaries.
-   **Recursive chunking:** Tries multiple separators hierarchically.
-   **Chunk overlap:** Repeats text between neighboring chunks.
-   **`chunk_size`:** Target chunk length.
-   **`chunk_overlap`:** Shared text between chunks.
-   **RAG use:** Embed and store chunks, retrieve relevant chunks, and
    pass them to the LLM.

**Key takeaway:** Chunking prepares documents for retrieval. Good chunk
boundaries help the RAG system retrieve useful context for the LLM.
