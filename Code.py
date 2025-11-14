import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF


#Connect to Oracle & Fetch Data

username = ""
password = ""
dsn = ""  

# Connect to Oracle
conn = cx_Oracle.connect(user=username, password=password, dsn=dsn)


query = "SELECT CASE_NUM, OCCURED_COUNTRY_DESC, FLAG_SERIOUS FROM c_identification WHERE ROWNUM <= 50000;"


df = pd.read_sql(query, conn)
conn.close()


#Generate Chart
def generate_chart(df):
    country_counts = df['OCCURED_COUNTRY_DESC'].value_counts()

    plt.figure(figsize=(12, 6))
    country_counts.plot(kind='bar', color='skyblue')
    plt.title("Cases per Country")
    plt.xlabel("Country")
    plt.ylabel("Number of Cases")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("cases_chart.png", bbox_inches='tight')
    plt.close()

generate_chart(df)


#Generate PDF Report

def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "RxLogix - Cases Report", ln=True, align="C")
    pdf.ln(10)

    # Subheading
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, "This report contains the cases from the Oracle database, along with a chart summarizing cases per country.")
    pdf.ln(10)

    # Insert chart
    pdf.image("cases_chart.png", x=20, w=170)
    pdf.ln(10)

    # Insert table
    pdf.set_font("Arial", "B", 12)
    col_width = pdf.w / (len(df.columns) + 1)

    # Table header
    for col in df.columns:
        pdf.cell(col_width, 10, str(col), border=1, align='C')
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    # Table rows
    for index, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, 8, str(item), border=1, align='C')
        pdf.ln()

    # Footer
    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Generated automatically using Python", ln=True, align="C")

    pdf.output("Cases_Report.pdf")

generate_pdf(df)

print("PDF Report Generated Successfully!")
