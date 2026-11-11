
import os
import json

from dotenv import load_dotenv  # type: ignore
from qdrant_client import QdrantClient  # type: ignore
from qdrant_client.models import (Distance, VectorParams,PointStruct, Filter,FieldCondition,MatchValue,PayloadSchemaType)  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore
from groq import Groq  # type: ignore


# ============================================================
# PART 1 — ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY or not GROQ_API_KEY:
    raise ValueError("Missing API keys or Qdrant URL in .env")


# ============================================================
# PART 2 — QDRANT CONNECTION
# ============================================================

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

print("Connected to Qdrant Cloud!")


# ============================================================
# PART 3 — CREATE COLLECTION
# ============================================================

COLLECTION_NAME = "knowledge"
EMBEDDING_SIZE = 384

if client.collection_exists(COLLECTION_NAME):
    print(f"Deleting existing collection: {COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE
    )
)

print(f"Created collection: {COLLECTION_NAME}")


# ============================================================
# PART 4 — CREATE PAYLOAD INDEX
# ============================================================

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)

print("Payload index created!")


# ============================================================
# PART 5 — LOAD DOCUMENTS
# ============================================================

with open("knowledge.json", "r", encoding="utf-8") as f:
    documents = json.load(f)


# ============================================================
# PART 6 — CREATE EMBEDDINGS
# ============================================================

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

texts = [document["text"] for document in documents]

embeddings = model.encode(texts)

print(f"Created {len(embeddings)} embeddings")


# ============================================================
# PART 7 — CREATE QDRANT POINTS
# ============================================================

points = []

for i, embedding in enumerate(embeddings):

    point = PointStruct(
        id=i,
        vector=embedding.tolist(),
        payload=documents[i]
    )

    points.append(point)


# ============================================================
# PART 8 — UPLOAD POINTS TO QDRANT
# ============================================================

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points,
)

print("Documents uploaded successfully!")


# ============================================================
# PART 9 — SEARCH QDRANT WITH FILTER
# ============================================================

def search_qdrant_with_filter(query, top_k=3, category=None):

    # Convert query into embedding
    query_vector = model.encode([query]).tolist()[0]

    # Create filter dynamically
    filter_condition = None

    if category:
        filter_condition = Filter(
            must=[
                FieldCondition(
                    key="category",
                    match=MatchValue(value=category)
                )
            ]
        )

    # Search in Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=filter_condition
    ).points

    return results


# ============================================================
# PART 10 — GROQ LLM CONNECTION
# ============================================================

groq_client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# PART 11 — ASK LLM WITH RETRIEVED CONTEXT
# ============================================================

def ask_llm(question, context):

    system_prompt = f"""
    Answer in one sentence based only on the provided context.

    If the answer is not available in the context,
    say that you don't have enough information.

    Do not hallucinate.

    Context:
    {context}
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )

    return response.choices[0].message.content


# ============================================================
# PART 12 — FINAL RAG PIPELINE
# ============================================================

question = "How much vacation do I get?"

# Retrieve relevant documents using category filter
results = search_qdrant_with_filter(
    query=question,
    top_k=3,
    category="leave"
)

# Print retrieved documents
print("\nRetrieved Documents:")

for result in results:
    print(f"Score: {result.score}")
    print(f"Text: {result.payload['text']}")
    print("-----------------------------------")


# Prepare context
context = " ".join(
    result.payload["text"]
    for result in results
)

# Generate answer
if not results:
    print("\nNo relevant documents found.")
else:
    answer = ask_llm(question, context)
    print(f"\nAnswer: {answer}")
