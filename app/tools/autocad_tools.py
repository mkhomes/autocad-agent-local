import os
from typing import Dict, List

from win32com.client import Dispatch

from app.config import AUTO_CAD_VISIBLE


class AutoCADTools:
    def __init__(self):
        self.acad = None
        self.doc = None
        self.modelspace = None

    def connect(self):
        if self.acad is None:
            try:
                self.acad = Dispatch("AutoCAD.Application")
            except Exception:
                try:
                    self.acad = Dispatch("AutoCAD.Application.24")
                except Exception as exc:
                    raise RuntimeError(
                        "Không thể kết nối AutoCAD. Hãy chắc chắn AutoCAD đã cài trên Windows và đang chạy."
                    ) from exc

            self.acad.Visible = AUTO_CAD_VISIBLE

        return self.acad

    def new_document(self):
        acad = self.connect()
        self.doc = acad.Documents.Add()
        self.modelspace = self.doc.ModelSpace
        return self.doc

    def set_layer(self, layer_name: str, color_index: int = 7):
        if self.doc is None:
            raise RuntimeError("AutoCAD document chưa được khởi tạo. Gọi new_document trước.")
        try:
            layer = self.doc.Layers.Item(layer_name)
        except Exception:
            layer = self.doc.Layers.Add(layer_name)
        layer.Color = color_index
        self.doc.ActiveLayer = layer
        return layer

    def add_line(self, x1: float, y1: float, x2: float, y2: float, layer: str = "A-WALL"):
        self.set_layer(layer)
        return self.modelspace.AddLine((x1, y1, 0), (x2, y2, 0))

    def add_text(self, text: str, x: float, y: float, height: float = 0.3, layer: str = "A-TEXT"):
        self.set_layer(layer)
        return self.modelspace.AddText(text, (x, y, 0), height)

    def add_circle(self, x: float, y: float, radius: float, layer: str = "A-DOOR"):
        self.set_layer(layer)
        return self.modelspace.AddCircle((x, y, 0), radius)

    def insert_block(self, block_name: str, x: float, y: float, rotation: float = 0, scale: float = 1.0):
        self.set_layer("A-DOOR")
        p1 = (x, y, 0)
        p2 = (x + 0.8 * scale, y + 0.6 * scale, 0)
        rect = self.modelspace.AddRectangle(p1, p2)
        return {"block_name": block_name, "x": x, "y": y, "rotation": rotation, "scale": scale, "entity": rect}

    def list_layers(self) -> List[str]:
        self.connect()
        if self.doc is None:
            self.new_document()
        layers = []
        for i in range(0, self.doc.Layers.Count):
            layers.append(self.doc.Layers.Item(i).Name)
        return layers

    def save_dwg(self, file_path: str):
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        if self.doc is None:
            self.new_document()
        self.doc.SaveAs(file_path)

    def export_pdf(self, dwg_path: str, pdf_path: str):
        if self.doc is None:
            self.new_document()
        self.doc.Export(pdf_path, "PDF")
        return pdf_path

    def draw_room(self, room: Dict[str, float], wall_thickness: float = 0.15):
        x = room["x"]
        y = room["y"]
        width = room["width"]
        depth = room["depth"]

        self.add_line(x, y, x + width, y, "A-WALL")
        self.add_line(x + width, y, x + width, y + depth, "A-WALL")
        self.add_line(x + width, y + depth, x, y + depth, "A-WALL")
        self.add_line(x, y + depth, x, y, "A-WALL")

        self.add_text(room["name"], x + 0.25, y + 0.25, height=0.25, layer="A-TEXT")

    def draw_floorplan(self, plan: Dict[str, object]):
        self.new_document()
        self.set_layer("A-WALL", 1)
        self.set_layer("A-TEXT", 3)
        self.set_layer("A-DIM", 2)

        for room in plan.get("rooms", []):
            self.draw_room(room, plan.get("walls_thickness", 0.15))

        overall_width = float(plan.get("overall_width", 0))
        overall_depth = float(plan.get("overall_depth", 0))
        self.add_line(0, 0, overall_width, 0, "A-WALL")
        self.add_line(overall_width, 0, overall_width, overall_depth, "A-WALL")
        self.add_line(overall_width, overall_depth, 0, overall_depth, "A-WALL")
        self.add_line(0, overall_depth, 0, 0, "A-WALL")

        self.add_text(plan.get("project_name", "Project"), 0.5, overall_depth + 0.5, 0.4, "A-TEXT")
