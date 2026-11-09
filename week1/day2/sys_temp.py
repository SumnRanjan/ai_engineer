import os
from pathlib import Path
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from groq import Groq # type: ignore

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(".....API KEY NOT FOUND.....")

client=Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role="user"
prompt="Suggest name for my food compnay"

#System role
message_system={
    "role": "system",
    # "content" : "you are my loving girlfriend"
    "content" : "you are a brand manager who suggests name for food brand"

}

message={
    "role":role,
    "content":prompt
}

messages=[message_system,message]

#Temperature by default is 0 - range [0 , 2]
response=client.chat.completions.create(model=model,messages=messages,temperature=1)

answer=response.choices[0].message.content
print(answer)