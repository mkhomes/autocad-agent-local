import json
import requests

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaTools:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def is_available(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def generate_json(self, prompt: str) -> dict:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()

        data = resp.json()
        content = data.get("response", "")
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_response": content}

    def generate_floorplan_plan(self, user_prompt: str) -> dict:
        system_prompt = """
Bạn là chuyên gia kiến trúc và AutoCAD.
Trả về một JSON hợp lệ với schema sau:

{
  "project_name": "string",
  "unit": "m",
  "overall_width": 10.0,
  "overall_depth": 8.0,
  "walls_thickness": 0.15,
  "rooms": [
    {
      "name": "Living Room",
      "x": 0.0,
      "y": 0.0,
      "width": 4.0,
      "depth": 5.0
    }
  ]
}

Yêu cầu:
- x, y là tọa độ góc trái dưới của phòng
- walls_thickness là bề dày tường
- không viết text nào ngoài JSON
"""

        return self.generate_json(f"{system_prompt}\n\nYêu cầu người dùng: {user_prompt}")
