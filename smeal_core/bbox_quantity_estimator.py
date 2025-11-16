import json
import pickle
import numpy as np

class QuantityEstimator:
    def __init__(self):
        self.model = pickle.load(open("models/nutrition_predictor.pkl", "rb"))
        self.scaler = pickle.load(open("models/scaler.pkl", "rb"))
        self.density_db = json.load(open("data/density_db.json", "r"))

    def estimate(self, ingredient, bbox_area, image_area):
        density = self.density_db.get(ingredient.lower(), 1.0)

        X = np.array([[bbox_area, image_area, density]])
        X_scaled = self.scaler.transform(X)
        
        CORRECTION_FACTOR = 6.0  # start with 5–7, adjust later

        # base prediction
        w = self.model.predict(X_scaled)[0]

        # adaptive correction factor
        ratio = bbox_area / image_area   # how big the food is in the image
        if ratio < 0.01:
            factor = 7
        elif ratio < 0.03:
            factor = 5
        elif ratio < 0.08:
            factor = 3
        else:
            factor = 1.5  # prevent huge weights

        w = w * factor
        return float(w)

