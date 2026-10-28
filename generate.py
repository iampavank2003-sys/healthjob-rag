"""Step 3: the 'G' in RAG. An LLM explains matches using ONLY the retrieved jobs.
Uses Google's free Gemini API. Key is read from the GEMINI_API_KEY environment variable."""
import os
import sys
import time
from google import genai
from google.genai import types
from google.genai import errors as genai_errors
from search import retrieve

client = genai.Client()  # reads GEMINI_API_KEY automatically
# Comma-separated list, tried in order. If one is busy, the next is used.
MODELS = os.environ.get("GEMINI_MODELS", os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-3.5-flash,gemini-3.8-flash")).split(",")

# Two prompt versions, so you can compare them later (your A/B test)
PROMPTS = {
    "v1": "You are a healthcare recruiter. Using ONLY the job postings below, "
          "explain briefly why each job fits the candidate. If a job does not fit, say so.",
    "v2": "You are a healthcare recruiter. Using ONLY the job postings below, rank them "
          "from best to worst fit for the candidate. For each, give one reason and one "
          "missing requirement. Never invent details that are not in the postings.",
}

def answer(profile: str, version: str = "v1", k: int = 3) -> str:
    jobs = retrieve(profile, k)
    context = "\n".join(f"- {j['title']} ({j['city']}): {j['text']}" for j in jobs)
    contents = f"Candidate profile: {profile}\n\nJob postings:\n{context}"
    config = types.GenerateContentConfig(system_instruction=PROMPTS[version], max_output_tokens=600)
    for attempt in range(4):  # servers are sometimes busy (503), so retry and fall back to other models
        for model in MODELS:
            try:
                return client.models.generate_content(model=model.strip(), contents=contents, config=config).text
            except genai_errors.ServerError:
                print(f"{model} is busy, trying again...")
        time.sleep(8 * (attempt + 1))
    raise RuntimeError("All models are busy right now. Try again in 10-15 minutes.")

if __name__ == "__main__":
    profile = " ".join(sys.argv[1:]) or "nurse with 3 years ICU experience"
    print(answer(profile))
