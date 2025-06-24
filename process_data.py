import pandas as pd
import os

data_dir = "data"
files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

all_data = []

for file in files:
    df = pd.read_csv(os.path.join(data_dir, file))
    df = df[df["product"] == "pink morsel"].copy()

    # Use raw string to avoid regex warning
    df["price"] = df["price"].replace(r'[\$,]', '', regex=True).astype(float)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df["sales"] = df["price"] * df["quantity"]
    df = df[["date", "region", "sales"]]
    all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)
final_df["date"] = pd.to_datetime(final_df["date"])
final_df["sales"] = final_df["sales"].round(2)

# Clean up existing file if needed
if os.path.exists("processed_sales_data.csv"):
    os.remove("processed_sales_data.csv")

final_df.to_csv("processed_sales_data.csv", index=False)
print("Processed data saved to 'processed_sales_data.csv'")
