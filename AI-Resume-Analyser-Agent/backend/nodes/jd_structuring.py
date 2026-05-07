import json
import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)


class JDStructurer:
    
    def __call__(self, state):
        return self.run(state)

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # 🔧 safe JSON parser
    def safe_parse_json(self, raw_output: str):
        try:
            return json.loads(raw_output)
        except:
            pass

        match = re.search(r"\{[\s\S]*\}", raw_output)
        if match:
            try:
                return json.loads(match.group())
            except:
                return {}

        return {}

    # 🧠 MAIN NODE
    def run(self, state: dict):
        jd_text = state["jd_text"]

        prompt = f"""
You are a STRICT job description parser.

Your ONLY task is to convert the given job description into structured JSON.

🚨 RULES:
- Output ONLY valid JSON
- No markdown
- No ``` fences
- No explanation
- Do NOT add text before or after JSON
- Do NOT hallucinate missing data

📌 FORMAT:
{{
  "title": "",
  "skills_required": [],
  "responsibilities": [],
  "experience_required": "",
  "tools_technologies": [],
  "education": ""
}}

📌 EXTRA RULES:
- Extract ALL explicitly mentioned skills
- Keep tools separate from skills
- Normalize skills (e.g., "Scikit-learn", "FastAPI")
- Do NOT remove important details

JOB DESCRIPTION:
{jd_text}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        raw_output = response.choices[0].message.content

        state["jd_json"] = self.safe_parse_json(raw_output)

        return state