
import pandas as pd

def concat_lines(df: pd.DataFrame, g1: str = 'train', g2: str = 'test'):
    if df['type'].nunique() > 1:
        df = df.sort_values('date')
        first = df[df['type'] == g2].head(1)
        first['type'] = g1
        df = pd.concat([df, first])
        df = df.sort_values('date')

    return df
