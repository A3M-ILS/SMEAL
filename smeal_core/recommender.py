def build_recommendation(problems):
    if not problems:
        return "Your meal looks balanced."
    
    txt = "⚠ Possible issues detected:\n"
    for p in problems:
        txt += f"- {p['problem']} → {p['recommendation']}\n"
    return txt
