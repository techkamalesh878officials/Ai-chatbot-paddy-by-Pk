# climate_analyzer.py
# This file analyzes weather conditions for rice farming

# ─────────────────────────────────────────────
# IDEAL CONDITIONS FOR RICE (rule-based)
# ─────────────────────────────────────────────
IDEAL_RAINFALL_MIN = 100    # mm per month
IDEAL_RAINFALL_MAX = 200    # mm per month
IDEAL_TEMP_MIN     = 25     # degrees Celsius
IDEAL_TEMP_MAX     = 35     # degrees Celsius
IDEAL_HUMIDITY_MIN = 70     # percent


def analyze_rainfall(rainfall_mm):
    """Check if rainfall is good for rice farming."""
    if rainfall_mm < 50:
        return "POOR", "Too dry! Rice needs at least 100mm of rain. Consider irrigation."
    elif rainfall_mm < IDEAL_RAINFALL_MIN:
        return "LOW", "Rainfall is below ideal. Use supplemental irrigation."
    elif rainfall_mm <= IDEAL_RAINFALL_MAX:
        return "OPTIMAL", "Rainfall is perfect for rice cultivation!"
    elif rainfall_mm <= 250:
        return "HIGH", "Rainfall is high. Ensure proper drainage to avoid flooding."
    else:
        return "DANGER", "Too much rain! Risk of crop damage and flooding."


def analyze_temperature(temp_c):
    """Check if temperature is good for rice farming."""
    if temp_c < 15:
        return "POOR", "Too cold! Rice cannot grow below 15°C."
    elif temp_c < IDEAL_TEMP_MIN:
        return "LOW", "Temperature is a bit cool. Growth will be slow."
    elif temp_c <= IDEAL_TEMP_MAX:
        return "OPTIMAL", "Temperature is ideal for rice growth!"
    elif temp_c <= 40:
        return "HIGH", "Temperature is high. Ensure water availability to cool crops."
    else:
        return "DANGER", "Extreme heat! Rice crops are at serious risk."


def analyze_humidity(humidity_percent):
    """Check if humidity is suitable for rice."""
    if humidity_percent < 50:
        return "LOW", "Humidity is too low. Increase irrigation frequency."
    elif humidity_percent < IDEAL_HUMIDITY_MIN:
        return "MODERATE", "Humidity is acceptable but could be higher."
    elif humidity_percent <= 90:
        return "OPTIMAL", "Humidity is great for rice cultivation!"
    else:
        return "HIGH", "Very high humidity. Watch out for fungal diseases."


def analyze_soil(soil_type):
    """Check if soil type is good for rice."""
    soil_type = soil_type.lower().replace(" ", "_")
    soil_ratings = {
        "clay":       ("EXCELLENT", "Clay soil is the best for rice — retains water well!"),
        "loam":       ("GOOD",      "Loam soil is great — good water retention and nutrients."),
        "sandy_loam": ("MODERATE",  "Sandy loam is acceptable. Add organic matter for better yield."),
        "sandy":      ("POOR",      "Sandy soil drains too fast. Heavy irrigation needed."),
        "silt":       ("GOOD",      "Silt soil is good for rice with proper water management."),
    }
    return soil_ratings.get(
        soil_type,
        ("UNKNOWN", f"Soil type '{soil_type}' not recognized. Using average conditions.")
    )


def get_overall_risk(rainfall_status, temp_status, humidity_status):
    """Calculate the overall climate risk level."""
    danger_count = sum(
        1 for s in [rainfall_status, temp_status, humidity_status]
        if s in ["DANGER", "POOR"]
    )
    low_count = sum(
        1 for s in [rainfall_status, temp_status, humidity_status]
        if s in ["LOW", "HIGH"]
    )

    if danger_count >= 1:
        return "HIGH RISK", "⚠️  Conditions are dangerous for rice farming right now."
    elif low_count >= 2:
        return "MEDIUM RISK", "⚡ Conditions are challenging. Careful management needed."
    elif low_count == 1:
        return "LOW RISK", "✅ Conditions are mostly good with minor concerns."
    else:
        return "NO RISK", "🌟 Excellent! Conditions are ideal for rice farming."


def full_climate_report(rainfall_mm, temp_c, humidity_percent, soil_type):
    """Run a complete climate analysis and return all results."""
    rain_status,  rain_msg  = analyze_rainfall(rainfall_mm)
    temp_status,  temp_msg  = analyze_temperature(temp_c)
    hum_status,   hum_msg   = analyze_humidity(humidity_percent)
    soil_status,  soil_msg  = analyze_soil(soil_type)
    risk_level,   risk_msg  = get_overall_risk(rain_status, temp_status, hum_status)

    return {
        "rainfall":  {"status": rain_status,  "message": rain_msg},
        "temperature": {"status": temp_status, "message": temp_msg},
        "humidity":  {"status": hum_status,   "message": hum_msg},
        "soil":      {"status": soil_status,  "message": soil_msg},
        "overall_risk": {"level": risk_level, "message": risk_msg},
    }
