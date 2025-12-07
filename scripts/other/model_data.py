import pandas as pd

def main():
    df = pd.read_csv("../../data/processed/auto24_cleaned.csv", low_memory=False)
    print("Original cleaned dataset:", df.shape)

    # Drop junk columns like Unnamed: xxx if they still exist
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    print("After dropping 'Unnamed' columns:", df.shape)

    # ---- Make sure target exists ----
    if "price" not in df.columns:
        raise ValueError("Column 'price' not found in auto24_cleaned.csv")

    # ---- Identify addon (equipment) columns ----
    addon_cols = []
    cols = list(df.columns)
    if "abs pidurid" in df.columns and "12v pistikupesad" in df.columns and "Liik" in df.columns:
        start = cols.index("abs pidurid")
        end = cols.index("Liik")  # Liik is the first column after the addons block
        addon_cols = cols[start:end]
    print(f"Number of addon columns: {len(addon_cols)}")

    high_level_cat = [
        "Mark",
        "Mudel",
        "Liik",
        "Keretüüp",
        "Kütus",
        "Vedav sild",
        "Käigukast",
        "Värvus",
    ]

    engineered_num = [
        "mileage_km",
        "reg_year",
        "engine_l",
        "power_kw",
        "seats",
        "doors",
        "num_addons",
        "car_age",
    ]

    # ---- Extra physical / technical numeric columns (kept as features) ----
    # These will still be strings (e.g. '5370 mm', '2188 kg'), but the model
    # can still learn some patterns via one-hot encoding for now.
    extra_numeric_like = [
        "pikkus",
        "laius",
        "kõrgus",
        "tühimass",
        "täismass",
        "kandevõime",
        "piduriga haagis",
        "pidurita haagis",
        "teljevahe",
        "CO2 (NEDC)",
        "CO2 (WLTP)",
        "kütusepaak",
        "kiirendus 0-100 km/h",
    ]

    # ---- keep list (no leakage columns) ----
    leakage_or_unwanted = [
        "Link",
        "Täisnimi",
        "Hind",
        "Läbisõidumõõdiku näit",
        "Esmane reg",
        "Mootor",
        "price_per_km",
        "price_per_kw",
        "log_price",
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
        "Osta Kohe hind",
    ]

    # Start building keep_cols
    keep_cols = ["price"]  # target stays inside, will be separated later

    # Add blocks
    keep_cols += addon_cols
    keep_cols += high_level_cat
    keep_cols += engineered_num
    keep_cols += extra_numeric_like

    # Make unique & only existing columns
    keep_cols = list(dict.fromkeys(keep_cols))  # preserve order, drop duplicates
    keep_cols = [c for c in keep_cols if c in df.columns and c not in leakage_or_unwanted]

    print("Number of columns kept for model:", len(keep_cols))
    print("Some of them:", keep_cols[:25])

    model_df = df[keep_cols].copy()

    # For safety, drop rows where critical numeric features are missing
    essential_for_training = ["price", "mileage_km", "reg_year", "engine_l", "power_kw"]
    existing_essentials = [c for c in essential_for_training if c in model_df.columns]

    model_df = model_df.dropna(subset=existing_essentials)
    print("Model dataset shape after dropping NaNs:", model_df.shape)

    # ---- Save ----
    model_df.to_csv("auto24_model_data.csv", index=False)
    print("Saved model dataset as auto24_model_data.csv")

if __name__ == "__main__":
    main()
