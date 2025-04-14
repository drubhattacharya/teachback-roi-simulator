
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image

# Load logo
logo = Image.open("canopy_logo.png")

st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=100)
with col2:
    st.title("Canopy Teach-Back ROI Simulator")
    st.markdown("This simulator models physician uptake and projected cost savings from the Canopy Teach-Back program.")

# User Inputs
st.sidebar.header("Manual Inputs")
monthly_minutes = st.sidebar.number_input("Avg total monthly minutes", value=24000)
minutes_per_call = st.sidebar.number_input("Minutes per call", value=13)
avg_calls = st.sidebar.number_input("Avg # calls", value=1846)
estimated_lep_pts = st.sidebar.number_input("Estimated # LEP pts", value=308)
rate_per_min = st.sidebar.number_input("Rate per minutes per call", value=0.75)
expected_readmits = st.sidebar.number_input("Expected LEP Readmissions", value=55)
actual_readmits = st.sidebar.number_input("Actual LEP Readmissions", value=41)
cost_per_stay = st.sidebar.number_input("Median cost per inpatient stay for LEP patients", value=11086)

# Calculations
teachback_reduction = estimated_lep_pts
monthly_call_savings = int(minutes_per_call * teachback_reduction * rate_per_min)
annual_call_savings = monthly_call_savings * 12
averted_readmits = expected_readmits - actual_readmits
monthly_readmit_savings = int(averted_readmits * cost_per_stay)
monthly_total_savings = monthly_call_savings + monthly_readmit_savings
annual_total_savings = monthly_total_savings * 12

# Display Outputs
st.subheader(f"Annual Hospital Savings: ${annual_total_savings:,}")
st.write(f"**Monthly Call Savings:** ${monthly_call_savings:,}")
st.write(f"**Annual Call Savings:** ${annual_call_savings:,}")
st.write(f"**Monthly Readmission Savings:** ${monthly_readmit_savings:,}")
st.write(f"**Monthly Total Savings:** ${monthly_total_savings:,}")

# Progress Simulation
months = list(range(1, 13))
uptake_percent = np.linspace(10, 95, 12)
monthly_savings_progress = (uptake_percent / 95) * monthly_total_savings
cumulative_savings = np.cumsum(monthly_savings_progress)

# Custom formatter
def format_dollar_ticks(x, pos):
    if x >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    elif x >= 1000:
        return f"{int(x/1000)}K"
    else:
        return str(int(x))

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(months, monthly_savings_progress, marker='o', label="Monthly Savings ($)", color="green")
ax1.plot(months, cumulative_savings, marker='s', label="Cumulative Savings ($)", color="blue")
ax1.set_xlabel("Month")
ax1.set_ylabel("Savings ($)")
ax1.set_title("Canopy Teach-Back: Monthly and Cumulative Savings")
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(format_dollar_ticks))

ax2 = ax1.twinx()
ax2.plot(months, uptake_percent, linestyle='--', color='orange', label="Teach-Back Uptake (%)")
ax2.set_ylabel("Uptake (%)")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

st.pyplot(fig)
