import json
import re

# loading chunks
with open("chunks_with_doc_info.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Chunks loaded:", len(chunks))
# removing lines which are not important for troubleshooting
NOISE_PATTERNS = [
    r"third[- ]party information disclaimer",
    r"microsoft makes no (representation|warranty)",
    r"need more help\??",
    r"for more information, see",
    r"learn more at https?://",
    r"visit the microsoft support",
    r"this article describes",
    r"applies to:",
    r"was this helpful\??",
    r"feedback",
]
# cleaning the chunks to remove unnecessary lines
def clean_chunk_text(text):
    cleaned_lines = []

    for line in text.split("\n"):
        lower = line.lower()

        # Skip pure noise lines
        if any(re.search(p, lower) for p in NOISE_PATTERNS):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()
def split_large_chunk(text, max_words=600):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        part = " ".join(words[i:i+max_words])
        chunks.append(part)

    return chunks

cleaned_chunks = []

for c in chunks:
    cleaned_text = clean_chunk_text(c["text"])

    # Skip empty chunks (rare but safe)
    if not cleaned_text:
        continue

    cleaned_chunks.append({
        **c,
        "text": cleaned_text
    })
print("Chunks after cleanup:", len(cleaned_chunks))

'''for c in cleaned_chunks[:3]:
    print("\nISSUE:", c["issue_title"])
    print("CHUNK:\n", c["text"])
lengths = [len(c["text"].split()) for c in cleaned_chunks]
print("Min:", min(lengths))
print("Avg:", sum(lengths)//len(lengths))
print("Max:", max(lengths))
'''

MIN_WORDS = 40

final_chunks = [
    c for c in cleaned_chunks
    if len(c["text"].split()) >= MIN_WORDS
]

print("Chunks after removing tiny ones:", len(final_chunks))
balanced_chunks = []

for c in final_chunks:
    words = len(c["text"].split())

    if words > 600: # splitting if chunk size is too large
        parts = split_large_chunk(c["text"], max_words=600)
        for idx, part in enumerate(parts):
            balanced_chunks.append({
                **c,
                "chunk_id": f"{c['chunk_id']}_{idx}",
                "text": part
            })
    else:
        balanced_chunks.append(c)

# sanity check
print("Final balanced chunks:", len(balanced_chunks))
lengths = [len(c["text"].split()) for c in balanced_chunks]
print("Min:", min(lengths))
print("Avg:", sum(lengths)//len(lengths))
print("Max:", max(lengths)) # not allowing too large chunks which can create problem during prompt

with open("chunks_cleaned_with_doc.json", "w", encoding="utf-8") as f:
    json.dump(balanced_chunks, f, ensure_ascii=False, indent=2)