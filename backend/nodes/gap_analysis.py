from typing import Dict, Any


class GapAnalysisNode:

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        missing = state.get("missing", [])

        state["gaps"] = missing

        return state