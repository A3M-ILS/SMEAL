import pandas as pd
import json
import re

csv_path = "data/Table_Ciqual_2020.csv"

# French CSV: ; separator, latin-1 encoding
df = pd.read_csv(csv_path, sep=";", encoding="latin-1")

print("\nColumns loaded:")
print(df.columns[:20].tolist())

# Correct columns from your file
COL_PROT = "ProtÃ©ines, N x facteur de Jones (g/100 g)"
COL_GLUC = "Glucides (g/100 g)"
COL_SUC  = "Sucres (g/100 g)"
COL_FAT  = "Lipides (g/100 g)"
COL_NAME = "alim_nom_fr"

def clean_value(v):
    if pd.isna(v):
        return None

    if isinstance(v, str):
        v = v.strip().lower()

        if v in ["", "-"]:
            return None
        if "traces" in v:
            return 0.01

        # FIX: French decimal comma → dot
        v = v.replace(",", ".")

        if v.startswith("<"):
            try:
                return float(v[1:])
            except:
                return None

    try:
        return float(v)
    except:
        return None

def normalize_name(name):
    if isinstance(name, float):
        return ""
    name = name.lower().strip()
    name = re.sub(r"\s+", " ", name)
    return name

nutrition_db = {}

for _, row in df.iterrows():
    name = normalize_name(row[COL_NAME])

    prot = clean_value(row[COL_PROT])
    gluc = clean_value(row[COL_GLUC])
    sucr = clean_value(row[COL_SUC])
    fat  = clean_value(row[COL_FAT])

    nutrition_db[name] = {
        "proteines": prot if prot is not None else 0.0,
        "glucides":  gluc if gluc is not None else 0.0,
        "sucres":    sucr if sucr is not None else 0.0,
        "graisses":  fat  if fat is not None else 0.0
    }

with open("data/nutrition_db.json", "w", encoding="utf-8") as f:
    json.dump(nutrition_db, f, ensure_ascii=False, indent=4)

print("\n✔ nutrition_db.json generated successfully!")
