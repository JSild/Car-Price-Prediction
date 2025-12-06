import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# LOAD CLEANED DATA

df = pd.read_csv("auto24_cleaned.csv")

print("Dataset shape:", df.shape)
print("\nMissing values per column:\n", df.isna().sum())


# SUMMARY STATISTICS

print("\nPrice statistics:\n", df["price"].describe())
print("\nMileage statistics:\n", df["mileage_km"].describe())
print("\nYear statistics:\n", df["reg_year"].describe())
print("\nPower statistics:\n", df["power_kw"].describe())

print("\nTop 20 brands:\n", df["Mark"].value_counts().head(20))
print("\nTop 20 models:\n", df["Mudel"].value_counts().head(20))


# VISUALIZATIONS

plt.figure(figsize=(10,5))
sns.histplot(df["price"], kde=True)
plt.title("Price Distribution")
plt.savefig("fig_price_distribution.png")
plt.close()

plt.figure(figsize=(10,5))
sns.histplot(df["mileage_km"], kde=True)
plt.title("Mileage Distribution")
plt.savefig("fig_mileage_distribution.png")
plt.close()

plt.figure(figsize=(10,5))
sns.scatterplot(x=df["mileage_km"], y=df["price"], alpha=0.3)
plt.title("Mileage vs Price")
plt.savefig("fig_mileage_vs_price.png")
plt.close()

plt.figure(figsize=(10,5))
sns.scatterplot(x=df["car_age"], y=df["price"], alpha=0.3)
plt.title("Car Age vs Price")
plt.savefig("fig_age_vs_price.png")
plt.close()

# Average price per brand (top 20)
brand_avg = df.groupby("Mark")["price"].mean().sort_values(ascending=False).head(20)

plt.figure(figsize=(12,6))
sns.barplot(x=brand_avg.index, y=brand_avg.values)
plt.xticks(rotation=45)
plt.title("Top 20 Brands by Average Price")
plt.savefig("fig_brand_avg_price.png")
plt.close()

