import streamlit as st
from pipeline import run_pipeline # your existing ingestion pipeline

st.header("Admin Ingest Data")

source_type = st.selectbox(
    "Source type",
    ["pdf", "url"]
)

source_value = st.text_input(
    "PDF path or URL",
    placeholder="https://learn.microsoft.com/..."
)
service= st.selectbox(
    "Service",
    ["Outlook","Teams"]
)

if st.button("Ingest"):
    if not source_value:
        st.error("Please provide a source.")
    else:
        with st.spinner("Running ingestion pipeline..."):
            try:
                run_pipeline(source_type, source_value,service)
                st.success("Ingestion completed successfully.")
            except Exception as e:
                st.error(f"Ingestion failed: {e}")
