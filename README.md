# AI Resume & Career Assistant

**Live demo:** https://ai-resume-career-assistant-dsonqwbvxmh48cwawvnfsf.streamlit.app/

Upload a resume (PDF) and paste a job description to get a match score, a skill-gap analysis, and tailored resume bullet points.

## What it does
- **Match score:** combines exact keyword overlap with semantic similarity between resume skills and job skills.
- **Skill-gap analysis:** lists matched skills, missing skills, and the top priority gaps.
- **Bullet tailoring:** rewrites the most relevant resume bullets for the job, without inventing tools or numbers.

## How it works
1. `pypdf` reads the resume text.
2. An LLM (Groq, `openai/gpt-oss-20b`) extracts skills from the resume and the job description as JSON.
3. `sentence-transformers` (`all-MiniLM-L6-v2`) embeds the skills and compares them. A job skill counts as matched when a resume skill is clearly similar.
4. The LLM rewrites bullets using only facts from the resume.
5. A Streamlit app ties it together.

## Tech stack
Python, Streamlit, sentence-transformers, Groq API, pypdf

## Evaluation
Tested one resume against 14 job descriptions: 5 good fit, 4 partial fit, 5 unrelated.

| Group | Average match score |
|---|---|
| Good fit | 57.6% |
| Partial fit | 17.6% |
| Unrelated | 0.0% |

Good-fit jobs scored above partial-fit and unrelated jobs in every test pair. Run it with `python evaluate.py`.

## Limitations
- Small test set (14 jobs, one resume); job labels were assigned by job title.
- Skill extraction depends on the LLM, so results can vary slightly between runs.
- Long phrases such as "semantic search" or "LLM APIs (Groq, OpenAI)" can fail to match shorter resume wording.
- Scanned (image-only) PDFs are not supported.

## Run locally
1. `pip install -r requirements.txt`
2. Create a `.env` file with `GROQ_API_KEY=your_key`
3. `streamlit run app.py`