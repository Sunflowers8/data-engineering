import pandas as pd

# Path to the raw employee dataset
input_file = "01-week-foundations/data/raw/employees.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Filter employees who:
# 1. Work in the Data department
# 2. Earn more than 40,000
filtered_df = df[
    (df["department"] == "Data")
    & (df["salary"] > 40000)
]

print("Data department employees earning more than 40,000:")
print(filtered_df)