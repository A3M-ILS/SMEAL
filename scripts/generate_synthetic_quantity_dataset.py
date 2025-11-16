import pandas as pd
import numpy as np
import json
import random

density_db = json.load(open("data/density_db.json"))

def random_ingredient():
    return random.choice(list(density_db.keys()))

rows = []

for _ in range(300):  # generate 300 samples
    ingredient = random_ingredient()
    density = density_db[ingredient]

    image_area = random.randint(600000, 1400000)
    bbox_area = random.randint(8000, int(image_area * 0.12))

    # synthetic physics-inspired formula:
    # weight = bbox_area * density * scaling factor
    weight = (bbox_area / 10000) * density * random.uniform(8, 14)

    rows.append([bbox_area, image_area, density, round(weight)])

df = pd.DataFrame(rows, columns=["bbox_area", "image_area", "density", "weight"])
df.to_csv("data/quantity_training_dataset.csv", index=False)

print("✔ Synthetic dataset generated!")
