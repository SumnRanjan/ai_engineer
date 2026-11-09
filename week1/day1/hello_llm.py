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
prompt="Do you know virat kholi"
message={
    "role":role,
    "content":prompt
}

messages=[message]

response=client.chat.completions.create(model=model,messages=messages)
print(response)

print("#############################")

answer=response.choices[0].message.content
print(answer)