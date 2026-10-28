"""Step 6: compare prompt v1 vs v2 on 10 test queries.
Automatic checks (rough, title-based):
  - found_expected: the expected job's title appears in the answer
  - invented: the answer names a job that was NOT in the retrieved results (possible hallucination)
  - words: answer length
It also saves every answer to prompt_comparison.csv so YOU can score quality 1-5 by hand."""
import csv
import json
import time
from search import retrieve
from generate import answer

TITLES = {j["id"]: j["title"] for j in json.load(open("data/jobs.json"))}
TESTS = [
    ("nurse for premature babies, incubator experience", "job13"),
    ("nurse for heart patients with ECG skills", "job12"),
    ("nurse for walk-in emergencies and triage", "job11"),
    ("physiotherapist for stroke patients, balance and gait training", "job20"),
    ("physiotherapist working with athletes, taping", "job19"),
    ("therapist for swallowing and speech problems", "job21"),
    ("specialist doctor who reads CT and MRI scans and writes reports", "job29"),
    ("pharmacist who checks drug interactions on hospital wards and advises doctors", "job33"),
    ("doctor for skin cancer screening", "job28"),
    ("entry-level hospital helper, no degree needed", "job40"),
]

stats = {v: {"found": 0, "invented": 0, "words": 0} for v in ("v1", "v2")}
rows = []
for query, expected in TESTS:
    retrieved = {j["title"] for j in retrieve(query, 3)}
    for v in ("v1", "v2"):
        text = answer(query, v)
        found = TITLES[expected] in text
        invented = [t for t in TITLES.values() if t not in retrieved and t in text]
        stats[v]["found"] += found
        stats[v]["invented"] += len(invented)
        stats[v]["words"] += len(text.split())
        rows.append([query, v, found, "; ".join(invented), len(text.split()), "", text])
        print(f"{v} | found={found} invented={len(invented)} | {query}")
        time.sleep(6)  # stay under the free-tier rate limit

n = len(TESTS)
print("\n=== Summary ===")
for v, s in stats.items():
    print(f"{v}: expected job named {s['found']}/{n}, invented jobs {s['invented']}, avg words {s['words']/n:.0f}")

with open("prompt_comparison.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["query", "prompt", "found_expected", "invented_jobs", "words", "YOUR_SCORE_1_to_5", "answer"])
    w.writerows(rows)
print("Saved prompt_comparison.csv. Open it in Excel and fill YOUR_SCORE_1_to_5 for each answer.")
