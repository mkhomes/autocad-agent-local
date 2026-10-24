# AutoCAD Local AI Agent

A local prototype that combines:
- FastAPI
- Ollama (local LLM)
- AutoCAD automation on Windows
- MCP-style tool registry and agent orchestration

This project demonstrates an agent that can understand a design request, call specialized skills, invoke drawing tools, generate a floor plan, save the result to DWG, and export a PDF.

Important notes:
- AutoCAD automation only works on Windows.
- This is a prototype for local experimentation and internal workflows.
- Ollama must be running locally on your machine.
- The project is designed to work with AutoCAD 2022–2026 on Windows, provided the environment is configured correctly.

## Features
- Floor plan generation from natural language prompts
- Local Ollama-based LLM plan generation
- AutoCAD drawing operations via pywin32 / COM
- Tool registry and MCP-like architecture
- Skill-based agent orchestration
- Validation and quality checks before export
- API endpoint for agent execution
- DWG/PDF generated outputs

## Workflow

1. Input stage
   - DWG / DXF
   - PDF
   - JPG / PNG
   - CAD template files

2. Skill 00 – AutoCAD reading
   - AI reads and interprets the source drawing
   - Identifies key structures such as grids, walls, doors, columns, layers, and blocks
   - Detects missing or uncertain information and asks for clarification when needed

3. Project Data Store
   - Stores structured drawing metadata in a central project repository
   - Keeps common design data for downstream skills and validation

4. 10 CAD Skills
   - Grid / axis creation
   - Column creation
   - Wall generation
   - Door insertion
   - Connection / join logic
   - Hatch generation
   - Dimensioning
   - Finish / refinement
   - Validation
   - Export

5. CAD Validator
   - Checks for geometric issues
   - Detects conflicts and structural inconsistencies
   - Validates dimensions and rule compliance

6. AutoCAD integration
   - Interacts with AutoCAD through COM / pywin32 APIs
   - Executes drawing commands and updates the document

7. Output
   - DWG
   - Finalized DWG
   - PDF
   - Validation reports / structured project data

## Design philosophy
The core principle is:

Read once → store common data → draw by skill → validate continuously

This approach keeps the system modular and easier to manage than a single large end-to-end drawing agent.

## Requirements
- Windows 10/11
- Python 3.10+
- AutoCAD installed on the machine
- Ollama installed and running locally
- Matching Python and AutoCAD bitness (recommended: both 64-bit)

## AutoCAD 2022–2026 compatibility notes
This project is designed to be compatible with AutoCAD 2022 through 2026 on Windows, assuming the environment is correctly configured.

Important compatibility points:
- AutoCAD automation requires Windows.
- Python and AutoCAD must use the same architecture (for example, both 64-bit).
- COM/pywin32 must be installed and working correctly.
- AutoCAD trust/security settings may block some automation tasks depending on version and environment.
- Version-specific differences can affect export behavior, plotting, and layer handling, so validation is important.

## Project structure

```text
autocad-agent-local/
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ main.py
│  ├─ agent/
│  │  ├─ orchestrator.py
│  │  └─ planner.py
│  ├─ mcp/
│  │  ├─ server.py
│  │  └─ tool_registry.py
│  ├─ skills/
│  │  ├─ floorplan_skill.py
│  │  ├─ layer_check_skill.py
│  │  └─ skill_base.py
│  └─ tools/
│     ├─ autocad_tools.py
│     └─ ollama_tools.py
├─ .env.example
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ projects/
└─ ...
```

## Install

1. Clone the repository

```bash
git clone https://github.com/mkhomes/autocad-agent-local.git
cd autocad-agent-local
```

2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Install Ollama

Download and install Ollama from:
- https://ollama.com

Then start the model server:

```bash
ollama serve
ollama pull qwen2.5-coder:7b
```

You can replace the model with another supported one if desired.

## Configure environment

Copy the example file:

```bash
copy .env.example .env
```

Then update the values if needed.

Default values:

```env
APP_NAME=autocad-agent
HOST=0.0.0.0
PORT=8000
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b
PROJECTS_DIR=./projects
AUTO_CAD_VISIBLE=true
```

## Run the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API test

POST to:

```text
http://localhost:8000/api/agent/run
```

Example request:

```bash
curl -X POST "http://localhost:8000/api/agent/run" ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Tạo mặt bằng nhà 1 tầng 10x8m với phòng khách, 2 phòng ngủ, bếp, WC.\"}"
```

Example response:

```json
{
  "status": "success",
  "data": {
    "intent": "floor_plan",
    "result": {
      "status": "success",
      "skill": "floor_plan_generation",
      "project_name": "HousePlan1",
      "dwg_path": "C:\\project\\autocad-agent-local\\projects\\HousePlan1.dwg",
      "pdf_path": "C:\\project\\autocad-agent-local\\projects\\HousePlan1.pdf"
    }
  }
}
```

## Known limitations
- AutoCAD automation only works in Windows environments.
- This is a prototype, not a full CAD authoring platform.
- Layer naming and blocks should be customized for your own company standards.
- PDF export depends on AutoCAD document behavior and may need adjustments.
- Different AutoCAD versions may require small environment-specific tuning.

## Test request
Please test the app locally and report:
- whether the API starts successfully
- whether Ollama is reachable
- whether AutoCAD connects properly
- whether floor-plan generation saves DWG/PDF
- any errors in the tool registry or AutoCAD integration

Please share the output of:
- uvicorn startup logs
- curl response body
- AutoCAD COM errors

## Next improvements
- add more skills: 3D model generation, dimension validation, block library insertion
- add SQLite/PostgreSQL project history
- add React frontend for local UI
- add human approval before saving final drawings
- improve compatibility testing across AutoCAD 2022–2026 versions

## License
This project is provided as a prototype for local experimentation and development.
