import pandas as pd
import glob
import os

# Step 1: Read all CSV files from the data/ folder
data_path = 'data/'
all_files = glob.glob(os.path.join(data_path, 'daily_sales_data_*.csv'))

# Step 2: List to store DataFrames
df_list = []

for file in all_files:
    df = pd.read_csv(file)

    # Step 3: Filter only "Pink Morsel" product
    df = df[df['product'] == 'pink morsel']

    # Step 4: Calculate sales = quantity * price
    df['sales'] = df['quantity'] * df['price']

    # Step 5: Select only relevant columns
    df = df[['sales', 'date', 'region']]

    # Step 6: Add to list
    df_list.append(df)

# Step 7: Concatenate all dataframes
final_df = pd.concat(df_list, ignore_index=True)

# Step 8: Save to CSV
final_df.to_csv('processed_sales_data.csv', index=False)

print("✅ Data processed and saved to 'processed_sales_data.csv'")
