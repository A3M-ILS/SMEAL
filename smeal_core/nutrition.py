import json

class NutritionAnalyzer:
    def __init__(self, db_path="data/nutrition_db.json"):
        self.db = json.load(open(db_path, "r", encoding="utf-8"))

    def compute(self, quantities):
        total = {"proteines": 0, "glucides": 0, "sucres": 0, "graisses": 0}

        for ing, grams in quantities.items():
            if ing not in self.db:
                continue
            
            nut = self.db[ing]

            for k in total:
                total[k] += nut[k] * (grams / 100)

        return total
