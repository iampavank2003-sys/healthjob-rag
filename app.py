"""Step 4: Streamlit web app for the healthcare job-matching RAG assistant."""
import os
import streamlit as st

# On Streamlit Cloud the key comes from Secrets; locally from the environment variable
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# Build the vector database on first run (the chroma_db folder is not stored on GitHub)
if not os.path.exists("chroma_db"):
    import ingest  # noqa: F401  (running this file builds the database)

from search import retrieve
from generate import answer

st.set_page_config(page_title="Healthcare Job Matcher (RAG)", page_icon="🩺")
st.title("🩺 Healthcare Job Matcher")
st.caption("RAG demo: retrieves matching job postings from a vector database, then an LLM explains the fit using only those postings. Sample dataset.")

profile = st.text_area("Describe the candidate", "ICU nurse with 3 years of ventilator experience", height=100)
col1, col2 = st.columns(2)
version = col1.selectbox("Prompt version", ["v1", "v2"], help="v1: explain fit. v2: rank and list missing requirements.")
k = col2.slider("Jobs to retrieve", 1, 5, 3)

if st.button("Find matches", type="primary") and profile.strip():
    with st.spinner("Searching jobs..."):
        jobs = retrieve(profile, k)
    st.subheader("Retrieved jobs")
    for j in jobs:
        st.write(f"**{j['title']}** ({j['city']}), distance {j['distance']:.3f}")
    with st.spinner("Generating explanation..."):
        try:
            st.subheader("AI explanation")
            st.write(answer(profile, version, k))
        except Exception as e:
            st.error(f"The AI service is busy or unavailable. Try again in a minute. ({type(e).__name__})")
