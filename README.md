# AutoCAD Local AI Agent

This project is a local prototype for an architecture-focused AutoCAD agent powered by:
- FastAPI
- Ollama (local LLM)
- AutoCAD automation on Windows
- MCP-style tool registry + agent orchestration pattern

It demonstrates an agent that can:
- generate a floor plan from a natural language prompt
- call AutoCAD tools to draw rooms
- save DWG output
- export PDF
- validate layers

Important:
- AutoCAD automation works only on Windows.
- This is a local prototype, not a production-grade CAD engine.
