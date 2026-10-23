from app.skills.skill_base import SkillBase


class LayerCheckSkill(SkillBase):
    name = "layer_standard_check"

    def can_handle(self, intent: str) -> bool:
        i = intent.lower()
        return "layer" in i or "standard" in i or "check" in i

    def execute(self, context: dict, mcp_server, **kwargs) -> dict:
        layers = mcp_server.call_tool("autocad.list_layers")
        required_layers = ["0", "A-WALL", "A-TEXT", "A-DIM", "A-DOOR"]
        missing = [layer for layer in required_layers if layer not in layers]

        return {
            "status": "success" if not missing else "warning",
            "skill": self.name,
            "layers": layers,
            "missing": missing,
        }
