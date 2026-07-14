import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HUB_URL ="https://learn.microsoft.com/en-us/troubleshoot/microsoftteams/teams-welcome" 
# Keywords that indicate useful troubleshooting pages
KEEP_KEYWORDS = [
    "not working",
    "cannot",
    "fails",
    "error",
    "sign-in",
    "launch",
    "meeting",
    "audio",
    "video",
    "chat",
    "call"
]

# Keywords that indicate admin / infra pages (exclude)
DROP_KEYWORDS = [
    "admin",
    "tenant",
    "policy",
    "autodiscover",
    "exchange",
    "powershell",
    "hybrid",
    "deployment",
    "licensing"
]

def should_keep(title: str) -> bool:
    title = title.lower()

    if any(k in title for k in DROP_KEYWORDS):
        return False

    if any(k in title for k in KEEP_KEYWORDS):
        return True

    return False


def extract_filtered_links():
    response = requests.get(HUB_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)

        if not text or "/troubleshoot/microsoftteams/" not in href:
            continue

        full_url = urljoin("https://learn.microsoft.com", href)

        if should_keep(text):
            links.append({
                "title": text,
                "url": full_url
            })

    return links


if __name__ == "__main__":
    filtered = extract_filtered_links()

    print(f"Selected {len(filtered)} documents:\n")
    for i, item in enumerate(filtered, 1):
        print(f"{i}. {item['title']}")
        print(f"   {item['url']}\n")
