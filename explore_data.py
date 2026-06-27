import pandas as pd

# Load dataset
df = pd.read_csv("data/housing.csv")

print("===== SHAPE =====")
print(df.shape)

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== INFO =====")
print(df.info())

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== MISSING VALUES =====")

missing = df.isnull().sum()
missing = missing[missing > 0]

print(missing.sort_values(ascending=False))

print("\n===== SUMMARY =====")

print(df.describe())

numerical = df.select_dtypes(include=["int64", "float64"]).columns

categorical = df.select_dtypes(include=["object"]).columns

print("\nNumerical Features:", len(numerical))
print(numerical)

print("\nCategorical Features:", len(categorical))
print(categorical)