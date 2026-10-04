import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_skills(text):
    prompt = f"""Read the text below and return ONLY a JSON object with these keys:
"skills": list of technical skills and tools,
"keywords": list of important domain keywords.
Do not add anything that is not in the text.

TEXT:
{text}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)