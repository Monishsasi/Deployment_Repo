import re
from typing import Dict, Any


class ValidationNode:
    def __call__(self, state: Dict[str, Any]):
        return self.run(state)

    def run(self, state: Dict[str, Any]):
        resume = state.get("resume_json", {})
        jd = state.get("jd_json", {})

        # ✅ update state instead of replacing
        state["resume_json"] = self.validate_resume(resume)
        state["jd_json"] = self.validate_jd(jd)

        return state

    # ---------------- RESUME VALIDATION ---------------- #

    def validate_resume(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": self.clean_string(data.get("name")),
            "email": self.validate_email(data.get("email")),
            "phone": self.validate_phone(data.get("phone")),
            "skills": self.clean_list(data.get("skills")),
            "education": self.clean_list(data.get("education")),
            "projects": self.validate_projects(data.get("projects")),
            "experience": self.clean_list(data.get("experience")),
            "certifications": self.clean_list(data.get("certifications")),
        }

    # ---------------- JD VALIDATION ---------------- #

    def validate_jd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": self.clean_string(data.get("title")),
            "skills_required": self.clean_list(data.get("skills_required")),
            "responsibilities": self.clean_list(data.get("responsibilities")),
            "experience_required": self.clean_string(data.get("experience_required")),
            "tools_technologies": self.clean_list(data.get("tools_technologies")),
            "education": self.clean_string(data.get("education")),
        }

    # ---------------- HELPERS ---------------- #

    def clean_string(self, value):
        if not value or not isinstance(value, str):
            return ""
        return value.strip()

    def clean_list(self, value):
        if not value or not isinstance(value, list):
            return []

        seen = set()
        cleaned = []

        for item in value:
            if isinstance(item, str):
                item = item.strip()
                if item and item not in seen:
                    seen.add(item)
                    cleaned.append(item)

        return cleaned  # ✅ preserves order

    def validate_email(self, email):
        if not email or not isinstance(email, str):
            return ""

        email = email.strip()

        # improved regex
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return email if re.match(pattern, email) else ""

    def validate_phone(self, phone):
        if not phone or not isinstance(phone, str):
            return ""

        # remove spaces, dashes, etc.
        phone = re.sub(r"[^\d+]", "", phone.strip())

        pattern = r"^\+?\d{10,15}$"
        return phone if re.match(pattern, phone) else ""

    def validate_projects(self, projects):
        if not projects or not isinstance(projects, list):
            return []

        cleaned_projects = []

        for proj in projects:
            if not isinstance(proj, dict):
                continue

            cleaned_projects.append({
                "name": self.clean_string(proj.get("name")),
                "description": self.clean_string(proj.get("description")),
                "tech_stack": self.clean_list(proj.get("tech_stack")),
                "metrics": self.clean_string(proj.get("metrics")),
            })

        return cleaned_projects