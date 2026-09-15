import pandas as pd

df=pd.read_csv("employees_dirty.csv")

average_age=df["age"].mean()
df["age"] = df["age"].fillna(average_age)
df["department"] = df["department"].fillna("Unknown")
average_salary=df["salary"].mean()
df["salary"] = df["salary"].fillna(average_salary)

df.to_csv("employees_cleaned.csv", index=False)

