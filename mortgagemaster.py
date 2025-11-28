import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="MortgageMaster (Python)",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def generate_pdf(df, currency_symbol, monthly_pmt, total_int, total_cost):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Mortgage Amortization Schedule", styles['Title']))
    elements.append(Spacer(1, 12))

    summary_data = [
        [f"Monthly Payment: {currency_symbol}{monthly_pmt:,.2f}"],
        [f"Total Interest: {currency_symbol}{total_int:,.2f}"],
        [f"Total Cost of Loan: {currency_symbol}{total_cost:,.2f}"]
    ]

    summary_table = Table(summary_data, hAlign='LEFT')
    summary_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    table_data = [['Month', 'Principal', 'Interest', 'Total Interest', 'Balance']]
    
    for index, row in df.iterrows():
        table_data.append([
            str(row['Month']),
            f"{currency_symbol}{row['Principal Payment']:,.2f}",
            f"{currency_symbol}{row['Interest Payment']:,.2f}",
            f"{currency_symbol}{row['Total Interest']:,.2f}",
            f"{currency_symbol}{row['Remaining Balance']:,.2f}"
        ])

    t = Table(table_data)
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer

st.title("🏠 MortgageMaster Calculator")
st.markdown("Calculate your monthly payments and view your amortization schedule.")

col_inputs, col_results = st.columns([1, 2], gap="large")

with col_inputs:
    st.subheader("Settings")
    
    currency_options = {
        "USD ($)": "$",
        "EUR (€)": "€",
        "GBP (£)": "£",
        "INR (₹)": "₹",
        "JPY (¥)": "¥"
    }
    selected_curr_label = st.selectbox("Select Currency", list(currency_options.keys()))
    currency = currency_options[selected_curr_label]

    st.subheader("Loan Details")
    
    home_price = st.number_input(f"Home Price ({currency})", min_value=0, value=350000, step=1000)
    
    col_dp1, col_dp2 = st.columns(2)
    with col_dp1:
        down_payment = st.number_input(f"Down Payment ({currency})", min_value=0, value=70000, step=1000)
    with col_dp2:
        dp_percent = (down_payment / home_price * 100) if home_price > 0 else 0
        st.info(f"{dp_percent:.1f}%")

    col_term1, col_term2 = st.columns(2)
    with col_term1:
        loan_term = st.number_input("Loan Term (Years)", min_value=1, max_value=50, value=30)
    with col_term2:
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=6.5, step=0.1, format="%.2f")

    st.subheader("Taxes & Fees")
    property_tax_annual = st.number_input(f"Property Tax (Annual {currency})", min_value=0, value=3500, step=50)
    home_insurance_annual = st.number_input(f"Home Insurance (Annual {currency})", min_value=0, value=1200, step=50)
    hoa_fees_monthly = st.number_input(f"HOA Fees (Monthly {currency})", min_value=0, value=0, step=10)

principal = home_price - down_payment
monthly_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12

if interest_rate == 0:
    monthly_pi = principal / number_of_payments
else:
    monthly_pi = (principal * monthly_rate * ((1 + monthly_rate) ** number_of_payments)) / \
                 (((1 + monthly_rate) ** number_of_payments) - 1)

monthly_tax = property_tax_annual / 12
monthly_insurance = home_insurance_annual / 12
total_monthly_payment = monthly_pi + monthly_tax + monthly_insurance + hoa_fees_monthly

schedule = []
remaining_balance = principal
total_interest_paid = 0

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_rate
    principal_payment = monthly_pi - interest_payment
    remaining_balance -= principal_payment
    total_interest_paid += interest_payment
    
    if remaining_balance < 0:
        remaining_balance = 0

    schedule.append({
        "Month": i,
        "Principal Payment": principal_payment,
        "Interest Payment": interest_payment,
        "Total Interest": total_interest_paid,
        "Remaining Balance": remaining_balance
    })

df_schedule = pd.DataFrame(schedule)

with col_results:
    st.subheader("Estimated Monthly Payment")
    
    st.markdown(f"<h1 style='color: #2563eb; font-size: 48px;'>{currency}{total_monthly_payment:,.2f}</h1>", unsafe_allow_html=True)
    
    chart_data = pd.DataFrame({
        'Category': ['Principal & Interest', 'Property Tax', 'Home Insurance', 'HOA Fees'],
        'Value': [monthly_pi, monthly_tax, monthly_insurance, hoa_fees_monthly]
    })

    base = alt.Chart(chart_data).encode(
        theta=alt.Theta("Value", stack=True)
    )
    
    pie = base.mark_arc(outerRadius=120, innerRadius=80).encode(
        color=alt.Color("Category"),
        order=alt.Order("Value", sort="descending"),
        tooltip=["Category", alt.Tooltip("Value", format=",.2f")]
    )
    
    text = base.mark_text(radius=140).encode(
        text=alt.Text("Value", format=",.0f"),
        order=alt.Order("Value", sort="descending"),
        color=alt.value("black") 
    )
    
    st.altair_chart(pie + text, use_container_width=True)

    col_sum1, col_sum2, col_sum3 = st.columns(3)
    col_sum1.metric("Loan Amount", f"{currency}{principal:,.0f}")
    col_sum2.metric("Total Interest", f"{currency}{total_interest_paid:,.0f}")
    col_sum3.metric("Total Cost", f"{currency}{principal + total_interest_paid:,.0f}")

st.divider()
st.subheader("Amortization Schedule")

with st.expander("View Full Schedule Table"):
    st.dataframe(
        df_schedule.style.format({
            "Principal Payment": f"{currency}{{:,.2f}}",
            "Interest Payment": f"{currency}{{:,.2f}}",
            "Total Interest": f"{currency}{{:,.2f}}",
            "Remaining Balance": f"{currency}{{:,.2f}}"
        }),
        use_container_width=True
    )

col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    csv = df_schedule.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Schedule as CSV",
        data=csv,
        file_name='amortization_schedule.csv',
        mime='text/csv',
        use_container_width=True
    )

with col_dl2:
    if st.button("Generate PDF Report", use_container_width=True):
        pdf_file = generate_pdf(
            df_schedule, 
            currency, 
            total_monthly_payment, 
            total_interest_paid, 
            principal + total_interest_paid
        )
        st.download_button(
            label="Download PDF Ready - Click to Save",
            data=pdf_file,
            file_name='amortization_schedule.pdf',
            mime='application/pdf',
            use_container_width=True
        )

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        Made by <b>Varsh Vishwakarma</b><br>
        AI • ML • DL • Data Science • Cloud • Full-Stack ML Developer
    </div>
    """,
    unsafe_allow_html=True
)
