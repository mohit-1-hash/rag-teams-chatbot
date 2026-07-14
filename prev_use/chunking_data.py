import json
import re

with open("issues.json", "r", encoding="utf-8") as f:
    final_issues = json.load(f)

print("Issues loaded:", len(final_issues))

#checking if a line is a step or line
def is_step(line):
    return bool(re.match(r"^\d+\.", line.strip()))

# creating chunks from issue based information
def chunk_issue(issue, max_words=180):
    chunks = []
    current_chunk = []
    word_count = 0

    for line in issue["content"]:
        words = len(line.split())

        # If chunk is big and a new step starts then split
        if word_count >= max_words and is_step(line):
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0

        current_chunk.append(line)
        word_count += words

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# loading all chunks for each issue into all_chunks
all_chunks = []
for issue_id, issue in enumerate(final_issues, start=1):
    chunks = chunk_issue(issue)

    for idx, chunk in enumerate(chunks):
        all_chunks.append({
            "issue_id": issue_id,
            "issue_title": issue["issue_title"],
            "chunk_id": idx,
            "text": chunk,
            "document_title":issue["document_title"],
            "document_url":issue["document_url"],
        })
print("Total chunks created:", len(all_chunks))

# adding chunks into chunks json
with open("chunks_with_doc_info.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)
