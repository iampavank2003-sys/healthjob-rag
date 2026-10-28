# Healthcare Job-Matching RAG Assistant
Retrieves matching healthcare jobs for a candidate profile, then (step 3) an LLM explains each match using only the retrieved postings.

## Run
    pip install -r requirements.txt
    python ingest.py
    python search.py "ICU nurse with ventilator experience"

Note: data/jobs.json is sample data. Expand it to 30-50 postings.
