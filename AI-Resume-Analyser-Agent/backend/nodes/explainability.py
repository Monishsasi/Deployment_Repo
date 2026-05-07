import os
from groq import Groq
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class ExplainabilityNode:

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:

        score = state.get("score", 0)
        matched = state.get("matched", [])
        missing = state.get("missing", [])
        recommendations = state.get("recommendations", [])
        jd = state.get("jd_json", {})
        resume = state.get("resume_json", {})

        prompt = f"""
You are an ATS + career advisor.

Give a SHORT, CRISP, HIGH-IMPACT analysis.

RULES:
- Max 10–12 lines total
- No JSON, no markdown
- No long explanations
- Be direct and insightful

FORMAT:

1. MATCH SCORE INTERPRETATION
Score: {score}
→ 1 line meaning (Strong/Moderate/Weak fit)

2. KEY STRENGTHS
- {matched}
→ 1–2 lines why these help job fit

3. KEY GAPS
- {missing}
→ 1–2 lines impact on hiring

4. FIT SUMMARY
→ 1–2 lines overall alignment with JD

5. NEXT STEPS
- {recommendations}
→ 1–2 lines actionable improvement

RESUME: {resume}
JD: {jd}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Be extremely concise and ATS-focused."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        state["explanation"] = response.choices[0].message.content
        return state