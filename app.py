
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO
from analyzer import analyze_trends
from extractor import extract_financials
from utils import generate_excel, generate_commentary

st.set_page_config(page_title="Financial Report Analyzer", layout="wide")
st.title("📊 Financial Report Analyzer")

uploaded_files = st.file_uploader("Upload one or more annual financial report PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    records = []
    for file in uploaded_files:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
            data = extract_financials(text)
            if data:
                year = re.search(r"20\d{2}", file.name)
                data['Year'] = year.group(0) if year else "Unknown"
                records.append(data)

    if records:
        df = pd.DataFrame(records).sort_values("Year")
        trends = analyze_trends(df)
        commentary = generate_commentary(trends)

        st.subheader("📈 Extracted Financial Data")
        st.dataframe(df)

        st.subheader("📊 Trends")
        st.dataframe(trends)

        st.subheader("📉 Revenue and Net Profit Over Time")
        fig, ax = plt.subplots()
        df.plot(x="Year", y=["Revenue", "Net Profit"], marker='o', ax=ax)
        st.pyplot(fig)

        st.subheader("📝 Narrative Analysis")
        st.write(commentary)

        st.subheader("📤 Download Summary Report")
        excel_file = generate_excel(df, trends, commentary)
        st.download_button("Download Excel Report", data=excel_file, file_name="financial_summary.xlsx")
    else:
        st.warning("No recognizable financial data found in the uploaded files.")
else:
    st.info("Please upload one or more PDF financial reports to begin.")
