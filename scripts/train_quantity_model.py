import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/quantity_training_dataset.csv")

X = df[["bbox_area", "image_area", "density"]].values
y = df["weight"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestRegressor(n_estimators=200)
model.fit(X_scaled, y)

pickle.dump(model, open("models/nutrition_predictor.pkl", "wb"))
pickle.dump(scaler, open("models/scaler.pkl", "wb"))

print("✔ nutrition_predictor.pkl and scaler.pkl generated!")
