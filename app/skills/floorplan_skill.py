import os

from app.config import PROJECTS_DIR
from app.skills.skill_base import SkillBase


class FloorPlanSkill(SkillBase):
    name = "floor_plan_generation"

    def can_handle(self, intent: str) -> bool:
        i = intent.lower()
        return "floor" in i or "plan" in i or "layout" in i or "room" in i

    def execute(self, context: dict, mcp_server, **kwargs) -> dict:
        user_prompt = context["user_prompt"]
        plan = mcp_server.call_tool("ollama.generate_floorplan_plan", user_prompt=user_prompt)

        project_name = plan.get("project_name", "FloorPlan")
        safe_name = "".join(ch for ch in project_name if ch.isalnum() or ch in ("-", "_")).strip() or "FloorPlan"

        os.makedirs(PROJECTS_DIR, exist_ok=True)
        dwg_path = os.path.join(PROJECTS_DIR, f"{safe_name}.dwg")
        pdf_path = os.path.join(PROJECTS_DIR, f"{safe_name}.pdf")

        mcp_server.call_tool("autocad.draw_floorplan", plan=plan)
        mcp_server.call_tool("autocad.save_dwg", file_path=dwg_path)

        try:
            mcp_server.call_tool("autocad.export_pdf", dwg_path=dwg_path, pdf_path=pdf_path)
        except Exception:
            pass

        return {
            "status": "success",
            "skill": self.name,
            "project_name": project_name,
            "dwg_path": dwg_path,
            "pdf_path": pdf_path,
            "plan": plan,
        }
