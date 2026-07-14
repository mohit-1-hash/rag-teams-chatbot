import requests
from bs4 import BeautifulSoup

def extract_and_clean_url(path):
    html = requests.get(path, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    pages = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 200]
    return pages
