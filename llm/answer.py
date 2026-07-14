import os
import google.generativeai as genai
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv["GEMINI_API_KEY"])
llm = genai.GenerativeModel("gemini-2.5-flash-lite")

SYSTEM_PROMPT = """
You are a technical troubleshooting assistant for Microsoft Teams.

Rules:
- Use ONLY the provided context to answer.
- Combine steps only if they refer to the SAME troubleshooting method.
- Do not repeat section headings.
- Provide clear, step-by-step instructions.
- Do NOT invent new steps.
- If no solution exists, say:
  "I couldn't find a documented solution for this issue."
- End with a short IT support note.
- Prefer end-user troubleshooting steps. Exclude admin-only solutions unless explicitly asked.
"""

def dedupe_chunks(chunks):
    seen = set()
    unique = []
    for c in chunks:
        key = c.strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique

def build_prompt(query, chunks):
    context = "\n\n".join(chunks)
    return f"""
{SYSTEM_PROMPT}

Context:
{context}

User question:
{query}

Answer:
"""

def generate_answer(query, retrieved_rows):
    """
    retrieved_rows = list of dicts from DB:
    { issue_title, text }
    """
    print(retrieved_rows)
    if not retrieved_rows:
        return "I couldn't find a documented solution for this issue."

    '''# 🔹 choose dominant issue
    issue_counts = Counter(r["issue_title"] for r in retrieved_rows)
    main_issue = issue_counts.most_common(1)[0][0]
'''
    # 🔹 take top chunks for that issue
    chunks = [
        r["text"]
        for r in retrieved_rows
    ]
    print(chunks)
    print("reached here")
    chunks = dedupe_chunks(chunks)
    
    prompt = build_prompt(query, chunks)

    response = llm.generate_content(
        prompt,
        generation_config={
            "temperature": 0,
            "max_output_tokens": 1600
        }
    )

    return response.text
