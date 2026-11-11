# RAG with Qdrant, Sentence Transformers, and Groq

A simple Retrieval-Augmented Generation (RAG) project that loads text
documents, converts them into embeddings, stores them in **Qdrant
Cloud**, retrieves relevant information using vector similarity search,
and sends the retrieved context to a **Groq-hosted LLM** to generate an
answer.

## How the project works

The project has two main stages:

1.  **Indexing:** Read documents, generate embeddings, create Qdrant
    points, and upload them to a collection.
2.  **Question answering:** Convert a user's question into an embedding,
    search Qdrant for the most similar document vectors, and pass the
    retrieved text to the LLM.

``` text
                 INDEXING
knowledge.txt
     |
     v
Read documents (one non-empty line = one document)
     |
     v
SentenceTransformer (all-MiniLM-L6-v2)
     |
     v
384-dimensional embeddings
     |
     v
Qdrant Points (ID + Vector + Payload)
     |
     v
Qdrant Cloud Collection: knowledge


              QUESTION ANSWERING
User question
     |
     v
SentenceTransformer
     |
     v
Question embedding (384 dimensions)
     |
     v
Qdrant similarity search (top_k)
     |
     v
Relevant document text (context)
     |
     v
Groq LLM (openai/gpt-oss-120b)
     |
     v
Generated answer
```

## Technologies used

  -----------------------------------------------------------------------
  Technology                          Purpose
  ----------------------------------- -----------------------------------
  Python                              Implements the RAG pipeline

  `sentence-transformers`             Converts documents and questions
                                      into embeddings

  `all-MiniLM-L6-v2`                  Embedding model that produces
                                      384-dimensional vectors

  Qdrant Cloud                        Stores vectors and payloads, and
                                      performs similarity search

  `qdrant-client`                     Python client for communicating
                                      with Qdrant

  Groq                                Provides the LLM API used to
                                      generate answers

  `python-dotenv`                     Loads API credentials from a `.env`
                                      file
  -----------------------------------------------------------------------

## Key concepts

### 1. Embeddings

An embedding is a numerical representation of text. The project uses
`all-MiniLM-L6-v2` from Sentence Transformers.

``` python
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("Python is used in AI development")
print(embedding.shape)  # (384,)
```

This model produces a vector with **384 dimensions**, meaning 384
numerical values per embedding.

If there are 5 documents, the project creates 5 vectors. Each vector has
384 values, so there are `5 × 384 = 1,920` numerical values in total.

### 2. Qdrant collection

A **collection** is a named group of points in Qdrant. It is broadly
comparable to a table in a relational database.

This project creates a collection named `knowledge`.

### 3. VectorParams

`VectorParams` configures the vectors that a collection will store. In
this project:

``` python
VectorParams(
    size=384,
    distance=Distance.COSINE,
)
```

-   `size=384`: every vector in this vector configuration must contain
    384 dimensions.
-   `distance=Distance.COSINE`: Qdrant uses cosine distance to compare
    vectors during similarity search.

`VectorParams` configures the vector settings;
`client.create_collection()` actually creates the collection.

### 4. Distance

`Distance.COSINE` selects the **distance metric**, not the indexing
algorithm. Qdrant also supports metrics such as `Distance.DOT` and
`Distance.EUCLID`.

The metric determines how Qdrant compares a query vector with stored
vectors and ranks matching results.

### 5. PointStruct

A Qdrant point is a record containing an ID, a vector, and optionally a
payload.

``` python
PointStruct(
    id=1,
    vector=embedding.tolist(),
    payload={"text": "Employees receive annual vacation days."}
)
```

-   `id`: identifies the point.
-   `vector`: the embedding stored for that document.
-   `payload`: additional information, such as the original text, source
    filename, page number, or category.

The payload lets the application retrieve readable document content
after a vector search.

### 6. HNSW

HNSW means **Hierarchical Navigable Small World**. It is a graph-based
approximate-nearest-neighbor indexing method that Qdrant commonly uses
to make vector search efficient.

Keep these concepts separate:

-   `VectorParams`: configures vector dimensions and distance metric.
-   `Distance.COSINE`: selects the vector comparison metric.
-   HNSW: an indexing/search method used to find nearest vectors
    efficiently.

HNSW is not the same thing as the distance metric.

### 7. RAG

RAG stands for **Retrieval-Augmented Generation**:

-   **Retrieval:** Qdrant finds relevant document chunks.
-   **Augmented:** those retrieved documents are supplied as context.
-   **Generation:** the LLM uses the question and context to generate an
    answer.

Qdrant does not replace RAG or generate embeddings in this project.
Sentence Transformers generates embeddings, Qdrant stores and retrieves
them, and the Groq LLM generates the answer.

## Project structure

A minimal project layout:

``` text
rag-qdrant/
├── .env
├── .gitignore
├── knowledge.txt
├── main.py
├── pyproject.toml
└── README.md
```

Save the Python pipeline in `main.py`. Put your source knowledge in
`knowledge.txt`, with one document or text chunk per non-empty line.

## Requirements

-   Python version supported by the installed dependencies.
-   A Qdrant Cloud cluster and its URL/API key.
-   A Groq API key.
-   Internet access for the cloud APIs and for downloading the embedding
    model the first time it is used.

## Setup

### 1. Create the project

``` bash
uv init rag-qdrant
cd rag-qdrant
```

### 2. Add dependencies

``` bash
uv add python-dotenv qdrant-client sentence-transformers groq
```

### 3. Configure environment variables

Create a `.env` file in the project root:

``` env
QDRANT_URL=https://YOUR-CLUSTER-URL
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Replace the placeholders with your actual credentials. Do not commit
`.env` or expose API keys in source code, screenshots, logs, or Git
history.

### 4. Add your knowledge

Create `knowledge.txt`. Example:

``` text
Employees receive 20 days of annual leave each year.
Employees can request work from home with manager approval.
Salary is paid on the last working day of each month.
```

The supplied script treats each non-empty line as a separate document.
For larger files, consider splitting content into meaningful chunks and
retaining source metadata.

### 5. Run the project

``` bash
uv run python qdrant_vectordb.py
```

The first run may take longer because Sentence Transformers may need to
download the embedding model.

## Understanding the Python pipeline

  -----------------------------------------------------------------------
  Part                                What it does
  ----------------------------------- -----------------------------------
  1\. Imports and environment         Imports dependencies and loads
                                      `.env` variables

  2\. Connect to Qdrant               Creates a client using the cloud
                                      URL and API key

  3\. Create collection               Checks for the `knowledge`
                                      collection and creates it with
                                      384-dimensional cosine vectors

  4\. Load knowledge                  Reads non-empty lines from
                                      `knowledge.txt`

  5\. Create embeddings               Uses Sentence Transformers to
                                      convert each document into a vector

  6\. Create points                   Builds `PointStruct` objects with
                                      IDs, vectors, and text payloads

  7\. Upload to Qdrant                Uses `upsert()` to insert or update
                                      points

  8\. Search Qdrant                   Embeds a query and retrieves the
                                      top matching points

  9\. Test search                     Prints similarity scores and
                                      retrieved text

  10\. Connect to Groq                Creates a Groq API client

  11\. Ask the LLM                    Sends the question and retrieved
                                      context to the LLM

  12\. Complete RAG pipeline          Combines retrieval and generation
                                      into a final answer
  -----------------------------------------------------------------------

## How search works

The `search()` function performs these steps:

1.  Encodes the user's question with the same embedding model used for
    the documents.
2.  Sends the query vector to Qdrant.
3.  Requests up to `top_k` matching points.
4.  Returns the points, including their payloads.

``` python
def search(query, top_k=3):
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    return results
```

`top_k=3` asks Qdrant to return up to three matching points. It does not
mean that the collection contains only three points.

The returned `score` is a vector-search score based on the configured
distance metric. It is not a guarantee that the retrieved text answers
the question.

## Important implementation notes

1.  **Collection deletion:** The supplied script deletes the existing
    `knowledge` collection before recreating it. This removes its
    existing points and collection configuration. It is useful for a
    clean demo re-index, but do not use this behavior if you need to
    preserve existing data.
2.  **Credentials:** Check that `QDRANT_URL`, `QDRANT_API_KEY`, and
    `GROQ_API_KEY` are present before creating clients. Never hard-code
    secrets.
3.  **Empty input:** Ensure `knowledge.txt` contains at least one
    non-empty line before accessing `embeddings[0]`.
4.  **Consistent embeddings:** Use the same embedding model and
    compatible vector dimensions for document vectors and query vectors.
5.  **Chunking:** One line per document is a simple demonstration. Real
    documents usually need to be split into appropriately sized chunks.
6.  **Retrieval quality:** Similarity search can return related but
    insufficient text. Tune chunking and `top_k`, and consider metadata
    filters or reranking when needed.
7.  **LLM grounding:** The prompt asks the model to answer only from the
    retrieved context, but prompts alone cannot guarantee that a model
    will never make an unsupported statement.

## Troubleshooting

-   **Qdrant connection error:** Verify the cluster URL, API key,
    network access, and that the Qdrant cluster is available.
-   **Dimension mismatch:** Ensure the collection's vector size matches
    the embedding model output (384 for `all-MiniLM-L6-v2`).
-   **Missing environment variables:** Confirm `.env` is in the working
    directory and the variable names match exactly.
-   **No useful search results:** Check that the knowledge file contains
    relevant content and that the query and documents use the same
    embedding model.
-   **Groq API error:** Verify the API key, model availability, and
    account/API limits.

## Summary

This project demonstrates a basic RAG pipeline:

-   **Sentence Transformers** converts text into 384-dimensional
    embeddings.
-   **Qdrant Collection** organizes the stored points.
-   **VectorParams** defines the vector size and distance metric.
-   **Distance.COSINE** selects how vectors are compared.
-   **PointStruct** represents each stored point with an ID, vector, and
    payload.
-   **HNSW** is an indexing approach that helps Qdrant search vectors
    efficiently.
-   **Groq LLM** generates an answer using the context retrieved from
    Qdrant.
