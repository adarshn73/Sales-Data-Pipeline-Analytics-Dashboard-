import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/raw_sales_data.csv")

print("Initial shape:", df.shape)
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# -----------------------------
# CLEAN DATA
# -----------------------------
df["date"] = pd.to_datetime(df["date"])
df = df.drop_duplicates()
df["discount_pct"] = df["discount_pct"].fillna(0)

# Recalculate revenue, cost, and profit
df["revenue"] = (df["units_sold"] * df["price_per_unit"] * (1 - df["discount_pct"])).round(2)
df["total_cost"] = (df["units_sold"] * df["cost_per_unit"]).round(2)
df["profit"] = (df["revenue"] - df["total_cost"]).round(2)

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
df["year"] = df["date"].dt.year
df["month_num"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%b")
df["year_month"] = df["date"].dt.to_period("M").astype(str)
df["quarter"] = df["date"].dt.to_period("Q").astype(str)
df["profit_margin"] = np.where(df["revenue"] > 0, df["profit"] / df["revenue"], 0).round(4)

# -----------------------------
# SAVE CLEANED DATA
# -----------------------------
os.makedirs("data", exist_ok=True)
df.to_csv("data/cleaned_sales_data.csv", index=False)

print("\nShape after cleaning:", df.shape)
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
total_units = df["units_sold"].sum()
total_orders = df["order_id"].nunique()
avg_order_value = total_revenue / total_orders
avg_profit_margin = df["profit_margin"].mean()

print("\n===== KEY KPIs =====")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: ${avg_order_value:,.2f}")
print(f"Average Profit Margin: {avg_profit_margin:.2%}")

# -----------------------------
# SUMMARY TABLES
# -----------------------------
monthly_summary = df.groupby("year_month", as_index=False).agg({
    "revenue": "sum",
    "profit": "sum",
    "units_sold": "sum"
})
monthly_summary["year_month"] = pd.to_datetime(monthly_summary["year_month"])

product_summary = df.groupby("product_name", as_index=False).agg({
    "revenue": "sum",
    "profit": "sum",
    "units_sold": "sum"
}).sort_values("revenue", ascending=False)

channel_summary = df.groupby("channel", as_index=False).agg({
    "revenue": "sum",
    "profit": "sum",
    "units_sold": "sum"
}).sort_values("revenue", ascending=False)

region_summary = df.groupby("region", as_index=False).agg({
    "revenue": "sum",
    "profit": "sum",
    "units_sold": "sum"
}).sort_values("revenue", ascending=False)

category_summary = df.groupby("category", as_index=False).agg({
    "revenue": "sum",
    "profit": "sum",
    "units_sold": "sum"
}).sort_values("revenue", ascending=False)

# Save summary tables
monthly_summary.to_csv("data/monthly_summary.csv", index=False)
product_summary.to_csv("data/product_summary.csv", index=False)
channel_summary.to_csv("data/channel_summary.csv", index=False)
region_summary.to_csv("data/region_summary.csv", index=False)
category_summary.to_csv("data/category_summary.csv", index=False)

# -----------------------------
# CHARTS
# -----------------------------
os.makedirs("dashboard", exist_ok=True)

plt.figure(figsize=(12, 6))
plt.plot(monthly_summary["year_month"], monthly_summary["revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("dashboard/monthly_revenue.png")
plt.show()

plt.figure(figsize=(12, 6))
plt.bar(product_summary["product_name"], product_summary["revenue"])
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("dashboard/product_revenue.png")
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(channel_summary["channel"], channel_summary["profit"])
plt.title("Profit by Channel")
plt.xlabel("Channel")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("dashboard/channel_profit.png")
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(region_summary["region"], region_summary["revenue"])
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("dashboard/region_revenue.png")
plt.show()