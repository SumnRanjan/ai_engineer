import os
import json
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore
from pydantic import BaseModel  # type: ignore

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(".....API KEY NOT FOUND.....")

client=Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role="user"

class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}

system_prompt=f"""
Extract the personal information from the ticket strictly based on this schema and give a json output.
{schema}
"""

system_message={
    "role":"system",
    "content" : system_prompt
}

text = "Hello, my name is Suman Ranjan. I have an iPhone which is not working at all. My address is Deoghar, Jharkhand. My email is abc@gmail.com. My contact number is 82134."
prompt=f""" 
This is a customer ticket. Please extract the personal information from this.
{text}
"""
message={
    "role":role,
    "content":prompt
}

messages=[system_message,message]

response=client.chat.completions.create(model=model, messages=messages, response_format=response_format) 

answer=response.choices[0].message.content
# print(answer)


# how to read json file
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)

