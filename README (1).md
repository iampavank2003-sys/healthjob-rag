# 🩺 Healthcare Job Matcher (RAG)

A Retrieval-Augmented Generation (RAG) app that matches a candidate profile to healthcare job postings. It retrieves the most relevant postings from a vector database, then an LLM explains how well each one fits, using only the retrieved postings.

**Live demo:** _add your Streamlit link here_

## How it works
1. **Ingest** (`ingest.py`): job postings from `data/jobs.json` are converted into embeddings (all-MiniLM-L6-v2) and stored in a Chroma vector database.
2. **Retrieve** (`search.py`): the candidate profile is embedded and the closest postings are returned by cosine similarity.
3. **Generate** (`generate.py`): the retrieved postings are passed to a Gemini model with a prompt that restricts it to the provided context. Two prompt versions are included:
   - `v1`: explains why each job fits or does not fit
   - `v2`: ranks the jobs and lists one missing requirement per job
   The script retries on server errors and falls back across several models.
4. **App** (`app.py`): a Streamlit interface to enter a profile, choose the prompt version and number of jobs, and view the retrieved jobs and the explanation.

## Tech stack
Python, ChromaDB, sentence embeddings (all-MiniLM-L6-v2), Google Gemini API, Streamlit

## Run locally
```
pip install -r requirements.txt
python ingest.py
python search.py "ICU nurse with ventilator experience"
set GEMINI_API_KEY=your-key        # Windows (use export on Mac/Linux)
python generate.py "ICU nurse with ventilator experience"
streamlit run app.py
```
Get a free API key at https://aistudio.google.com/apikey. Never commit your key.

## Results
- **Retrieval:** 35 test queries over a 40-posting sample dataset, 100% Top-1 and Top-3 accuracy. Queries and postings were written for this demo, so wording overlaps and real-world accuracy would be lower.
- **Prompt comparison:** on 10 test queries, both prompts named the correct job every time. In my manual quality scoring (1-5), v1 (fit explanation) averaged 5.0 and v2 (ranking plus missing requirements) averaged 4.0. v2 sometimes reported no missing requirements when the posting listed requirements the candidate profile did not show. Small sample, single rater.
- Raw results are in the `evaluation/` folder.

## Data
`data/jobs.json` is a small **sample dataset** of 40 healthcare job postings (including many similar roles) written for this demo. It is not real job data.

## Project structure
```
app.py            Streamlit web app
ingest.py         builds the vector database
search.py         retrieval
generate.py       LLM answer generation, two prompt versions
list_models.py    lists Gemini models available to your key
data/jobs.json    sample job postings
```

## Author
Pavan K, [GitHub](https://github.com/iampavank2003), [LinkedIn](https://linkedin.com/in/pavank2003)
