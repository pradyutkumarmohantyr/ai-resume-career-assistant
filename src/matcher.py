from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def clean(items):
    return sorted({s.strip().lower() for s in items if s.strip()})

def match_score(resume_skills, jd_skills, threshold=0.5):
    resume = clean(resume_skills)
    jd = clean(jd_skills)

    if not resume or not jd:
        return {"keyword_score": 0, "semantic_score": 0, "final_score": 0}

    # 1. Keyword score: job skills that appear exactly in the resume
    keyword = len(set(jd) & set(resume)) / len(jd)

    # 2. Semantic score: job skills that have a clearly similar resume skill
    resume_emb = model.encode(resume, convert_to_tensor=True)
    jd_emb = model.encode(jd, convert_to_tensor=True)
    best = util.cos_sim(jd_emb, resume_emb).max(dim=1).values
    semantic = float((best >= threshold).float().mean())

    # 3. Final score
    final = 0.4 * keyword + 0.6 * semantic

    return {
        "keyword_score": round(keyword * 100, 1),
        "semantic_score": round(semantic * 100, 1),
        "final_score": round(final * 100, 1),
    }