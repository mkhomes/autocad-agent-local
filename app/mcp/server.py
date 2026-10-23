from app.mcp.tool_registry import ToolRegistry


class MCPServer:
    def __init__(self):
        self.registry = ToolRegistry()

    def register_tool(self, name: str, func):
        self.registry.register(name, func)

    def call_tool(self, name: str, **kwargs):
        return self.registry.call(name, **kwargs)
