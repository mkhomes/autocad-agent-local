from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent.orchestrator import AgentOrchestrator
from app.config import APP_NAME, HOST, PORT
from app.mcp.server import MCPServer
from app.skills.floorplan_skill import FloorPlanSkill
from app.skills.layer_check_skill import LayerCheckSkill
from app.tools.autocad_tools import AutoCADTools
from app.tools.ollama_tools import OllamaTools

app = FastAPI(title=APP_NAME)

mcp_server = MCPServer()
autocad_tools = AutoCADTools()
ollama_tools = OllamaTools()

mcp_server.register_tool("autocad.list_layers", autocad_tools.list_layers)
mcp_server.register_tool("autocad.new_document", autocad_tools.new_document)
mcp_server.register_tool("autocad.draw_floorplan", autocad_tools.draw_floorplan)
mcp_server.register_tool("autocad.save_dwg", autocad_tools.save_dwg)
mcp_server.register_tool("autocad.export_pdf", autocad_tools.export_pdf)
mcp_server.register_tool("autocad.add_line", autocad_tools.add_line)
mcp_server.register_tool("autocad.insert_block", autocad_tools.insert_block)

mcp_server.register_tool("ollama.generate_floorplan_plan", ollama_tools.generate_floorplan_plan)

skills = [
    FloorPlanSkill(),
    LayerCheckSkill(),
]

agent = AgentOrchestrator(skills=skills, mcp_server=mcp_server)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": APP_NAME,
        "ollama_available": ollama_tools.is_available(),
    }


@app.post("/api/agent/run")
def run_agent(request: PromptRequest):
    try:
        if not ollama_tools.is_available():
            raise RuntimeError("Ollama chưa chạy ở http://localhost:11434. Hãy chạy `ollama serve` trước.")
        response = agent.handle_request(request.prompt)
        return {
            "status": "success",
            "data": response,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
