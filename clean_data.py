import pandas as pd
import numpy as np

df = pd.read_csv("ebay_tech_deals.csv", dtype=str)

df["price"] = df["price"].str.replace("US $", "", regex=False)
df["price"] = df["price"].str.replace(",", "", regex=False)
df["price"] = df["price"].str.strip()

df["original_price"] = df["original_price"].str.replace("US $", "", regex=False)
df["original_price"] = df["original_price"].str.replace(",", "", regex=False)
df["original_price"] = df["original_price"].str.strip()

df["original_price"] = df["original_price"].replace(["N/A", "", np.nan], df["price"])

df["shipping"] = df["shipping"].replace(["N/A", "", np.nan], "Shipping info unavailable")
df["shipping"] = df["shipping"].apply(lambda x: "Shipping info unavailable" if isinstance(x, str) and x.strip() == "" else x)

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce")

df["discount_percentage"] = ((df["original_price"] - df["price"]) / df["original_price"]) * 100
df["discount_percentage"] = df["discount_percentage"].round(2)

df.to_csv("cleaned_ebay_deals.csv", index=False)

