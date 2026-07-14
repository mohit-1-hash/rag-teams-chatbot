import streamlit as st
from pipeline import search
from llm.answer import generate_answer

st.header("Microsoft Teams Troubleshooting Assistant")

query = st.text_input(
    "Enter your Teams issue",
    placeholder="Issues when starting the new teams app"
)

if st.button("Get Solution"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching documentation..."):
            retrieved = search(query)
            answer = generate_answer(query, retrieved)

        st.subheader("Solution")
        st.markdown(answer)
