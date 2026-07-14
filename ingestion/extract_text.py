from ingestion.extract_pdf import extract_and_clean_pdf
from ingestion.extract_url import extract_and_clean_url

def extract_text(document):
    if document["source_type"] == "pdf":
        return extract_and_clean_pdf(document["source_path"])

    if document["source_type"] == "url":
        return extract_and_clean_url(document["source_path"])

    raise ValueError("Unsupported source type")
