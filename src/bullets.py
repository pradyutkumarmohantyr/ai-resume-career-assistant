import os
import json
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def tailor_bullets(resume_text, jd_text, missing_skills, retries=3):
    prompt = f"""You are a resume coach. Using ONLY facts from the resume below,
pick the 5 bullets most relevant to the job description and rewrite them to fit it.

Rules:
- Start each bullet with a strong action verb such as Built, Designed, Engineered or Improved. Never start with the word "Accomplished".
- Keep the same measured result as the original. Do not change what was measured.
- End each bullet with a full stop.
- Use keywords from the job description only where the resume truly supports them.
- NEVER invent tools, numbers, or experience that are not in the resume.
- These skills are missing from the resume, so do NOT claim them: {missing_skills}
- Keep each bullet under 30 words.

Return ONLY a JSON object: {{"bullets": [{{"original": "...", "tailored": "..."}}]}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}"""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                reasoning_effort="low",
                temperature=0.3,
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            print(f"Attempt {attempt + 1} failed, retrying...")
            if attempt == retries - 1:
                raise
            time.sleep(1)