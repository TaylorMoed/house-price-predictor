import pandas as pd

# Load dataset
df = pd.read_csv("data/housing.csv")

print("Original Shape:", df.shape)

# Check missing values
missing = df.isnull().sum()
missing = missing[missing > 0]

# Remove identifier columns
df = df.drop(columns=["Order", "PID"])

# Categorical columns where missing means "feature not present"
none_columns = [
    "Pool QC",
    "Misc Feature",
    "Alley",
    "Fence",
    "Mas Vnr Type",
    "Fireplace Qu",
    "Garage Type",
    "Garage Finish",
    "Garage Qual",
    "Garage Cond",
    "Bsmt Exposure",
    "BsmtFin Type 1",
    "BsmtFin Type 2",
    "Bsmt Qual",
    "Bsmt Cond"
]

df["Electrical"] = df["Electrical"].fillna(df["Electrical"].mode()[0])

for col in none_columns:
    if col in df.columns:
        df[col] = df[col].fillna("None")

# Numerical columns - fill missing values with the median
numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

for col in numeric_columns:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

# One-hot encode all categorical columns
df = pd.get_dummies(df, drop_first=True)

print("\nShape after encoding:", df.shape)

# Save cleaned dataset
df.to_csv("data/housing_cleaned.csv", index=False)

print("\nCleaned dataset saved as data/housing_cleaned.csv")

print("\nRemaining Missing Values:")
print(df.isnull().sum()[df.isnull().sum() > 0])