import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(".....API KEY NOT FOUND.....")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

#step 1: create a knowledge base
knowledge_base={
    "age" : "Batman is 35 years old",
    "net worth": "Batman has a net worth of 9.2 billion dollars",
}

#step 2 : retrieve relevant information from the knowledge base
def retrive_info(question):
    question=question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "net worth" in question:
        return knowledge_base["net worth"]
    else:
        return "Information not found."

def ask_llm(question):
    context= retrive_info(question)
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
    response=client.chat.completions.create(model=model, messages=messages)
    answer= response.choices[0].message.content
    return answer

print(ask_llm("who is batman age ?"))
print(ask_llm("what is batman net worth ?"))
print(ask_llm("is he rich ?")) 



