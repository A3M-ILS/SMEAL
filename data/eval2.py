import pandas as pd
import numpy as np
import joblib
import json
from sklearn.metrics import r2_score

# ===== Load model and scaler =====
model = joblib.load("models/nutrition_predictor.pkl")
scaler = joblib.load("models/scaler.pkl")

# ===== Load density DB =====
with open("data/density_db.json", "r") as f:
    density_db = json.load(f)

# ===== Load test CSV =====
df = pd.read_csv("data/quantity_test.csv")

preds = []

for _, row in df.iterrows():
    food = row["class"]
    true_qty = row["true_qty"]

    bbox_area = row["bbox_area"]
    image_area = row["image_area"]
    ratio = bbox_area / image_area

    density = density_db.get(food.lower(), 1.0)

    # === Features vector ===
    X = np.array([[bbox_area, image_area, ratio, density]])

    # === Scaling ===
    X_scaled = scaler.transform(X)

    # === Prediction ===
    pred_qty = model.predict(X_scaled)[0]
    preds.append(pred_qty)

df["pred_qty"] = preds

# ===== Regression Metrics =====
errors = df["pred_qty"] - df["true_qty"]
abs_errors = abs(errors)

MAE  = np.mean(abs_errors)
RMSE = np.sqrt(np.mean(errors**2))
MAPE = np.mean(abs_errors / df["true_qty"]) * 100
R2   = r2_score(df["true_qty"], df["pred_qty"])
Bias = np.mean(errors)

print("\n=== Regression Metrics ===")
print(f"MAE  : {MAE:.2f} g")
print(f"RMSE : {RMSE:.2f} g")
print(f"MAPE : {MAPE:.2f} %")
print(f"R²   : {R2:.3f}")
print(f"Bias : {Bias:.2f} g")

# ===== MAE per class =====
print("\n=== MAE per class ===")
print(df.groupby("class").apply(lambda x: abs(x["pred_qty"] - x["true_qty"]).mean()))

# ===== Save predictions =====
df.to_csv("data/quantity_predictions.csv", index=False)
print("\nPredictions saved to data/quantity_predictions.csv")
