import os
from groq import Groq
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class MatchingNode:

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        resume = state.get("resume_json", {})
        jd = state.get("jd_json", {})

        prompt = f"""
You are an expert AI resume-job matching system.

Your task is to compare the resume and job description.

Return STRICT JSON ONLY.

RULES:
- No explanation
- No markdown
- No extra text

OUTPUT FORMAT:
{{
  "matched_skills": [],
  "missing_skills": [],
  "match_summary": ""
}}

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        import json, re
        raw = response.choices[0].message.content

        try:
            cleaned = re.search(r"\{.*\}", raw, re.DOTALL)
            result = json.loads(cleaned.group())
        except:
            result = {
                "matched_skills": [],
                "missing_skills": [],
                "match_summary": ""
            }

        state["matched"] = result.get("matched_skills", [])
        state["missing"] = result.get("missing_skills", [])
        state["summary"] = result.get("match_summary", "")

        return state