from typing import Dict, Any


class ScoringNode:

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        matched = state.get("matched", [])
        missing = state.get("missing", [])

        total = len(matched) + len(missing)

        if total == 0:
            score = 0
        else:
            score = int((len(matched) / total) * 100)

        state["score"] = score

        return state