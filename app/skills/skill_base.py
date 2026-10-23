from abc import ABC, abstractmethod


class SkillBase(ABC):
    name: str = "base_skill"

    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        pass

    @abstractmethod
    def execute(self, context: dict, mcp_server, **kwargs) -> dict:
        pass
