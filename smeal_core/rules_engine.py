rules = [
    # 1. Sugar + heavy proteins
    {
        "id": 1,
        "problem": "Sugar + Heavy Protein",
        "recommendation": "Wait 30–45 minutes between sugar and protein.",
        "condition": lambda ing, nut: nut["sucres"] > 12 and nut["proteines"] > 20
    },

    # 2. Sugar + saturated fats
    {
        "id": 2,
        "problem": "Sugar + Saturated Fats",
        "recommendation": "Avoid together or separate by 2 hours.",
        "condition": lambda ing, nut: nut["sucres"] > 12 and nut["graisses"] > 20
    },

    # 3. Protein animal + refined carbs
    {
        "id": 3,
        "problem": "Animal Protein + Refined Carbs",
        "recommendation": "Add vegetables or separate by 1 hour.",
        "condition": lambda ing, nut: any(i in ing for i in ["rice", "bread", "pasta"]) and nut["proteines"] > 20
    },

    # 4. Two animal proteins
    {
        "id": 4,
        "problem": "Two heavy animal proteins",
        "recommendation": "Use only one animal protein per meal.",
        "condition": lambda ing, nut: sum(1 for i in ing if i in ["meat","beef","chicken","fish","egg","cheese"]) >= 2
    },

    # 5. Fruit + salty meal
    {
        "id": 5,
        "problem": "Fruit + salty meal",
        "recommendation": "Eat fruits alone 2 hours before or after.",
        "condition": lambda ing, nut: any(i in ing for i in ["apple","orange","pear","banana"]) and nut["sel"] if "sel" in nut else False
    },

    # 6. Acidic fruits + milk/yogurt
    {
        "id": 6,
        "problem": "Acidic fruits + Dairy",
        "recommendation": "Separate by 45 minutes.",
        "condition": lambda ing, nut: any(i in ing for i in ["orange","lemon"]) and any(i in ing for i in ["milk","yogurt"])
    },

    # 7. Legumes + starches
    {
        "id": 7,
        "problem": "Legumes + Starches",
        "recommendation": "Avoid too often or add cumin/ginger.",
        "condition": lambda ing, nut: any(i in ing for i in ["lentils","beans"]) and any(i in ing for i in ["potato","bread","rice"])
    },

    # 8. Histamine-rich combination
    {
        "id": 8,
        "problem": "Too many histamine-rich foods",
        "recommendation": "Limit to 2 histamine-rich foods per meal.",
        "condition": lambda ing, nut: sum(1 for i in ing if i in ["tomato","vinegar","cheese","avocado","fish"]) > 2
    },

    # 9. Coffee/tea + sugar
    {
        "id": 9,
        "problem": "Caffeine + sugar",
        "recommendation": "Drink coffee after protein meal.",
        "condition": lambda ing, nut: nut["sucres"] > 12 and any(i in ing for i in ["coffee","tea"])
    },

    # 10. Cold water + fatty meal
    {
        "id": 10,
        "problem": "Cold water slows digestion of fatty food",
        "recommendation": "Use warm water with meal.",
        "condition": lambda ing, nut: nut["graisses"] > 20
    },

    # 11. Sugar + salt
    {
        "id": 11,
        "problem": "High sugar + high salt",
        "recommendation": "Wait 45–60 min between salty and sugary foods.",
        "condition": lambda ing, nut: nut["sucres"] > 12 and nut.get("sel", 0) > 1
    },

    # 12. Fiber overload + not enough water
    {
        "id": 12,
        "problem": "Too much fiber with no water",
        "recommendation": "Drink at least 1 glass of water.",
        "condition": lambda ing, nut: nut.get("fibres", 0) > 8
    },

    # 13. Heated fats + proteins
    {
        "id": 13,
        "problem": "Oxidized oils + protein",
        "recommendation": "Avoid repeated frying.",
        "condition": lambda ing, nut: any(i in ing for i in ["fried","oil"]) and nut["proteines"] > 20
    },

    # 14. Fast + slow carbs
    {
        "id": 14,
        "problem": "Fast carbs + slow carbs",
        "recommendation": "Choose only one carb source.",
        "condition": lambda ing, nut: any(i in ing for i in ["bread","white rice"]) and any(i in ing for i in ["pasta","brown rice"])
    }
]

def evaluate_rules(ingredients, nutrition):
    problems = []
    for r in rules:
        try:
            if r["condition"](ingredients, nutrition):
                problems.append({
                    "id": r["id"],
                    "problem": r["problem"],
                    "recommendation": r["recommendation"]
                })
        except:
            pass
    return problems
