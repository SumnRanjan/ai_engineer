import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore
import numpy as np # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") #384
groq_model = "openai/gpt-oss-120b"

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(".....API KEY NOT FOUND.....")

client=Groq(api_key=my_api_key)

documents = [
    "Employees receive 24 days of paid leave per year.",
   
    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",
   
    "Employees receive Rs 3000 per month for gym reimbursement.",
   
    "Employees can claim Rs 2000 per month for home internet.",
   
    "Employees have a 90 day notice period."
]

document_embeddings = model.encode(documents)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(qembedding):
    scores = []  # 0.4 
    for i, document in  enumerate(document_embeddings):
        score=cosine_similarity(qembedding,document )
        scores.append((score,documents[i]))
    scores.sort(reverse=True)
    return scores[0]  

def ask_llm(question,context):
    system_prompt=f"""Answer in one sentence anwer based on context. do not hallucinate. context: {context}"""
    system_message={
        "role":"system",    
        "content": system_prompt
    }
    message={
        "role":"user",
        "content": question
    }
    messages= [system_message, message]
    response=client.chat.completions.create(model=groq_model, messages=messages)
    answer= response.choices[0].message.content
    return answer

query = "How much vacation do I get?"
qembedding = model.encode(query)
score, context = retrieve(qembedding)
# print(f"Score: {score}, Context: {context}")
answer = ask_llm(query, context)
print(f"Answer: {answer}")
