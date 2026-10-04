import os
import json
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("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"))

def extract_skills(text, retries=3):
    prompt = f"""Read the text below and return ONLY a JSON object with these keys:
"skills": list of technical skills and tools,
"keywords": list of important domain keywords.
Do not add anything that is not in the text.

TEXT:
{text}"""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                reasoning_effort="low",
                temperature=0,
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed, retrying...")
            if attempt == retries - 1:
                raise
            time.sleep(1)