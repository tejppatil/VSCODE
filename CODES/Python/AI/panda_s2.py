import pandas as pd
sales = {'Product': ['A', 'B', 'A', 'B'], 'Revenue': [100, 150, 200, 250]}
df_sales = pd.DataFrame(sales)

total = df_sales.groupby('Product')['Revenue'].sum()
print(total)
