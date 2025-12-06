import pandas as pd

df = pd.read_csv(
    "auto24_data(3rd batch).csv",
    engine="python",
    on_bad_lines="skip"
)

print("Usable rows in 2nd batch:", len(df))
