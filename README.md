[README.md](https://github.com/user-attachments/files/28796406/README.md)
# 🌾 Rice Climate Risk & Precision Farming Assistant

An AI-driven command-line tool that helps farmers decide **exactly when to sow and harvest rice** based on real-time climate inputs.

---

## 🚀 What It Does

- Analyzes **rainfall, temperature, humidity, and soil type**
- Calculates **climate risk level** for rice cultivation
- Recommends the **best sowing date** based on climate zone
- Calculates the **optimal harvest date** based on rice variety
- Estimates **expected yield** in kg per hectare
- Saves results to a **CSV file** for future reference

---

## 📁 Project Structure

```
rice-climate-optimizer/
├── user_data/
│   ├── rice_data.csv        ← Sample historical data
│   └── my_results.csv       ← Your saved analysis results
├── main.py                  ← Run this to start the program
├── climate_analyzer.py      ← Climate risk analysis logic
├── harvest_optimizer.py     ← Sowing & harvest date recommendations
├── requirements.txt         ← Libraries needed (none external!)
└── README.md                ← You are here
```

---

## ▶️ How to Run

1. Make sure **Python 3.7+** is installed
2. Open terminal in this folder
3. Run the program:

```bash
python main.py
```

4. Enter your farm's climate data when prompted
5. Get your personalized sowing and harvest recommendations!

---

## 📊 Sample Output

```
============================================================
   🌾 RICE CLIMATE RISK & PRECISION FARMING ASSISTANT 🌾
============================================================

  🌧️ Rainfall    [ OPTIMAL ]  Rainfall is perfect for rice cultivation!
  🌡️ Temperature [ OPTIMAL ]  Temperature is ideal for rice growth!
  💧 Humidity    [ OPTIMAL ]  Humidity is great for rice cultivation!
  🪨 Soil        [  GOOD   ]  Loam soil is great — good water retention.

  🌟 Excellent! Conditions are ideal for rice farming.

  📌 Recommended Sowing  Date: June 15, 2025
  📌 Recommended Harvest Date: October 13, 2025
  📊 Estimated Yield         : ~5,200 kg per hectare
```

---

## 🌍 Supported Conditions

| Parameter   | Range         |
|-------------|---------------|
| Rainfall    | 0 – 400 mm    |
| Temperature | 10 – 45 °C    |
| Humidity    | 20 – 100 %    |
| Soil Types  | Clay, Loam, Sandy Loam, Sandy, Silt |
| Varieties   | Short (105d), Medium (120d), Long (150d) |

---

## 💡 How It Works

This tool uses **rule-based AI** — a set of expert agricultural rules to evaluate conditions:

- Rainfall < 100mm → LOW risk rating → delay sowing
- Temperature 25–35°C → OPTIMAL for rice growth
- Clay/Loam soil → best water retention for rice
- Score out of 100 → maps to yield estimate (1,500–6,500 kg/ha)

---

## 👨‍💻 Built With

- **Python 3** (no external libraries needed)
- Built-in modules: `csv`, `os`, `datetime`

---

## 📌 Future Improvements

- [ ] Add weather API integration for live data
- [ ] Add machine learning model for yield prediction
- [ ] Add multi-crop support (wheat, corn, cotton)
- [ ] Add a web interface using Flask

- Next version will include live weather data via Open-Meteo API and Tamil language support.
---

*Built as part of a Python + AI portfolio project by *techkamalesh878officials.**
