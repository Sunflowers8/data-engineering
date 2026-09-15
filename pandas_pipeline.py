import pandas as pd

df = pd.read_csv("employees.csv")
filtered_df = df[(df['department'] == 'Data')
                 & (df['salary'] > 40000)]
print(filtered_df)