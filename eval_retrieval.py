"""Step 5: measure retrieval quality on 20 test queries.
Each query has ONE expected job (40 postings, 35 queries). We check if it comes back first (Top-1) or in the top 3 (Top-3)."""
import csv
import chromadb

collection = chromadb.PersistentClient(path="chroma_db").get_collection("jobs")

# (query, expected job id). Job ids match data/jobs.json: job1 = ICU nurse, job2 = pediatric nurse, ...
TESTS = [
    ("nurse experienced with critically ill patients and life support machines", "job1"),
    ("intensive care nurse who speaks German", "job1"),
    ("nurse who enjoys working with kids and giving vaccines", "job2"),
    ("children's hospital nurse with pediatric certificate", "job2"),
    ("therapist helping people recover after knee or hip surgery", "job3"),
    ("physio with manual therapy skills for an outpatient clinic", "job3"),
    ("licensed doctor for family practice and long-term illnesses", "job4"),
    ("MD who wants to run primary care and diagnose patients", "job4"),
    ("technician experienced with MRI and CT scans", "job5"),
    ("radiographer who knows radiation safety", "job5"),
    ("laboratory scientist who analyzes blood samples", "job6"),
    ("medical technologist with lab quality control experience", "job6"),
    ("nurse with dementia care experience for a nursing home", "job7"),
    ("caregiver nurse for old people managing medications", "job7"),
    ("therapist who helps patients return to daily activities after injury", "job8"),
    ("hand therapy specialist in a hospital", "job8"),
    ("doctor specialising in anesthesia and pain control during operations", "job9"),
    ("board certified anesthetist", "job9"),
    ("pharmacist who counsels patients on medicines in a hospital", "job10"),
    ("someone who dispenses prescriptions", "job10"),
    # Harder queries: several similar jobs exist, so only specific details pick the right one
    ("nurse for premature babies, incubator experience", "job13"),
    ("nurse for heart patients with ECG skills", "job12"),
    ("nurse for walk-in emergencies and triage", "job11"),
    ("nurse who administers chemotherapy and supports cancer patients", "job15"),
    ("nurse who visits patients at home to change wound dressings", "job16"),
    ("nurse experienced with dialysis machines", "job18"),
    ("psychiatric nurse good at calming agitated patients", "job17"),
    ("physiotherapist for stroke patients, balance and gait training", "job20"),
    ("physiotherapist working with athletes, taping", "job19"),
    ("therapist for swallowing and speech problems", "job21"),
    ("therapist for children with developmental delays and sensory issues", "job22"),
    ("specialist doctor who reads CT and MRI scans and writes reports", "job29"),
    ("pharmacist who checks drug interactions on hospital wards and advises doctors", "job33"),
    ("doctor for skin cancer screening", "job28"),
    ("entry-level hospital helper, no degree needed", "job40"),
]

top1 = top3 = 0
rows = []
for query, expected in TESTS:
    res = collection.query(query_texts=[query], n_results=3)
    ids = res["ids"][0]
    hit1, hit3 = ids[0] == expected, expected in ids
    top1 += hit1
    top3 += hit3
    rows.append([query, expected, ids[0], "yes" if hit1 else "NO", "yes" if hit3 else "NO"])
    print(f"{'OK ' if hit1 else 'MISS'}  expected={expected:6} got={ids[0]:6} | {query}")

n = len(TESTS)
print(f"\nTop-1 accuracy: {top1}/{n} = {top1/n:.0%}")
print(f"Top-3 accuracy: {top3}/{n} = {top3/n:.0%}")

with open("retrieval_results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["query", "expected", "top_result", "top1_hit", "top3_hit"])
    w.writerows(rows)
print("Saved retrieval_results.csv")
