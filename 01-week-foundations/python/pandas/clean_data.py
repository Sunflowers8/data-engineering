import pandas as pd

# File paths
input_file = "01-week-foundations/data/raw/employees_dirty.csv"
output_file = "01-week-foundations/data/processed/employees_cleaned.csv"

# Extract: Read the dirty employee dataset
df = pd.read_csv(input_file)

# Transform: Handle missing values

# Fill missing age with the average age
average_age = df["age"].mean()
df["age"] = df["age"].fillna(average_age)

# Fill missing department with "Unknown"
df["department"] = df["department"].fillna("Unknown")

# Fill missing salary with the average salary
average_salary = df["salary"].mean()
df["salary"] = df["salary"].fillna(average_salary)

# Load: Save the cleaned dataset
df.to_csv(output_file, index=False)

print("Data cleaning completed.")
print(df)

