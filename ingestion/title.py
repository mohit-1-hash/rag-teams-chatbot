import requests
from bs4 import BeautifulSoup
from pathlib import Path
def derive_title(source_type: str, source_path: str) -> str:
    if source_type == "url":
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            html = requests.get(source_path, headers=headers, timeout=30).text
            soup = BeautifulSoup(html, "html.parser")
            if soup.title and soup.title.string:
                return soup.title.string.strip()
        except Exception:
            pass

    if source_type == "pdf":
        return Path(source_path).stem

    return "Untitled document"
