import re
from typing import Dict, Any, List


class NormalizationNode:

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        resume = state.get("resume_json", {})
        jd = state.get("jd_json", {})

        # Resume
        resume["skills"] = self.normalize_skills(resume.get("skills", []))
        resume["projects"] = self.normalize_projects(resume.get("projects", []))
        resume["education"] = self.normalize_list(resume.get("education", []))
        resume["experience"] = self.normalize_list(resume.get("experience", []))
        resume["certifications"] = self.normalize_list(resume.get("certifications", []))

        # JD
        jd["skills_required"] = self.normalize_skills(jd.get("skills_required", []))
        jd["tools_technologies"] = self.normalize_skills(jd.get("tools_technologies", []))
        jd["responsibilities"] = self.normalize_list(jd.get("responsibilities", []))

        state["resume_json"] = resume
        state["jd_json"] = jd

        return state

    # -------------------------------
    # SKILLS (NO MAPPING)
    # -------------------------------
    def normalize_skills(self, skills: List[str]) -> List[str]:
        cleaned = set()

        for skill in skills:
            if not skill:
                continue

            s = skill.lower().strip()

            # remove unwanted characters
            s = re.sub(r"[^a-z0-9\s\.\+#]", "", s)

            # normalize spacing
            s = re.sub(r"\s+", " ", s)

            # title case
            s = self.smart_title_case(s)

            cleaned.add(s)

        return sorted(list(cleaned))

    # -------------------------------
    # PROJECTS
    # -------------------------------
    def normalize_projects(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []

        for proj in projects:
            if not isinstance(proj, dict):
                continue

            normalized.append({
                "name": self.clean_text(proj.get("name", "")),
                "description": self.clean_text(proj.get("description", "")),
                "tech_stack": self.normalize_skills(proj.get("tech_stack", [])),
                "metrics": self.clean_text(proj.get("metrics", ""))
            })

        return normalized

    # -------------------------------
    # GENERIC LIST CLEANER
    # -------------------------------
    def normalize_list(self, items: List[str]) -> List[str]:
        cleaned = set()

        for item in items:
            if item and item.strip():
                cleaned.add(self.clean_text(item))

        return sorted(list(cleaned))

    # -------------------------------
    # TEXT CLEANING
    # -------------------------------
    def clean_text(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text

    # -------------------------------
    # SMART TITLE CASE
    # -------------------------------
    def smart_title_case(self, text: str) -> str:
        words = re.split(r"[\s\-_/]+", text)
        return " ".join(word.capitalize() for word in words if word)