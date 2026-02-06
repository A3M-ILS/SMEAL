# 🍽️ SMEAL — Smart Meal Analyzer  
A complete Machine Learning system that analyzes meal photos and provides nutritional insights.

SMEAL is an end-to-end ML application that can:  
- 🥗 Detect food items in one or multiple photos  
- ⚖️ Estimate the quantity (in grams) of each food item  
- 🔬 Compute total nutritional values (proteins, carbs, sugars, fats)  
- ⚠️ Evaluate unhealthy food combinations (14 nutrition rules)  
- ⭐ Assign a health score  
- 💡 Provide personalized recommendations  
- 🌐 Offer a full interactive web interface with Gradio

This project demonstrates a real-world ML pipeline:  
**data collection → preprocessing → model training → evaluation → deployment**.

---

# 📌 1. Requirements

## ✔️ Recommended Python Version
SMEAL has been tested with:


❗ **Python 3.12 is not recommended** (some ML libraries are not fully compatible).

---

# 📌 2. Clone the Repository
git clone https://github.com/A3M-ILS/Smeal.git

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

Main libraries:

ultralytics (YOLOv8)

opencv-python

pillow

numpy

pandas

scikit-learn

joblib

plotly

gradio

matplotlib

Project Structure
Smeal/
│
├── app.py                        # Gradio web interface
├── requirements.txt
│
├── smeal_core/
│   ├── detection.py              # YOLO inference pipeline
│   ├── bbox_quantity_estimator.py# RandomForest regression model
│   ├── nutrition.py              # Nutritional calculations
│   ├── recommender.py            # Health score + recommendations
│   ├── rules_engine.py           # 14 food combination rules
│   └── class_mapping.py
│
├── models/
│   ├── yolo_food.pt              # Food detection model
│   ├── nutrition_predictor.pkl   # RandomForestRegressor
│   └── scaler.pkl                # StandardScaler
│
├── data/
│   ├── nutrition_db.json
│   ├── density_db.json
│   └── quantity_test.csv
│
└── scripts/
    ├── predict.py
    ├── train_quantity_model.py
    ├── evaluate

# 📌 3. Start the interface:

python app.py
