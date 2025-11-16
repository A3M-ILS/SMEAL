from ultralytics import YOLO
from PIL import Image

class IngredientDetector:
    def __init__(self, model_path="models/yolo_food.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path):
        results = self.model(image_path)[0]

        detections = []
        img = Image.open(image_path)
        img_area = img.size[0] * img.size[1]

        for box in results.boxes:
            name = self.model.names[int(box.cls)]
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            area = (x2 - x1) * (y2 - y1)

            detections.append({
                "ingredient": name,
                "bbox": [x1, y1, x2, y2],
                "bbox_area": area,
                "image_area": img_area
            })

        return detections
