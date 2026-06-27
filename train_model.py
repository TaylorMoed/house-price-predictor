import pandas as pd
import joblib 

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Metrics
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

# Load cleaned dataset
df = pd.read_csv("data/housing_cleaned.csv")

print("Dataset Shape:", df.shape)

# Target variable
y = df["SalePrice"]

# Features
X = df.drop(columns=["SalePrice"])

print("\nFeatures:", X.shape)
print("Target:", y.shape)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Samples:", X_train.shape)
print("Testing Samples:", X_test.shape)

# Train Linear Regression
model = LinearRegression()

model.fit(X_train, y_train)

print("\nModel trained successfully!")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\n===== LINEAR REGRESSION RESULTS =====")
print(f"Mean Absolute Error: ${mae:,.2f}")
print(f"Root Mean Squared Error: ${rmse:,.2f}")
print(f"R² Score: {r2:.3f}")

from sklearn.ensemble import RandomForestRegressor

# Train Random Forest
rf_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_predictions)
rf_rmse = mean_squared_error(y_test, rf_predictions) ** 0.5
rf_r2 = r2_score(y_test, rf_predictions)

print("\n===== RANDOM FOREST RESULTS =====")
print(f"Mean Absolute Error: ${rf_mae:,.2f}")
print(f"Root Mean Squared Error: ${rf_rmse:,.2f}")
print(f"R² Score: {rf_r2:.3f}")

# Save the trained model
joblib.dump(rf_model, "models/house_price_model.pkl")

print("\nModel saved to models/house_price_model.pkl")

joblib.dump(X.columns.tolist(), "models/model_features.pkl")

print("Feature list saved to models/model_features.pkl")