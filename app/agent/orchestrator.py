from app.agent.planner import Planner


class AgentOrchestrator:
    def __init__(self, skills, mcp_server):
        self.skills = skills
        self.mcp_server = mcp_server
        self.planner = Planner()

    def handle_request(self, user_prompt: str):
        intent = self.planner.detect_intent(user_prompt)
        skill = self.planner.choose_skill(intent, self.skills)

        context = {
            "user_prompt": user_prompt,
            "intent": intent,
        }

        result = skill.execute(context, self.mcp_server)
        return {
            "intent": intent,
            "result": result,
        }
