"""Generate a SYNTHETIC dataset of incoming raw-material lots.

All values are simulated. No real company, supplier or lab data is used.
The relationships below are assumptions written by the author for demonstration,
not findings about real feed mills.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 1200

materials = ["maize", "soybean_meal", "canola_meal", "cottonseed_meal"]
mat_p = [0.45, 0.25, 0.15, 0.15]
mat_effect = {"maize": 0.5, "soybean_meal": 0.0, "canola_meal": 0.0, "cottonseed_meal": 0.4}

suppliers = [f"S{i:02d}" for i in range(1, 13)]
supplier_risk = dict(zip(suppliers, rng.beta(1.2, 4.0, len(suppliers))))

dates = pd.date_range("2025-01-01", periods=N, freq="7h")
material = rng.choice(materials, N, p=mat_p)
supplier = rng.choice(suppliers, N)

moisture = np.clip(rng.normal(12.5, 1.6, N) + np.where(material == "maize", 0.4, 0), 9, 18)
humidity = np.clip(rng.normal(60, 15, N), 20, 95)
storage_days = np.clip(rng.gamma(2.0, 6.0, N), 0, 90)
transit_hours = np.clip(rng.gamma(2.0, 5.0, N), 1, 72)
defect_pct = np.clip(rng.exponential(1.5, N), 0, 15)

z = (-3.6
     + 0.6 * (moisture - 12.5)
     + 0.03 * (humidity - 60)
     + 0.04 * storage_days
     + 0.03 * transit_hours
     + 0.15 * defect_pct
     + 2.5 * np.array([supplier_risk[s] for s in supplier])
     + np.array([mat_effect[m] for m in material]))
p = 1 / (1 + np.exp(-z))
positive = rng.random(N) < p

# Illustrative rapid-test reading (ppb). The 20 ppb cut-off is a placeholder, not a regulatory limit.
ppb = np.where(positive, 20 + rng.lognormal(2.0, 0.8, N), np.clip(rng.lognormal(0.8, 0.7, N), 0, 19.5))

df = pd.DataFrame({
    "lot_id": [f"LOT-{i:04d}" for i in range(1, N + 1)],
    "arrival_time": dates,
    "material": material,
    "supplier_id": supplier,
    "moisture_pct": moisture.round(1),
    "ambient_humidity_pct": humidity.round(0),
    "storage_days_before_arrival": storage_days.round(0),
    "transit_hours": transit_hours.round(0),
    "visual_defect_pct": defect_pct.round(1),
    "rapid_aflatoxin_ppb": ppb.round(1),
    "aflatoxin_positive": positive.astype(int),
})
df.to_csv("data/mock_lots.csv", index=False)
print(df.shape, "positive rate:", round(df.aflatoxin_positive.mean(), 3))
