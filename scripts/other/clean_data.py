import pandas as pd
import numpy as np
import re

# LOAD ALL BATCHES

csv_files = [
    "auto24_data(1st batch).csv",
    "auto24_data(2nd batch).csv",
    "auto24_data(3rd batch).csv",
    "auto24_data(last batch).csv",
]

dfs = []
for f in csv_files:
    print("Reading:", f)
    df_part = pd.read_csv(
        f,
        engine="python",       # more tolerant parser
        on_bad_lines="skip"    # skip rows with wrong number of columns
    )
    print(f, "shape:", df_part.shape)
    dfs.append(df_part)

df = pd.concat(dfs, ignore_index=True)

print("Rows after merge:", df.shape)

# Remove duplicate links
if "Link" in df.columns:
    df = df.drop_duplicates(subset="Link")

print("Rows after removing duplicates:", df.shape)

# HELPER FUNCTIONS

def parse_int(x):
    if pd.isna(x):
        return np.nan
    s = str(x).replace("\xa0", " ").replace(" ", "")
    nums = re.findall(r"\d+", s)
    if not nums:
        return np.nan
    return int("".join(nums))

def parse_float(x):
    if pd.isna(x):
        return np.nan
    s = str(x).replace("\xa0", " ").replace(" ", "").replace(",", ".")
    m = re.findall(r"\d+(\.\d+)?", s)
    if not m:
        return np.nan
    return float(m[0])

def parse_engine_liters(x):
    cm3 = parse_int(x)
    if pd.isna(cm3):
        return np.nan
    return cm3 / 1000.0

# CLEAN KEY NUMERIC FIELDS


df["price"] = df["Hind"].apply(parse_int)
df["mileage_km"] = df["Läbisõidumõõdiku näit"].apply(parse_int)

# Extract year from "Esmane reg"
df["reg_year"] = (
    df["Esmane reg"].astype(str).str.extract(r"(\d{4})").astype(float)
)

df["engine_l"] = df["mootori maht"].apply(parse_engine_liters)
df["power_kw"] = df["võimsus"].apply(parse_int)

if "istekohti" in df.columns:
    df["seats"] = df["istekohti"].apply(parse_int)

if "uste arv" in df.columns:
    df["doors"] = df["uste arv"].apply(parse_int)

print("=== DEBUG: BEFORE FILTERING ===")
print("Total rows before filtering:", df.shape[0])

print("Missing price:", df["price"].isna().sum())
print("Missing mileage_km:", df["mileage_km"].isna().sum())
print("Missing reg_year:", df["reg_year"].isna().sum())

print("Price min/max:", df["price"].min(), df["price"].max())
print("Mileage min/max:", df["mileage_km"].min(), df["mileage_km"].max())
print("Year min/max:", df["reg_year"].min(), df["reg_year"].max())

# FILTER BROKEN ROWS


before = df.shape[0]

df = df[
    df["price"].notna() &
    df["mileage_km"].notna() &
    df["reg_year"].notna()
]

df = df[(df["reg_year"] >= 1990) & (df["reg_year"] <= 2025)]
df = df[(df["mileage_km"] >= 0) & (df["mileage_km"] <= 800000)]
df = df[(df["price"] >= 300) & (df["price"] <= 300000)]

after = df.shape[0]

print(f"Removed {before - after} invalid rows.")
print("Remaining rows:", after)

# ADDON PROCESSING

#Identify addon columns
col_list = list(df.columns)
start_idx = col_list.index("abs pidurid")
end_idx = col_list.index("Liik")
addon_cols = col_list[start_idx:end_idx]

numeric_addon_candidates = [
    "turvapadi", "elektriliselt reguleeritavad istmed",
    "õhuga reguleeritav iste", "istmesoojendused",
    "elektrilised akende tõstukid", "peeglid päikesesirmides",
    "rulookardinad ustel", "12v pistikupesad"
]

numeric_addon_cols = [c for c in addon_cols if c in numeric_addon_candidates]
binary_addon_cols = [c for c in addon_cols if c not in numeric_addon_candidates]

# binary addons: presence = 1
for c in binary_addon_cols:
    df[c] = df[c].notna().astype(int)

# numeric addons
for c in numeric_addon_cols:
    df[c] = df[c].apply(parse_int).fillna(0).astype(int)

# total addons
df["num_addons"] = (
    df[binary_addon_cols].sum(axis=1) +
    df[numeric_addon_cols].sum(axis=1)
)

# FEATURE ENGINEERING


CURRENT_YEAR = 2025
df["car_age"] = CURRENT_YEAR - df["reg_year"]
df.loc[df["car_age"] < 0, "car_age"] = np.nan

df["price_per_km"] = df["price"] / df["mileage_km"].replace({0: np.nan})
df["price_per_kw"] = df["price"] / df["power_kw"].replace({0: np.nan})
df["log_price"] = np.log1p(df["price"])

# SAVE

df.to_csv("auto24_cleaned.csv", index=False)
print("Saved cleaned dataset as auto24_cleaned.csv")