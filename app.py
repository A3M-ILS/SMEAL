import gradio as gr
import os
from PIL import Image
from ultralytics import YOLO
import plotly.graph_objects as go

from smeal_core.detection import IngredientDetector
from smeal_core.bbox_quantity_estimator import QuantityEstimator
from smeal_core.nutrition import NutritionAnalyzer
from smeal_core.rules_engine import evaluate_rules
from smeal_core.recommender import build_recommendation

detector = IngredientDetector()
estimator = QuantityEstimator()
nutritioner = NutritionAnalyzer()
YOLO_MODEL = YOLO("models/yolo_food.pt")

os.makedirs("static", exist_ok=True)


def draw_boxes(image_path):
    results = YOLO_MODEL(image_path)[0]
    out_path = f"static/out_{os.path.basename(image_path)}"
    results.save(filename=out_path)
    return out_path


def compute_score(n, detected_foods):
    proteines = n["proteines"]
    glucides = n["glucides"]
    sucres = n["sucres"]
    graisses = n["graisses"]

    score = 0

    # 1. Protein Score (0–25)
    if proteines < 20:
        score += 10
    elif proteines < 40:
        score += 18
    else:
        score += 25   # high protein, great for balanced meal

    # 2. Carb Quality (0–20)
    if "Rice" in detected_foods:
        score += 15
    if "Fries" in detected_foods or "Pizza" in detected_foods:
        score -= 10

    # 3. Sugar Quality (0–20)
    if "Soda" in detected_foods:
        score -= 20
    elif sucres < 10:
        score += 15
    else:
        score += 5

    # 4. Fat Score (0–15)
    if graisses < 10:
        score += 15
    elif graisses < 20:
        score += 10   # <-- FIXED, this is NORMAL fat
    else:
        score -= 10

    # 5. Whole Foods (0–10)
    if "Tomato" in detected_foods or "Apple" in detected_foods or "banana" in detected_foods:
        score += 10

    # 6. Rules Engine (0–10)
    problems = evaluate_rules(detected_foods, n)
    if len(problems) == 0:
        score += 10
    elif len(problems) == 1:
        score += 5

    # Clip 0–100
    return max(0, min(100, score))


def score_bar(score):
    pct = int(score)
    filled = int(pct // 5)
    empty = 20 - filled
    bar = "█" * filled + "░" * empty
    return f"**[{bar}]  {pct}/100**"


def score_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 40], "color": "red"},
                {"range": [40, 65], "color": "orange"},
                {"range": [65, 100], "color": "green"}
            ],
        },
        number={"suffix": " / 100"},
        title={"text": "Nutrition Score", "font": {"size": 24}},
        domain={"x": [0, 1], "y": [0, 1]}
    ))
    return fig


def analyze_meal(files):
    if not files:
        return [], "No images uploaded.", None

    total_quantities = {}
    boxed_images = []

    for idx, file in enumerate(files):
        img = Image.open(file)
        img_path = f"temp_meal_{idx}.jpg"
        img.save(img_path)

        boxed_path = draw_boxes(img_path)
        boxed_images.append(boxed_path)

        detections = detector.detect(img_path)
        for d in detections:
            ing = d["ingredient"]
            qty = estimator.estimate(ing, d["bbox_area"], d["image_area"])
            total_quantities[ing] = total_quantities.get(ing, 0) + qty

    detected_foods = list(total_quantities.keys())

    nutrition = nutritioner.compute(total_quantities)
    problems = evaluate_rules(detected_foods, nutrition)
    recommendation = build_recommendation(problems)

    score = compute_score(nutrition, detected_foods)
    score_display = round(score, 1)
    color = "green" if score > 65 else ("orange" if score > 40 else "red")

    summary = f"""
## 🥗 Meal Summary

### 🧮 Nutrition Score: <span style='color:{color}; font-weight:700'>{score_display}/100</span>

{score_bar(score)}

### 🥘 Ingredients Detected
"""
    for ing, q in total_quantities.items():
        summary += f"- **{ing}** : {q:.1f} g\n"

    summary += """
### 🔬 Nutrition Breakdown
"""
    for k, v in nutrition.items():
        summary += f"- **{k.capitalize()}** : {v:.2f} g\n"

    summary += """
### ⚠️ Food Combination Issues
"""
    if problems:
        for p in problems:
            summary += f"- ❌ **{p['problem']}** → {p['recommendation']}\n"
    else:
        summary += "✔ No problematic combinations.\n"

    summary += f"""
### 🧠 Final Recommendation
{recommendation}
"""

    gauge_plot = score_gauge(score_display)
    return boxed_images, summary, gauge_plot



with gr.Blocks(title="Smeal - Smart Meal Analyzer") as app:
    gr.Markdown("# 🍽️ Smeal – Smart Meal Analyzer\nUpload up to 3 images to analyze your meal.")

    with gr.Row():
        input_files = gr.File(label="Upload meal photos (1–3 images)", file_count="multiple", type="filepath")
        run_button = gr.Button("Analyze Meal 🍲")

    with gr.Row():
        output_gallery = gr.Gallery(label="Detected Ingredients (Bounding Boxes)", columns=3, height=300)
        output_score_gauge = gr.Plot(label="Nutrition Score Gauge")

    output_summary = gr.Markdown()

    run_button.click(
        analyze_meal,
        inputs=[input_files],
        outputs=[output_gallery, output_summary, output_score_gauge]
    )

app.launch()
