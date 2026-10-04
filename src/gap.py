from src.matcher import model, clean, util

def skill_gap(resume_skills, jd_skills, jd_text="", threshold=0.5):
    resume = clean(resume_skills)
    jd = clean(jd_skills)

    if not resume or not jd:
        return {"matched": [], "missing": [], "priority_gaps": []}

    resume_emb = model.encode(resume, convert_to_tensor=True)
    jd_emb = model.encode(jd, convert_to_tensor=True)
    sims = util.cos_sim(jd_emb, resume_emb)

    matched, missing = [], []
    for i, skill in enumerate(jd):
        score, idx = sims[i].max(dim=0)
        if float(score) >= threshold:
            matched.append({
                "job_skill": skill,
                "resume_skill": resume[int(idx)],
                "similarity": round(float(score) * 100),
            })
        else:
            missing.append(skill)

    # Priority gaps: missing skills the job description mentions most often
    text = jd_text.lower()
    priority = sorted(missing, key=lambda s: text.count(s), reverse=True)[:5]

    return {"matched": matched, "missing": missing, "priority_gaps": priority}