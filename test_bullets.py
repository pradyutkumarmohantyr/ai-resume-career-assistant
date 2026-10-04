from src.parser import read_resume
from src.extractor import extract_skills
from src.gap import skill_gap
from src.bullets import tailor_bullets

resume_text = read_resume("data/resume.pdf")
jd_text = open("data/jd.txt", encoding="utf-8").read()

resume = extract_skills(resume_text)
jd = extract_skills(jd_text)
gap = skill_gap(resume["skills"], jd["skills"], jd_text)

result = tailor_bullets(resume_text, jd_text, gap["missing"])

for i, b in enumerate(result["bullets"], 1):
    print(f"\n{i}. ORIGINAL: {b['original']}")
    print(f"   TAILORED: {b['tailored']}")