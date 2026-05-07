from typing import Dict, Any


class OutputNode:

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "summary": self.build_summary(state),
            "score": {
                "overall": state.get("score", 0),
                "interpretation": self.score_interpretation(state.get("score", 0))
            },
            "skills_analysis": {
                "matched_skills": state.get("matched", []),
                "missing_skills": state.get("missing", []),
                "match_percentage": self.calculate_match_percentage(state)
            },
            "recommendations": state.get("recommendations", []),
            "gap_analysis": state.get("gap_analysis", {}),
            "detailed_explanation": state.get("explanation", ""),
            "meta": {
                "resume_parsed": bool(state.get("resume_json")),
                "jd_parsed": bool(state.get("jd_json"))
            }
        }

    # ---------------- SUMMARY ---------------- #

    def build_summary(self, state: Dict[str, Any]) -> str:
        score = state.get("score", 0)
        matched = len(state.get("matched", []))
        missing = len(state.get("missing", []))

        return (
            f"The candidate matches {matched} key requirements but is missing {missing}. "
            f"Overall alignment score is {score}%. "
            f"See recommendations to improve alignment."
        )

    # ---------------- SCORE INTERPRETATION ---------------- #

    def score_interpretation(self, score: int) -> str:
        if score >= 80:
            return "Strong match — highly suitable for the role."
        elif score >= 60:
            return "Moderate match — can be improved with targeted enhancements."
        elif score >= 40:
            return "Weak match — significant gaps need to be addressed."
        else:
            return "Low match — major skill and experience gaps."

    # ---------------- MATCH % ---------------- #

    def calculate_match_percentage(self, state: Dict[str, Any]) -> float:
        matched = len(state.get("matched", []))
        total = matched + len(state.get("missing", []))

        if total == 0:
            return 0.0

        return round((matched / total) * 100, 2)