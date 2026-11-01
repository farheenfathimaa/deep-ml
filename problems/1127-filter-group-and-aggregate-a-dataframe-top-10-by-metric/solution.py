import pandas as pd

def solution(df):
    filtered = df[df['status'] == 'completed']
    grouped = filtered.groupby('region', as_index=False)['amount'].sum()
    result = grouped.sort_values('amount',ascending=False).reset_index(drop=True)
    return result.head(10)
