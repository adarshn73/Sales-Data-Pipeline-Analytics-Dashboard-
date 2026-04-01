import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load monthly summary
monthly = pd.read_csv("data/monthly_summary.csv")
monthly["year_month"] = pd.to_datetime(monthly["year_month"])
monthly = monthly.sort_values("year_month").reset_index(drop=True)

# Create a 3-month moving average
monthly["moving_avg_3"] = monthly["revenue"].rolling(window=3).mean()

# Forecast next 3 months
forecast_periods = 3
last_date = monthly["year_month"].max()
recent_values = monthly["revenue"].tolist()

future_rows = []

for i in range(1, forecast_periods + 1):
    next_date = last_date + pd.DateOffset(months=i)
    forecast_value = np.mean(recent_values[-3:])
    recent_values.append(forecast_value)

    future_rows.append({
        "year_month": next_date,
        "forecast_revenue": round(forecast_value, 2)
    })

forecast_df = pd.DataFrame(future_rows)
forecast_df.to_csv("data/monthly_forecast.csv", index=False)

# Plot
os.makedirs("dashboard", exist_ok=True)

plt.figure(figsize=(12, 6))
plt.plot(monthly["year_month"], monthly["revenue"], marker="o", label="Historical Revenue")
plt.plot(forecast_df["year_month"], forecast_df["forecast_revenue"], marker="o", linestyle="--", label="Forecast Revenue")
plt.title("Historical Revenue with 3-Month Forecast")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("dashboard/forecast_chart.png")
plt.show()

print("Forecast created successfully.")
print("Saved to data/monthly_forecast.csv")
print(forecast_df)