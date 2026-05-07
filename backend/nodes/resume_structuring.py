import json
import re
from groq import Groq
import os


class ResumeStructurer:
    
    def __call__(self, state):
        return self.run(state)

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # 🔧 JSON safe parser
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

    # 🧠 BASIC VALIDATION (added)
    def is_likely_resume(self, text: str):
        text = text.lower()
        return any(k in text for k in ["skills", "education", "projects", "experience"])

    # 🧠 MAIN NODE FUNCTION
    def run(self, state: dict):
        resume_text = state.get("resume_text", "")

        # 🚨 HARD VALIDATION (added)
        if not resume_text or len(resume_text.strip()) < 100:
            state["resume_json"] = {}
            state["resume_error"] = "Invalid or empty resume"
            return state

        # 🚨 WARNING (added)
        if not self.is_likely_resume(resume_text):
            state["resume_warning"] = "This may not be a proper resume"

        prompt = f"""
You are a STRICT resume information extraction system.

Your ONLY task is to convert the given resume into a structured JSON object.

🚨 ABSOLUTE RULES:
- Output ONLY valid JSON
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include ``` backticks
- Do NOT add extra text before or after JSON
- Do NOT summarize or shorten information
- Do NOT hallucinate missing data

📌 OUTPUT FORMAT (must follow exactly):
{{
  "name": "",
  "email": "",
  "phone": "",
  "skills": [],
  "education": [],
  "projects": [
    {{
      "name": "",
      "description": "",
      "tech_stack": [],
      "metrics": ""
    }}
  ],
  "experience": [],
  "certifications": []
}}

📌 EXTRA RULES:

SKILLS:
- Normalize into clean keywords
- Remove duplicates

PROJECTS:
- Keep full description, tech stack, metrics

EDUCATION:
- Keep institution + degree + year

EXPERIENCE:
- Keep full role and organization name

CERTIFICATIONS:
- List exactly as mentioned

GENERAL RULE:
- Extract ONLY factual information
- Missing → empty string/list

RESUME TEXT:
{resume_text}
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            raw_output = response.choices[0].message.content
            parsed = self.safe_parse_json(raw_output)

        except Exception as e:
            state["resume_json"] = {}
            state["resume_error"] = f"Extraction failed: {str(e)}"
            return state

        # 🧠 MINIMAL CONFIDENCE (added)
        confidence = 0
        if parsed.get("skills"):
            confidence += 0.4
        if parsed.get("projects"):
            confidence += 0.3
        if parsed.get("education"):
            confidence += 0.3

        state["resume_json"] = parsed
        state["resume_confidence"] = round(confidence, 2)

        return state