import re
def analyze_text(text: str, keywords: list[str]) -> dict:
    tokens = re.findall(r'\w+', text.lower())
    total_words = len(tokens)
    match_count = 0
    for k in keywords:
        match_count += len(re.findall(rf'\b{re.escape(k.lower())}\b', text.lower()))
    intensity = (match_count / total_words) * 1000 if total_words > 0 else 0
    return {"match_count": match_count, "total_words": total_words, "intensity_metric": intensity, "score": min(100.0, intensity/10.0)}
