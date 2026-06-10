# harvest_optimizer.py
# This file recommends the best sowing and harvesting dates for rice

from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# RICE GROWTH STAGES (days from sowing)
# ─────────────────────────────────────────────
RICE_GROWTH_DAYS = {
    "short":  105,   # Short-duration variety (e.g. IR36)
    "medium": 120,   # Medium-duration variety (e.g. IR64)  ← default
    "long":   150,   # Long-duration variety  (e.g. Basmati)
}

# Best months to sow rice (1 = January … 12 = December)
BEST_SOWING_MONTHS = {
    "tropical":    [6, 7, 8],       # June–August (monsoon season)
    "subtropical": [5, 6, 7],       # May–July
    "temperate":   [4, 5, 6],       # April–June
}


def recommend_sowing_date(rainfall_mm, temp_c, current_month=None):
    """
    Recommend the best sowing date based on climate conditions.
    Returns a suggested sowing date and an explanation.
    """
    if current_month is None:
        current_month = datetime.now().month

    # Determine climate zone from temperature
    if temp_c >= 28:
        zone = "tropical"
    elif temp_c >= 22:
        zone = "subtropical"
    else:
        zone = "temperate"

    best_months = BEST_SOWING_MONTHS[zone]

    # Find the next best sowing month from today
    today = datetime.now()
    sowing_date = None

    for month in best_months:
        if month >= current_month:
            sowing_date = datetime(today.year, month, 15)
            break

    # If all best months have passed, suggest next year
    if sowing_date is None:
        sowing_date = datetime(today.year + 1, best_months[0], 15)

    # Adjust if rainfall is too low (wait for more rain)
    if rainfall_mm < 80:
        sowing_date += timedelta(days=15)
        note = "⏳ Sowing delayed by 15 days — waiting for adequate rainfall."
    elif rainfall_mm > 220:
        sowing_date += timedelta(days=7)
        note = "⏳ Sowing delayed by 7 days — waiting for floodwater to recede."
    else:
        note = "✅ Conditions are good. Sow on the recommended date."

    return sowing_date.strftime("%B %d, %Y"), note, zone


def recommend_harvest_date(sowing_date_str, variety="medium"):
    """
    Calculate the best harvest date based on sowing date and rice variety.
    Returns harvest date and growth duration.
    """
    try:
        sowing_date = datetime.strptime(sowing_date_str, "%B %d, %Y")
    except ValueError:
        return None, "Invalid sowing date format."

    growth_days = RICE_GROWTH_DAYS.get(variety, RICE_GROWTH_DAYS["medium"])
    harvest_date = sowing_date + timedelta(days=growth_days)

    # Add a 5-day buffer for safety
    optimal_harvest = harvest_date + timedelta(days=5)

    return optimal_harvest.strftime("%B %d, %Y"), growth_days


def estimate_yield(rainfall_mm, temp_c, humidity_percent, soil_type):
    """
    Estimate rice yield in kg per hectare based on conditions.
    Uses simple rule-based scoring.
    """
    score = 0

    # Rainfall score (max 30 points)
    if 100 <= rainfall_mm <= 200:
        score += 30
    elif 80 <= rainfall_mm < 100 or 200 < rainfall_mm <= 230:
        score += 20
    elif 50 <= rainfall_mm < 80:
        score += 10
    else:
        score += 0

    # Temperature score (max 30 points)
    if 25 <= temp_c <= 32:
        score += 30
    elif 22 <= temp_c < 25 or 32 < temp_c <= 36:
        score += 20
    elif 18 <= temp_c < 22:
        score += 10
    else:
        score += 0

    # Humidity score (max 20 points)
    if 70 <= humidity_percent <= 85:
        score += 20
    elif 60 <= humidity_percent < 70 or 85 < humidity_percent <= 92:
        score += 12
    else:
        score += 5

    # Soil score (max 20 points)
    soil_scores = {
        "clay": 20, "loam": 18, "silt": 15,
        "sandy_loam": 10, "sandy": 5
    }
    score += soil_scores.get(soil_type.lower().replace(" ", "_"), 10)

    # Convert score (0–100) to yield estimate (1500–6500 kg/ha)
    base_yield  = 1500
    max_yield   = 6500
    yield_kg    = base_yield + int((score / 100) * (max_yield - base_yield))

    if score >= 80:
        quality = "🌟 Excellent"
    elif score >= 60:
        quality = "✅ Good"
    elif score >= 40:
        quality = "⚡ Average"
    else:
        quality = "⚠️  Below Average"

    return yield_kg, quality, score
