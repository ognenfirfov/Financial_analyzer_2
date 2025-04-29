
import pandas as pd

def analyze_trends(df):
    df = df.copy()
    df = df.sort_values("Year")
    df["Revenue YoY %"] = df["Revenue"].pct_change() * 100
    df["Net Profit YoY %"] = df["Net Profit"].pct_change() * 100
    df["EBITDA YoY %"] = df["EBITDA"].pct_change() * 100
    return df
