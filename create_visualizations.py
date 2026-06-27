import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/housing.csv")

os.makedirs("visualizations", exist_ok=True)

# 1. SalePrice distribution
plt.figure(figsize=(9, 6))
plt.hist(df["SalePrice"], bins=40)
plt.xlabel("Sale Price")
plt.ylabel("Number of Houses")
plt.title("Distribution of Sale Prices")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("visualizations/saleprice_distribution.png", dpi=300)
plt.close()

# 2. Living Area vs Sale Price
plt.figure(figsize=(9, 6))
plt.scatter(df["Gr Liv Area"], df["SalePrice"], alpha=0.5)
plt.xlabel("Above Ground Living Area")
plt.ylabel("Sale Price")
plt.title("Living Area vs Sale Price")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("visualizations/living_area_vs_price.png", dpi=300)
plt.close()

# 3. Overall Quality vs Sale Price
plt.figure(figsize=(9, 6))
plt.scatter(df["Overall Qual"], df["SalePrice"], alpha=0.5)
plt.xlabel("Overall Quality")
plt.ylabel("Sale Price")
plt.title("Overall Quality vs Sale Price")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("visualizations/overall_quality_vs_price.png", dpi=300)
plt.close()

# 4. Garage Area vs Sale Price
plt.figure(figsize=(9, 6))
plt.scatter(df["Garage Area"], df["SalePrice"], alpha=0.5)
plt.xlabel("Garage Area")
plt.ylabel("Sale Price")
plt.title("Garage Area vs Sale Price")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("visualizations/garage_area_vs_price.png", dpi=300)
plt.close()

# 5. Year Built vs Sale Price
plt.figure(figsize=(9, 6))
plt.scatter(df["Year Built"], df["SalePrice"], alpha=0.5)
plt.xlabel("Year Built")
plt.ylabel("Sale Price")
plt.title("Year Built vs Sale Price")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("visualizations/year_built_vs_price.png", dpi=300)
plt.close()

# 6. Top correlations with SalePrice
numeric_df = df.select_dtypes(include=["int64", "float64"])
corr = numeric_df.corr()["SalePrice"].sort_values(ascending=False)

top_corr = corr.drop("SalePrice").head(10)

plt.figure(figsize=(10, 7))
plt.barh(top_corr.index, top_corr.values)
plt.xlabel("Correlation with Sale Price")
plt.title("Top 10 Features Correlated with Sale Price")
plt.gca().invert_yaxis()
plt.grid(axis="x", alpha=0.25)
plt.tight_layout()
plt.savefig("visualizations/top_correlations.png", dpi=300)
plt.close()

print("Saved graphs to visualizations folder.")