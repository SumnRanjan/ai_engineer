import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore
import numpy as np # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") #384
text="Machine learning is fun."

# embedding=model.encode(text)
# print(f"Embedding shape: {embedding.shape}")  
# print(f"Embedding: {embedding[:10]}")

t1="there are 24 paid leaves"
t2="cat"

v1=model.encode(t1)
v2=model.encode(t2)
print(f"Cosine similarity between t1 and t2: {cosine_similarity(v1, v2)}")