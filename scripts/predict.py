import sys
import argparse
from smeal_core.detection import IngredientDetector
from smeal_core.bbox_quantity_estimator import QuantityEstimator
from smeal_core.nutrition import NutritionAnalyzer
from smeal_core.rules_engine import evaluate_rules
from smeal_core.recommender import build_recommendation


def run_prediction(image_paths):
    detector = IngredientDetector()
    estimator = QuantityEstimator()
    nutritioner = NutritionAnalyzer()

    # Combiner les quantités sur toutes les images
    total_quantities = {}

    for img_path in image_paths:
        print(f"\n🔍 Processing image: {img_path}")

        detections = detector.detect(img_path)

        for d in detections:
            ing = d["ingredient"]  # YOLO class name directly

            qty = estimator.estimate(
                ing,
                d["bbox_area"],
                d["image_area"]
            )

            if ing not in total_quantities:
                total_quantities[ing] = 0

            total_quantities[ing] += qty

    # Nutrition totale
    nutrition = nutritioner.compute(total_quantities)

    # Règles alimentaires
    problems = evaluate_rules(list(total_quantities.keys()), nutrition)
    recommendation = build_recommendation(problems)

    print("\n=== Final Combined Results ===")
    print("Ingredients:", total_quantities)
    print("Nutrition:", nutrition)
    print("Issues:", problems)
    print("Recommendation:", recommendation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", nargs="+", required=True, help="List of images")
    args = parser.parse_args()

    run_prediction(args.images)
