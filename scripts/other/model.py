"""
Task 4: Model Development & Evaluation
Authors: Jasper Suursild, Artjom Vassiljev, Hugo Arrak

Trains several regression models to predict car prices based on the cleaned
Auto24 dataset (auto24_cleaned.csv) and compares their performance.
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

import joblib


# 1. LOAD CLEANED DATA

df = pd.read_csv("../../data/processed/auto24_model_data.csv", low_memory=False)
print("Loaded dataset shape:", df.shape)

# Drop junk columns created from broken CSV (Unnamed: ...)
df = df.loc[:, ~df.columns.str.startswith("Unnamed:")]
print("After dropping Unnamed columns:", df.shape)

# 2. TARGET & FEATURE SELECTION
# Target variable: price
if "price" not in df.columns:
    raise ValueError("Column 'price' not found in auto24_cleaned.csv")

y = df["price"]

# Columns we definitely do NOT want to use as features:
# - Link: just URL, unique ID
# - Täisnimi: full listing text, nearly unique, very noisy
# - Hind: original price string (we use numeric 'price' instead)
# - Läbisõidumõõdiku näit: raw mileage text (we use 'mileage_km')
# - Esmane reg: raw registration text (we use 'reg_year')
# - Mootor: engine text (we use numeric engine fields)
# - Müüja, Parim pakkumine, Alghind, etc: seller/auction meta that can leak info
columns_to_drop = [
    "price",          # target itself
    "Link",
    "Täisnimi",
    "Hind",
    "Läbisõidumõõdiku näit",
    "Esmane reg",
    "Mootor",
    "Müüja",
    "Eksporthind",
    "Hetkehind",
    "Lõpuni on jäänud",
    "Lõpuaeg",
    "Pikenemise samm",
    "Parim pakkumine",
    "Alghind",
    "Pakkumiste arv",
    "Vaatamiste arv",
]

# Keep only columns that actually exist in the dataframe
columns_to_drop = [c for c in columns_to_drop if c in df.columns]

X = df.drop(columns=columns_to_drop)
print("Feature matrix shape after dropping non-useful columns:", X.shape)

# 3. TRAIN / TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train shape:", X_train.shape, "Test shape:", X_test.shape)

# 4. PREPROCESSING PIPELINE
# - Numeric features: impute median, scale
# - Categorical features: impute most frequent
# - Addon columns are already numeric (0/1), so they go through numeric pipeline

categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numeric_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

print("Number of numeric features:", len(numeric_cols))
print("Number of categorical features:", len(categorical_cols))

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols),
    ]
)

# 5. DEFINE MODELS

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    )
}

# 6. BASELINE MODEL (MEAN PREDICTOR)

baseline_pred = np.full_like(y_test, fill_value=y_train.mean(), dtype=float)
baseline_r2 = r2_score(y_test, baseline_pred)
baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
baseline_mae = mean_absolute_error(y_test, baseline_pred)

print("\n=== Baseline (predict mean price) ===")
print(f"R2:   {baseline_r2:.4f}")
print(f"RMSE: {baseline_rmse:.2f}")
print(f"MAE:  {baseline_mae:.2f}")

# 7. TRAIN & EVALUATE EACH MODEL

results = {}
fitted_pipelines = {}

for name, model in models.items():
    print(f"\n=== Training model: {name} ===")
    pipe = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)

    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)

    results[name] = {"R2": r2, "RMSE": rmse, "MAE": mae}
    fitted_pipelines[name] = pipe

    print(f"{name} - R2: {r2:.4f}, RMSE: {rmse:.2f}, MAE: {mae:.2f}")

# 8. COMPARE MODELS

print("\n=== Model comparison (higher R2 is better, lower RMSE/MAE is better) ===")
for name, m in results.items():
    print(
        f"{name:18s} | R2 = {m['R2']:.4f} | RMSE = {m['RMSE']:.2f} | MAE = {m['MAE']:.2f}"
    )

# 9. SAVE BEST MODEL

# Choose best by lowest RMSE
best_model_name = min(results.keys(), key=lambda k: results[k]["RMSE"])
best_pipeline = fitted_pipelines[best_model_name]

print(f"\nBest model by RMSE: {best_model_name}")
joblib.dump(best_pipeline, "../../models/best_model.pkl")
