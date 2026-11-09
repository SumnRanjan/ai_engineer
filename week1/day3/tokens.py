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
prompt1 = "Hi!"
prompt2 = "Explain time travel in Detail but under 100 words"
prompt3 = "Write a 100 word essay on Machine learning"

prompts=[prompt1,prompt2,prompt3]

for prompt in prompts:
    message={
        "role":role,
        "content":prompt
    }

    messages=[message]
    response=client.chat.completions.create(model=model,messages=messages,max_tokens=500)
    usage=response.usage
    print(f"Prompt: {prompt} -->Your tokens: {usage.prompt_tokens}  completion_tokens: {usage.completion_tokens} total tokens: {usage.prompt_tokens + usage.completion_tokens} Finish Reason: {response.choices[0].finish_reason}")
