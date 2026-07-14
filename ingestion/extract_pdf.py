import pdfplumber
import re
from collections import Counter

def extract_and_clean_pdf(pdf_path):

    # checking if  a particular is part of a common header or footer which is unimportant for troubleshooting
    def is_header_footer(line, count):
        if re.match(r"^\d+\.", line):
            return False # not removing numbered lines
        return (
            count > 30 and
            len(line) < 80 and
            not line.endswith(".")
        )
    # removing lines which are headers or footers
    def clean_page_safe(text, line_counter):
        lines = text.split("\n")
        cleaned = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if is_header_footer(stripped, line_counter[stripped]):
                continue

            cleaned.append(line)

        return "\n".join(cleaned)

    # fixing lines going onto the next line without ending properly giving no semantic sense
    def fix_broken_lines(text):
        lines = text.split("\n")
        merged = []
        buffer = ""
        in_command = False

        for line in lines:
            l = line.strip().lower()

            if "powershell" in l or l.startswith("get-") or "Console" in l:
                in_command = True
                if buffer:
                    merged.append(buffer)
                    buffer = ""
                merged.append(line)
                continue

            if in_command:
                if l == "":
                    in_command = False
                merged.append(line)
                continue

            # Normal prose logic
            if re.match(r"^\d+\.", line):
                if buffer:
                    merged.append(buffer)
                buffer = line
            elif buffer.endswith((".", ":", "?", "!")):
                merged.append(buffer)
                buffer = line
            else:
                buffer += " " + line

        if buffer:
            merged.append(buffer)

        return "\n".join(merged)

    # removing troubleshoot information related to admin as they are not important to solve
    
    text = ""
    pages=[]
    with pdfplumber.open(f"{pdf_path}") as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
            pages.append(page.extract_text())


    
    line_counter = Counter()
    # separating header and footer lines by counting their occurences in the top and bottom of page
    for p in pages:
        lines = [l.strip() for l in p.split("\n") if l.strip()]
        for line in lines[:3] + lines[-3:]:  # top & bottom lines only
            line_counter[line] += 1

    # filtering the pages
    filtered_pages = []
    for p in pages:
            
            filtered_p=clean_page_safe(p,line_counter)
            filtered_p=fix_broken_lines(filtered_p)
            lines = [l.strip() for l in filtered_p.split("\n") if l.strip()]
            if(len(filtered_p)>200 and len(lines)>3):
                filtered_pages.append(filtered_p)
    return filtered_pages   
