class Planner:
    def detect_intent(self, prompt: str) -> str:
        p = prompt.lower()

        if any(word in p for word in ["mặt bằng", "layout", "floor plan", "plan", "phòng"]):
            return "floor_plan"
        if any(word in p for word in ["layer", "standard", "check", "kiểm tra"]):
            return "layer_check"
        if any(word in p for word in ["3d", "mô hình", "3d model"]):
            return "3d_model"
        return "general"

    def choose_skill(self, intent: str, skill_list):
        for skill in skill_list:
            if skill.can_handle(intent):
                return skill
        raise ValueError(f"No skill matched intent: {intent}")
