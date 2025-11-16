import pandas as pd
import numpy as np
import joblib
import json

# ---- Load model and scaler ----
model = joblib.load("models/nutrition_predictor.pkl")
scaler = joblib.load("models/scaler.pkl")

# ---- Load density DB ----
with open("data/density_db.json", "r") as f:
    density_db = json.load(f)

# ---- Load test file ----
df = pd.read_csv("quantity_test.csv")

preds = []

for _, row in df.iterrows():
    food = row["class"]
    true_qty = row["true_qty"]
    
    bbox_area = row["bbox_area"]
    image_area = row["image_area"]
    ratio = bbox_area / image_area
    
    density = density_db.get(food.lower(), 1.0)

    # Build feature vector
    X = np.array([[bbox_area, image_area, ratio, density]])

    # Scale features
    X_scaled = scaler.transform(X)

    # Predict
    pred_qty = model.predict(X_scaled)[0]
    preds.append(pred_qty)

df["pred_qty"] = preds
df.to_csv("quantity_predictions.csv", index=False)

print(df.head())
