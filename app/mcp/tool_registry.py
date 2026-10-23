from typing import Any, Callable, Dict


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]):
        self.tools[name] = func

    def get(self, name: str):
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' not found")
        return self.tools[name]

    def call(self, name: str, **kwargs):
        func = self.get(name)
        return func(**kwargs)
