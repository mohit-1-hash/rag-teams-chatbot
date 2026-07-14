import re
from ingestion.window import merge_page_windows
def extract_issues(pages,doc_id):
    # using merged window pages to get issues
    issues=[]

    ISSUE_REGEX = re.compile(
    r"^(issue|problem|error|symptom|troubleshoot|fix|resolve)\b.*",
    re.IGNORECASE
)

    
    def extract_issue_title(raw_title):
        title = raw_title.lower()

        # remove dates
        title = re.sub(r"\d{2}/\d{2}/\d{4}.*$", "", title)

        # remove "Applies to" section
        title = re.sub(r"applies to:.*", "", title)

        # remove leading verbs normalization
        title = re.sub(r"^(resolve|troubleshoot|fix)\s+", "", title)
        
        title=re.sub(r"(important |\s+note).*$","",title)
        # normalize spaces
        title = re.sub(r"\s+", " ", title)

        return title.strip()
    def is_bad_title(title):
        bad_patterns = [
            "follow these steps",
            "run checks",
            "manually",
            "note these troubleshooting steps",
            "if you want to",
            "check whether the issue is resolved",
            "run the",
        ]
        t = title.lower()
        return any(p in t for p in bad_patterns)

    def dedupe_preserve_order(lines): # to remove lines when they are repeated in issues
        seen = set()
        unique = []
        for line in lines:
            key = line.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(line)
        return unique
    pages = merge_page_windows(pages)
    issues = []
    current_issue = None

    for page in pages:
        lines = [l.strip() for l in page.split("\n") if l.strip()]

        for line in lines:
            if ISSUE_REGEX.match(line) and not is_bad_title(line):
        # real issue boundary
                if current_issue:
                    issues.append(current_issue)

                current_issue = {
                    "title": line,
                    "content": []
                    }
            else:
            # everything else (including bad titles) is content
                if current_issue:
                    current_issue["content"].append(line)

    # Save last issue
    if current_issue:
        issues.append(current_issue)
    if not issues:
    # Fallback: treat whole document as a single issue
        merged_issues = [{
        "issue_title": "General troubleshooting information",
        "content": [
            line for page in pages for line in page.split("\n") if line.strip()
        ],
        "document_id": doc_id
    }]
        return merged_issues

    #print(len(issues))
    merged_issues = {}
    # merging issues together if they have same title because of duplication while creating windows
    for issue in issues:
        clean_title = extract_issue_title(issue["title"])

        if clean_title not in merged_issues:
            #print(clean_title)
            merged_issues[clean_title] = {
                "raw_title": issue["title"],   # keep first full title for display
                "issue_title":clean_title,
                "content": [],
                "document_id":doc_id,
            }

        merged_issues[clean_title]["content"].extend(issue["content"])
    final_issues = []
    for issue in merged_issues.values():
        issue["content"] = dedupe_preserve_order(issue["content"])
        final_issues.append(issue)
        #print(issue)
    #print(final_issues[:3])
    #print("Final unique issues:", len(final_issues))

    return final_issues
