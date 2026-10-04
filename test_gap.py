from src.parser import read_resume
from src.extractor import extract_skills
from src.gap import skill_gap

jd_text = open("data/jd.txt", encoding="utf-8").read()
resume = extract_skills(read_resume("data/resume.pdf"))
jd = extract_skills(jd_text)

result = skill_gap(resume["skills"], jd["skills"], jd_text)

print("\nMATCHED:")
for m in result["matched"]:
    print(f"  {m['job_skill']}  <-  {m['resume_skill']} ({m['similarity']}%)")

print("\nMISSING:")
for s in result["missing"]:
    print(f"  {s}")

print("\nPRIORITY GAPS:")
for s in result["priority_gaps"]:
    print(f"  {s}")