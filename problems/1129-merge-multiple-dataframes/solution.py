import pandas as pd

def solution(df1, df2, df3):
    inner = pd.merge(df1, df2, on='emp_id', how='inner').reset_index(drop=True)
    result = pd.merge(inner, df3, on='emp_id', how='left').reset_index(drop=True)
    return result