# main.py
# AI Climate Risk & Precision Farming Assistant for Rice
# Run this file to start the program: python main.py

import csv
import os
from datetime import datetime
from climate_analyzer import full_climate_report
from harvest_optimizer import recommend_sowing_date, recommend_harvest_date, estimate_yield

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def print_banner():
    print("\n" + "=" * 60)
    print("   🌾 RICE CLIMATE RISK & PRECISION FARMING ASSISTANT 🌾")
    print("=" * 60)
    print("   Helping farmers decide WHEN to SOW and HARVEST rice")
    print("=" * 60 + "\n")


def print_section(title):
    print("\n" + "-" * 60)
    print(f"  {title}")
    print("-" * 60)


def get_float_input(prompt, min_val, max_val):
    """Ask the user for a number and validate it."""
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"  ⚠️  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠️  Invalid input. Please enter a number.")


def get_soil_input():
    """Ask user to pick a soil type."""
    soil_types = ["clay", "loam", "sandy_loam", "sandy", "silt"]
    print("\n  Soil types available:")
    for i, soil in enumerate(soil_types, 1):
        print(f"    {i}. {soil.replace('_', ' ').title()}")
    while True:
        try:
            choice = int(input("\n  Enter the number for your soil type: "))
            if 1 <= choice <= len(soil_types):
                return soil_types[choice - 1]
            else:
                print(f"  ⚠️  Please enter a number between 1 and {len(soil_types)}.")
        except ValueError:
            print("  ⚠️  Invalid input. Please enter a number.")


def get_variety_input():
    """Ask user to pick a rice variety."""
    varieties = {
        "1": ("short",  "Short-duration  (~105 days) — e.g. IR36"),
        "2": ("medium", "Medium-duration (~120 days) — e.g. IR64  [recommended]"),
        "3": ("long",   "Long-duration   (~150 days) — e.g. Basmati"),
    }
    print("\n  Rice varieties:")
    for key, (_, desc) in varieties.items():
        print(f"    {key}. {desc}")
    while True:
        choice = input("\n  Enter the number for your rice variety (default 2): ").strip()
        if choice == "":
            return "medium"
        if choice in varieties:
            return varieties[choice][0]
        print("  ⚠️  Please enter 1, 2, or 3.")


def save_results(data, filepath="user_data/my_results.csv"):
    """Save the user's results to a CSV file."""
    file_exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    print(f"\n  💾 Results saved to: {filepath}")


# ─────────────────────────────────────────────
# MAIN PROGRAM
# ─────────────────────────────────────────────

def main():
    print_banner()
    print("  Welcome! Enter your farm's current conditions below.")
    print("  The AI will recommend the best sowing and harvest dates.\n")

    # ── Collect user inputs ──────────────────
    print_section("📥 STEP 1: Enter Your Climate Data")

    rainfall = get_float_input(
        "\n  Average monthly rainfall (mm) [0–400]: ", 0, 400
    )
    temperature = get_float_input(
        "  Current temperature (°C)      [10–45]: ", 10, 45
    )
    humidity = get_float_input(
        "  Humidity (%)                  [20–100]: ", 20, 100
    )

    print_section("🌱 STEP 2: Enter Your Farm Data")
    soil_type = get_soil_input()
    variety   = get_variety_input()

    # ── Run Climate Analysis ─────────────────
    print_section("🔍 STEP 3: Climate Analysis Results")

    report = full_climate_report(rainfall, temperature, humidity, soil_type)

    print(f"\n  🌧️  Rainfall    [{report['rainfall']['status']:^10}]  {report['rainfall']['message']}")
    print(f"  🌡️  Temperature [{report['temperature']['status']:^10}]  {report['temperature']['message']}")
    print(f"  💧 Humidity    [{report['humidity']['status']:^10}]  {report['humidity']['message']}")
    print(f"  🪨 Soil        [{report['soil']['status']:^10}]  {report['soil']['message']}")
    print(f"\n  {report['overall_risk']['message']}")
    print(f"  Overall Risk Level: {report['overall_risk']['level']}")

    # ── Sowing & Harvest Recommendations ────
    print_section("📅 STEP 4: Sowing & Harvest Recommendations")

    current_month = datetime.now().month
    sow_date, sow_note, zone = recommend_sowing_date(rainfall, temperature, current_month)
    harvest_date, growth_days = recommend_harvest_date(sow_date, variety)

    print(f"\n  🌍 Climate Zone  : {zone.title()}")
    print(f"  🌾 Rice Variety  : {variety.title()} (~{growth_days} days to harvest)")
    print(f"\n  📌 Recommended Sowing Date  : {sow_date}")
    print(f"  📌 Recommended Harvest Date : {harvest_date}")
    print(f"\n  {sow_note}")

    # ── Yield Estimate ───────────────────────
    print_section("📊 STEP 5: Estimated Yield")

    yield_kg, quality, score = estimate_yield(rainfall, temperature, humidity, soil_type)

    print(f"\n  Condition Score  : {score}/100")
    print(f"  Yield Quality    : {quality}")
    print(f"  Estimated Yield  : ~{yield_kg:,} kg per hectare")

    # ── Summary ─────────────────────────────
    print_section("✅ SUMMARY")
    print(f"""
  Crop         : Rice ({variety.title()} variety)
  Sow on       : {sow_date}
  Harvest on   : {harvest_date}
  Expected     : ~{yield_kg:,} kg/hectare  ({quality})
  Risk Level   : {report['overall_risk']['level']}
    """)

    # ── Save Results ─────────────────────────
    save = input("  💾 Save these results to a file? (y/n): ").strip().lower()
    if save == "y":
        save_results({
            "date_analyzed":  datetime.now().strftime("%Y-%m-%d"),
            "rainfall_mm":    rainfall,
            "temperature_c":  temperature,
            "humidity_%":     humidity,
            "soil_type":      soil_type,
            "variety":        variety,
            "sowing_date":    sow_date,
            "harvest_date":   harvest_date,
            "yield_kg_ha":    yield_kg,
            "risk_level":     report['overall_risk']['level'],
        })

    print("\n" + "=" * 60)
    print("  🌾 Thank you for using the Rice Farming Assistant!")
    print("  Good luck with your harvest! 🚜")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
