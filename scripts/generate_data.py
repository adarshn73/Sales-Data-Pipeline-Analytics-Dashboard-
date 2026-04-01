import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

# -----------------------------
# SETTINGS
# -----------------------------
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
n_orders = 8000

products = [
    {
        "product_name": "PulseFuel Blue Raspberry Pre",
        "category": "Stim Pre-Workout",
        "flavor": "Blue Raspberry",
        "price": 42.99,
        "cost": 18.50,
        "weight": 0.20
    },
    {
        "product_name": "PulseFuel Watermelon Pre",
        "category": "Stim Pre-Workout",
        "flavor": "Watermelon",
        "price": 41.99,
        "cost": 17.80,
        "weight": 0.18
    },
    {
        "product_name": "PulseFuel Sour Gummy Pre",
        "category": "Stim Pre-Workout",
        "flavor": "Sour Gummy",
        "price": 43.99,
        "cost": 19.10,
        "weight": 0.16
    },
    {
        "product_name": "PulseFuel Mango Pump",
        "category": "Pump Formula",
        "flavor": "Mango",
        "price": 39.99,
        "cost": 16.25,
        "weight": 0.14
    },
    {
        "product_name": "PulseFuel Fruit Punch Non-Stim",
        "category": "Non-Stim Pre-Workout",
        "flavor": "Fruit Punch",
        "price": 38.99,
        "cost": 15.90,
        "weight": 0.12
    },
    {
        "product_name": "PulseFuel Energy Gummies",
        "category": "Energy Gummies",
        "flavor": "Mixed Berry",
        "price": 24.99,
        "cost": 9.50,
        "weight": 0.12
    },
    {
        "product_name": "PulseFuel Variety Sample Pack",
        "category": "Sample Pack",
        "flavor": "Variety",
        "price": 14.99,
        "cost": 5.25,
        "weight": 0.08
    }
]

channels = ["Website", "Amazon", "Retail"]
channel_weights = [0.50, 0.30, 0.20]

regions = ["Northeast", "South", "Midwest", "West"]
region_weights = [0.24, 0.29, 0.22, 0.25]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def seasonal_multiplier(date_obj):
    month = date_obj.month
    if month == 1:
        return 1.35
    elif month in [5, 6, 7]:
        return 1.20
    elif month in [11, 12]:
        return 1.10
    else:
        return 1.00

def channel_discount_options(channel):
    if channel == "Website":
        return [0, 0.05, 0.10, 0.15]
    elif channel == "Amazon":
        return [0, 0.05, 0.10]
    else:
        return [0, 0.03, 0.05]

rows = []

product_weights = [p["weight"] for p in products]

for i in range(1, n_orders + 1):
    date = random_date(start_date, end_date)
    product = random.choices(products, weights=product_weights, k=1)[0]
    channel = random.choices(channels, weights=channel_weights, k=1)[0]
    region = random.choices(regions, weights=region_weights, k=1)[0]

    base_units = np.random.poisson(2) + 1
    units_sold = max(1, int(round(base_units * seasonal_multiplier(date))))

    discount_pct = random.choice(channel_discount_options(channel))
    price = product["price"]
    cost = product["cost"]

    effective_price = price * (1 - discount_pct)
    revenue = round(units_sold * effective_price, 2)
    total_cost = round(units_sold * cost, 2)
    profit = round(revenue - total_cost, 2)

    rows.append({
        "order_id": f"PF-{100000 + i}",
        "date": date.strftime("%Y-%m-%d"),
        "product_name": product["product_name"],
        "category": product["category"],
        "flavor": product["flavor"],
        "channel": channel,
        "region": region,
        "units_sold": units_sold,
        "price_per_unit": round(price, 2),
        "cost_per_unit": round(cost, 2),
        "discount_pct": discount_pct,
        "revenue": revenue,
        "total_cost": total_cost,
        "profit": profit
    })

df = pd.DataFrame(rows)

# Add a few duplicates for cleaning practice
duplicate_rows = df.sample(25, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# Add some missing discounts for cleaning practice
missing_idx = df.sample(20, random_state=7).index
df.loc[missing_idx, "discount_pct"] = np.nan

os.makedirs("data", exist_ok=True)
df.to_csv("data/raw_sales_data.csv", index=False)

print("Raw dataset created successfully.")
print("Saved to data/raw_sales_data.csv")
print(df.head())
print("Total rows:", len(df))