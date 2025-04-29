
from io import BytesIO
import pandas as pd

def generate_excel(data_df, trend_df, comments):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data_df.to_excel(writer, index=False, sheet_name='Raw Data')
        trend_df.to_excel(writer, index=False, sheet_name='Trends')
        worksheet = writer.book.add_worksheet('Comments')
        worksheet.write('A1', 'Narrative Analysis')
        worksheet.write('A2', comments)
    output.seek(0)
    return output.read()

def generate_commentary(df):
    if df.empty:
        return "No data available to generate commentary."
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else None
    if prev is not None:
        return (f"In {latest['Year']}, Deutsche Telekom's revenue grew by "
                f"{latest['Revenue YoY %']:.2f}%, while net profit changed by "
                f"{latest['Net Profit YoY %']:.2f}%. EBITDA change was "
                f"{latest['EBITDA YoY %']:.2f}%.")
    return "Only one year of data available. More years are needed for a meaningful trend analysis."
