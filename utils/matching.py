def compute_match_score(provider, max_price, min_rating, max_distance, preferred_day, urgency):
    """
    Compute an AI match score (0–100) for a provider based on user preferences.

    Scoring breakdown:
      - Base category match:  20 pts
      - Rating quality:       25 pts
      - Price fit:            20 pts
      - Distance:             20 pts
      - Day availability:     15 pts
      - Experience:            5 pts
      - Urgency bonus:        up to 10 pts (replaces some availability weight)
    """
    score = 0.0

    # Base score for passing filters
    score += 20

    # Rating (0–25 pts)
    score += (provider["rating"] - 4.0) / 1.0 * 25

    # Price fit (0–20 pts) — cheaper relative to max = better
    price_ratio = 1 - (provider["price"] / max_price) if max_price > 0 else 0
    score += max(0, price_ratio) * 20

    # Distance (0–20 pts)
    dist_score = max(0, 1 - provider["distance"] / (max_distance + 0.1)) * 20
    score += dist_score

    # Day availability (0–15 pts)
    if preferred_day in provider["availability"]:
        score += 15

    # Urgency bonus — providers with more open days rank higher for urgent requests
    if urgency == "ASAP (today/tomorrow)":
        avail_ratio = len(provider["availability"]) / 7
        score += avail_ratio * 10

    # Experience (0–5 pts)
    score += min(provider["experience"] / 15 * 5, 5)

    return round(min(score, 100), 1)


def get_score_breakdown(provider, max_price, max_distance, preferred_day):
    """Return a dict of individual score components for visualisation."""
    return {
        "Rating quality":  min(int((provider["rating"] - 4.0) / 1.0 * 25), 25),
        "Price fit":       max(0, int((1 - provider["price"] / max_price) * 20)) if max_price > 0 else 0,
        "Distance":        int(max(0, 1 - provider["distance"] / (max_distance + 0.1)) * 20),
        "Availability":    15 if preferred_day in provider["availability"] else 0,
        "Experience":      min(int(provider["experience"] / 15 * 5), 5),
    }


def filter_and_rank(providers, category, max_price, min_rating, max_distance, preferred_day, urgency):
    """Filter providers by hard constraints then rank by match score."""
    filtered = [
        p for p in providers
        if (category == "All" or p["category"] == category)
        and p["price"] <= max_price
        and p["rating"] >= min_rating
        and p["distance"] <= max_distance
    ]

    for p in filtered:
        p["score"] = compute_match_score(p, max_price, min_rating, max_distance, preferred_day, urgency)

    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered
