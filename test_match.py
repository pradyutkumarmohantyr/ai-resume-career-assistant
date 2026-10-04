from src.parser import read_resume
from src.extractor import extract_skills
from src.matcher import match_score

resume = extract_skills(read_resume("data/resume.pdf"))
jd = extract_skills(open("data/jd.txt", encoding="utf-8").read())

print(match_score(resume["skills"], jd["skills"]))