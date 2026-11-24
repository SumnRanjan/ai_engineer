# tiktoken = OpenAI's tokenizer library.
# A tokenizer converts text into tokens (numbers), the same way OpenAI-style models do.
# LLMs never read letters; they only read these token IDs.
# Note: you don't need tiktoken to call an LLM. The provider (Groq/OpenAI) tokenizes on its servers.
# Use tiktoken locally to COUNT tokens, ESTIMATE cost, CHECK context limits and CHUNK text for RAG.
# Rule of thumb: 1 token ≈ 4 characters ≈ 3/4 of an English word.

import tiktoken  # type: ignore
enc = tiktoken.get_encoding("o200k_base")
# encode(): text -> list of token IDs.
tokens = enc.encode("Fix the total bug")

for t in tokens:
    print(t, repr(enc.decode([t])))

print(tokens)       
print(len(tokens))

enc.decode(tokens)
print(enc.decode(tokens)) 