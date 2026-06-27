import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Create folders if needed
os.makedirs("visualizations", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Load cleaned data
df = pd.read_csv("data/housing_cleaned.csv")

X = df.drop(columns=["SalePrice"])
y = df["SalePrice"]

# Same split used in training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Load model and feature names
model = joblib.load("models/house_price_model.pkl")
features = joblib.load("models/model_features.pkl")

# Make predictions
predictions = model.predict(X_test)

# -----------------------------
# 1. Feature Importance
# -----------------------------
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\nTop 20 Most Important Features:")
print(importance.head(20))

importance.to_csv("results/feature_importance.csv", index=False)

top20 = importance.head(20)

plt.figure(figsize=(10, 8))
plt.barh(top20["Feature"], top20["Importance"])
plt.gca().invert_yaxis()
plt.title("Top 20 Most Important Features")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("visualizations/feature_importance.png", dpi=300)
plt.show()

# -----------------------------
# 2. Actual vs Predicted
# -----------------------------
plt.figure(figsize=(8, 8))
plt.scatter(y_test, predictions, alpha=0.6)

min_val = min(y_test.min(), predictions.min())
max_val = max(y_test.max(), predictions.max())

plt.plot(
    [min_val, max_val],
    [min_val, max_val],
    "r--",
    linewidth=2,
    label="Perfect Prediction"
)

plt.legend()
plt.title("Actual vs Predicted House Prices")
plt.xlabel("Actual Sale Price")
plt.ylabel("Predicted Sale Price")
plt.tight_layout()
plt.savefig("visualizations/actual_vs_predicted.png", dpi=300)
plt.show()

# -----------------------------
# 3. Residual Plot
# -----------------------------
residuals = y_test - predictions

plt.figure(figsize=(8, 6))
plt.scatter(predictions, residuals, alpha=0.6)

plt.axhline(
    y=0,
    color="red",
    linestyle="--",
    linewidth=2
)

plt.title("Residual Plot")
plt.xlabel("Predicted Sale Price")
plt.ylabel("Residual (Actual - Predicted)")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig("visualizations/residual_plot.png", dpi=300)
plt.show()

print("\nSaved:")
print("visualizations/feature_importance.png")
print("visualizations/actual_vs_predicted.png")
print("visualizations/residual_plot.png")
print("results/feature_importance.csv")