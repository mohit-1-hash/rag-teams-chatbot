
import re

def chunk_issues(final_issues):


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
                "issue_id" : issue_id,
                "issue_title": issue["issue_title"],
                "chunk_id": idx,
                "text": chunk,
                "document_id": issue["document_id"],
            })
    #print("Total chunks created:", len(all_chunks))

    # adding chunks into chunks json

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

    for c in all_chunks:
        cleaned_text = clean_chunk_text(c["text"])

        # Skip empty chunks (rare but safe)
        if not cleaned_text:
            continue

        cleaned_chunks.append({
            **c,
            "text": cleaned_text
        })
    print("Chunks after cleanup:", len(cleaned_chunks))
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
    
    return balanced_chunks