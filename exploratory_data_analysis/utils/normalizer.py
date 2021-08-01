from typing import List
import pandas as pd

def normalize(sales_df: pd.DataFrame, columns: List[str], inplace: bool = False):
    if not inplace:
        sales_df = sales_df.copy()

    mins = sales_df[columns].min()
    maxs = sales_df[columns].max()
    d = maxs - mins
    
    for col in columns:
        sales_df[col] = (sales_df[col] - mins[col]) / d[col]

    return sales_df
