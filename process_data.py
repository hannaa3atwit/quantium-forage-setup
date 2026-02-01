import pandas as pd

# Load CSV files from the data folder
df1 = pd.read_csv("data/file1.csv")
df2 = pd.read_csv("data/file2.csv")
df3 = pd.read_csv("data/file3.csv")

# Combine all data
df = pd.concat([df1, df2, df3])

# Keep only Pink Morsels
df = df[df["product"] == "Pink Morsels"]

# Calculate total sales
df["Sales"] = df["quantity"] * df["price"]

# Select required fields
output = df[["Sales", "date", "region"]]

# Write formatted output
output.to_csv("output.csv", index=False)
