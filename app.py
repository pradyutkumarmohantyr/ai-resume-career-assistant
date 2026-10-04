import streamlit as st
from src.parser import read_resume
from src.extractor import extract_skills
from src.matcher import match_score
from src.gap import skill_gap
from src.bullets import tailor_bullets

st.set_page_config(page_title="AI Resume & Career Assistant", page_icon="📄")
st.title("📄 AI Resume & Career Assistant")
st.write("Upload your resume and paste a job description to get a match score, skill gaps, and tailored bullet points.")
st.caption("Your resume text is sent to the Groq API for analysis and is not stored by this app.")

resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd_text = st.text_area("Paste the job description", height=250)

if st.button("Analyze", type="primary"):
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
        st.stop()

    with st.spinner("Analyzing... this takes about 20 seconds"):
        resume_text = read_resume(resume_file)
        if not resume_text.strip():
            st.error("Could not read text from this PDF. Try a text-based PDF, not a scanned one.")
            st.stop()

        resume = extract_skills(resume_text)
        jd = extract_skills(jd_text)
        scores = match_score(resume["skills"], jd["skills"])
        gap = skill_gap(resume["skills"], jd["skills"], jd_text)
        bullets = tailor_bullets(resume_text, jd_text, gap["missing"])

    st.header("Match score")
    st.metric("Overall match", f"{scores['final_score']}%")
    st.progress(min(int(scores["final_score"]), 100))
    c1, c2 = st.columns(2)
    c1.metric("Keyword match", f"{scores['keyword_score']}%")
    c2.metric("Semantic match", f"{scores['semantic_score']}%")

    st.header("Skill gap analysis")
    st.subheader("✅ Matched skills")
    for m in gap["matched"]:
        st.write(f"- **{m['job_skill']}** ← {m['resume_skill']} ({m['similarity']}%)")

    st.subheader("❌ Missing skills")
    for s in gap["missing"]:
        st.write(f"- {s}")

    st.subheader("🎯 Priority gaps to work on")
    for s in gap["priority_gaps"]:
        st.write(f"- {s}")

    st.header("Tailored resume bullets")
    st.caption("Always check each bullet is true for your own work before using it.")
    for b in bullets["bullets"]:
        st.markdown(f"**Original:** {b['original']}")
        st.markdown(f"**Tailored:** {b['tailored']}")
        st.divider()