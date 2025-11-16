from ultralytics import YOLO

model = YOLO("models/yolo_food.pt")

print("\n=== Classes YOLO détectées ===\n")
for idx, name in model.names.items():
    print(f"{idx}: {name}")
