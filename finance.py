import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Financial Calculations
def calculate_financials(revenue, cogs, operating_expenses, tax_rate):
    """Calculates basic financials and returns a dictionary."""
    gross_profit = revenue - cogs
    operating_income = gross_profit - operating_expenses
    net_income = operating_income * (1 - tax_rate)
    return {
        "Revenue": revenue,
        "Cost of Goods Sold (COGS)": cogs,
        "Gross Profit": gross_profit,
        "Operating Expenses": operating_expenses,
        "Operating Income": operating_income,
        "Net Income": net_income,
        "Tax Rate (%)": tax_rate * 100,
    }

def generate_cash_flow_statement(financials, depreciation, capex, working_capital_change):
    """Generates a simple cash flow statement."""
    operating_cash_flow = financials["Net Income"] + depreciation - working_capital_change
    investing_cash_flow = -capex
    total_cash_flow = operating_cash_flow + investing_cash_flow
    return {
        "Operating Cash Flow": operating_cash_flow,
        "Investing Cash Flow": investing_cash_flow,
        "Total Cash Flow": total_cash_flow,
    }

def calculate_dcf(cash_flows, discount_rate, terminal_growth_rate):
    """Calculates the discounted cash flow (DCF) value."""
    years = len(cash_flows)
    discounted_cash_flows = [
        cf / ((1 + discount_rate) ** year) for year, cf in enumerate(cash_flows, start=1)
    ]
    terminal_value = cash_flows[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)
    dcf_value = sum(discounted_cash_flows) + discounted_terminal_value
    return dcf_value

# Streamlit Interface
st.title("Comprehensive Financial Modeling Tool")
st.sidebar.header("Input Parameters")

# Inputs for Financial Statements
revenue = st.sidebar.number_input("Revenue", value=500000.0, step=10000.0)
cogs = st.sidebar.number_input("Cost of Goods Sold (COGS)", value=300000.0, step=10000.0)
operating_expenses = st.sidebar.number_input("Operating Expenses", value=100000.0, step=5000.0)
tax_rate = st.sidebar.slider("Tax Rate (%)", 0.0, 50.0, 20.0) / 100

# Additional Inputs
depreciation = st.sidebar.number_input("Depreciation", value=20000.0, step=1000.0)
capex = st.sidebar.number_input("Capital Expenditures (CAPEX)", value=30000.0, step=1000.0)
working_capital_change = st.sidebar.number_input("Change in Working Capital", value=5000.0, step=1000.0)

# Generate Financial Statements
financials = calculate_financials(revenue, cogs, operating_expenses, tax_rate)
cash_flows = generate_cash_flow_statement(financials, depreciation, capex, working_capital_change)

# Display Financial Statements
st.header("Generated Financial Statements")
st.subheader("Income Statement")
st.write(financials)

st.subheader("Cash Flow Statement")
st.write(cash_flows)

# DCF Inputs
st.sidebar.header("DCF Valuation Inputs")
cash_flow_forecast = st.sidebar.text_area("Enter Cash Flow Forecast (comma-separated)", "100000, 110000, 121000, 133100")
discount_rate = st.sidebar.slider("Discount Rate (%)", 0.0, 20.0, 10.0) / 100
terminal_growth_rate = st.sidebar.slider("Terminal Growth Rate (%)", 0.0, 5.0, 2.0) / 100

if st.sidebar.button("Calculate DCF"):
    cash_flow_forecast = list(map(float, cash_flow_forecast.split(',')))
    dcf_value = calculate_dcf(cash_flow_forecast, discount_rate, terminal_growth_rate)
    st.subheader("DCF Valuation")
    st.write(f"**DCF Value:** ${dcf_value:,.2f}")

# Sensitivity Analysis
st.sidebar.header("Sensitivity Analysis")
sensitivity_metric = st.sidebar.selectbox("Sensitivity Metric", ["Discount Rate", "Growth Rate"])
if sensitivity_metric == "Discount Rate":
    rates = np.arange(0.05, 0.20, 0.01)
    dcf_values = [calculate_dcf(cash_flow_forecast, rate, terminal_growth_rate) for rate in rates]
    plt.plot(rates * 100, dcf_values)
    plt.xlabel("Discount Rate (%)")
    plt.ylabel("DCF Value ($)")
    plt.title("DCF Sensitivity to Discount Rate")
    st.pyplot(plt)

elif sensitivity_metric == "Growth Rate":
    growth_rates = np.arange(0.01, 0.05, 0.005)
    dcf_values = [calculate_dcf(cash_flow_forecast, discount_rate, rate) for rate in growth_rates]
    plt.plot(growth_rates * 100, dcf_values)
    plt.xlabel("Growth Rate (%)")
    plt.ylabel("DCF Value ($)")
    plt.title("DCF Sensitivity to Growth Rate")
    st.pyplot(plt)

# Export to Excel
if st.sidebar.button("Export to Excel"):
    data = pd.DataFrame([financials, cash_flows])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        data.to_excel(writer, index=False, sheet_name="Financial Data")
    st.download_button(
        label="Download Excel File",
        data=buffer,
        file_name="financial_model.xlsx",
        mime="application/vnd.ms-excel",
    )

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using [Streamlit](https://streamlit.io/).")
