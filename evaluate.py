import glob
import os
from src.parser import read_resume
from src.extractor import extract_skills
from src.matcher import match_score

resume = extract_skills(read_resume("data/resume.pdf"))

rows = []
for path in sorted(glob.glob("data/jds/*.txt")):
    name = os.path.basename(path)
    label = name.split("_")[0]
    text = open(path, encoding="utf-8").read()
    jd = extract_skills(text)
    score = match_score(resume["skills"], jd["skills"])["final_score"]
    rows.append((label, name, score))
    print(f"{label:8} {name:20} {score}")

groups = {}
for label, name, score in rows:
    groups.setdefault(label, []).append(score)

print("\nAVERAGE SCORE BY GROUP")
for label in ["fit", "partial", "poor"]:
    if label in groups:
        print(f"  {label}: {sum(groups[label]) / len(groups[label]):.1f}")

def pair_accuracy(high, low):
    pairs = [(h, l) for h in groups.get(high, []) for l in groups.get(low, [])]
    if not pairs:
        return None
    return sum(h > l for h, l in pairs) / len(pairs)

print("\nRANKING CHECK")
for high, low in [("fit", "poor"), ("fit", "partial"), ("partial", "poor")]:
    acc = pair_accuracy(high, low)
    if acc is not None:
        print(f"  {high} scored above {low} in {acc * 100:.0f}% of pairs")