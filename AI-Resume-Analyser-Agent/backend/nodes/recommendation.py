import os
from groq import Groq
from typing import Dict, Any
from dotenv import load_dotenv
import json
import re

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class RecommendationNode:

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        missing = state.get("missing", [])
        jd = state.get("jd_json", {})
        resume = state.get("resume_json", {})

        prompt = f"""
You are an expert AI career advisor.

Your task is to generate HIGH-VALUE, ACTIONABLE recommendations to improve a candidate's resume.

🚨 STRICT RULES:
- Return ONLY valid JSON
- No markdown
- No explanations outside JSON

📌 OUTPUT FORMAT:
{{
  "recommendations": [
    {{
      "skill": "",
      "priority": "High | Medium | Low",
      "why_needed": "",
      "how_to_learn": "",
      "projects_to_build": "",
      "resources": []
    }}
  ]
}}

📌 INSTRUCTIONS:
- Use missing skills to generate recommendations
- Prioritize skills based on job description importance
- Be SPECIFIC (not generic advice)
- Include real-world suggestions (projects, use-cases)
- Keep recommendations practical for a student/fresher
- Resources can include platforms like courses, docs, or tools

RESUME DATA:
{resume}

JOB DESCRIPTION:
{jd}

MISSING SKILLS:
{missing}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # slight creativity for better suggestions
        )

        raw = response.choices[0].message.content

        try:
            cleaned = re.search(r"\{.*\}", raw, re.DOTALL)
            result = json.loads(cleaned.group())
        except:
            result = {"recommendations": []}

        state["recommendations"] = result.get("recommendations", [])

        return state