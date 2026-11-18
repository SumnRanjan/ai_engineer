from langchain_text_splitters import (CharacterTextSplitter,RecursiveCharacterTextSplitter) # type: ignore

text = """
The detective entered the abandoned house just before midnight.
The rooms were silent, and the windows were covered with dust.
On the table, he found a bloodstained letter.

The man who did the crime was John.
Nobody in the village trusted him, but he had disappeared
three days before the murder. The detective immediately realized
that something was suspicious.

The next morning, the detective returned to the house.
Behind a loose brick, he discovered a photograph of John
standing beside the victim. This finally connected John
to the mysterious murder.
"""

# ============================================================
# 1. FIXED-SIZE CHUNKING
# ============================================================

fixed = CharacterTextSplitter(
    separator=" ",
    chunk_size=100,
    chunk_overlap=0,
    length_function=len
)

print("\n========== FIXED SIZE ==========")

for i, chunk in enumerate(fixed.split_text(text), 1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("------------------------")


# ============================================================
# 2. PARAGRAPH CHUNKING
# ============================================================

paragraph = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=200,
    chunk_overlap=0,
    length_function=len
)

print("\n========== PARAGRAPH CHUNKING ==========")

for i, chunk in enumerate(paragraph.split_text(text), 1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("------------------------")


# ============================================================
# 3. RECURSIVE CHARACTER CHUNKING
# ============================================================

recursive = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30,
)

print("\n========== RECURSIVE CHUNKING ==========")

for i, chunk in enumerate(recursive.split_text(text), 1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("------------------------")
