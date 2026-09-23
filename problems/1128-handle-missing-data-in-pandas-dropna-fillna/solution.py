import pandas as pd

def solution(df):
    df = df.copy()

    keep_cols = [c for c in df.columns if df[c].isna().mean() <= 0.5]
    df = df[keep_cols]

    df = df[df.isna().mean(axis=1) <= 0.5]

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())
        else:
            df[col] = df[col].fillna(df[col].mode().iloc[0])

    return df.reset_index(drop=True)