import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Sample data extracted from the CRF Vacancy Control Dashboards
data = {
    "Facility": [
        "Icahn House", "House East", "Hope House", "Kenilworth", 
        "Park Overlook Stabilization", "Ellington", "Apollo", "Lenox",
        "Light House", "Comfort Inn", "Best Western", "Park West", "Belnord"
    ],
    "Total Units": [65, 192, 51, 200, 91, 83, 43, 41, 240, 101, 101, 113, 130],
    "Available Units": [3, 1, 5, 0, 1, 4, 2, 0, 22, 1, 2, 4, 0],
    "Reserved Units": [0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "Units in Maintenance": [0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 1, 0, 0],
    "Units Under Repair": [2, 1, 2, 2, 0, 1, 1, 0, 0, 3, 0, 2, 0],
    "Units in Long-Term Repair": [1, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
    "Units Offline": [10, 8, 8, 2, 1, 5, 3, 0, 31, 6, 8, 8, 0],
    "Occupancy Rate (%)": [85, 96, 84, 99, 99, 94, 93, 100, 87, 94, 92, 93, 100],
    "Cribs": [10, 20, 5, 15, 7, 9, 4, 2, 12, 6, 10, 8, 5],
    "Days Offline": [5, 8, 10, 12, 2, 14, 7, 5, 25, 6, 12, 10, 0],
    "Status": ["Under Repair", "Maintenance", "Available", "Maintenance", "Repair", "Repair", "Repair", "Available", "Maintenance", "Repair", "Available", "Maintenance", "Available"],
    "Details (Repairs Needed)": ["Plumbing", "Electrical", "Ready", "HVAC", "Roof", "Extermination", "Flooring", "Paint", "Renovation", "Fumigation", "Ready", "Structural", "Ready"],
    "Expected Date": ["2024-09-20", "2024-09-18", "N/A", "2024-09-22", "2024-09-25", "2024-09-30", "2024-09-23", "N/A", "2024-09-30", "2024-09-26", "N/A", "2024-09-30", "N/A"],
    "Time of Turnover": ["5:00 PM", "3:00 PM", "N/A", "4:00 PM", "2:00 PM", "5:00 PM", "12:00 PM", "N/A", "1:00 PM", "5:00 PM", "N/A", "6:00 PM", "N/A"]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Add an Efficiency Metric: Occupied Units / Total Units * 100
df['Occupancy Efficiency (%)'] = (df["Total Units"] - df["Units Offline"]) / df["Total Units"] * 100

# Streamlit App Title
st.title("CRF Vacancy Control Dashboard with Metric Comparison")

# Updated Plotly Comparison Chart
def plot_comparison_chart(metrics):
    df_melted = df.melt(id_vars="Facility", value_vars=metrics, var_name="Metric", value_name="Value")
    fig = px.bar(df_melted, x="Facility", y="Value", color="Metric",
                 title="Comparison of Metrics", barmode="stack", text_auto='.2s')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

# Multiselect for choosing metrics to compare
st.subheader("Choose Metrics to Compare")
metrics = st.multiselect(
    "Select Metrics for Comparison",
    options=df.columns.drop("Facility"),  # Exclude Facility column
    default=["Occupancy Rate (%)", "Units Offline"]  # Preselect common metrics
)

# Display comparison chart
if metrics:
    plot_comparison_chart(metrics)

# Sleeker Occupancy Rate Overview (Matplotlib)
st.subheader("1. Occupancy Rate Overview")
fig, ax = plt.subplots()
df.set_index("Facility")["Occupancy Rate (%)"].plot(kind="barh", color="#1f77b4", ax=ax)
plt.title("Occupancy Rate by Facility")
plt.xlabel("Occupancy Rate (%)")
plt.ylabel("Facility")
plt.xlim(0, 100)
for index, value in enumerate(df["Occupancy Rate (%)"]):
    plt.text(value + 1, index, f"{value}%", va='center')
st.pyplot(fig)
st.write(df[["Facility", "Occupancy Rate (%)"]])

# Chart: Days Offline and Status (Matplotlib)
st.subheader("2. Days Offline and Unit Status")
fig, ax = plt.subplots()
df.set_index("Facility")[["Days Offline", "Units Offline"]].plot(kind="bar", stacked=True, color=['#ff7f0e', '#2ca02c'], ax=ax)
plt.title("Days Offline vs Units Offline")
plt.ylabel("Days/Units")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)
st.write(df[["Facility", "Days Offline", "Status", "Details (Repairs Needed)", "Expected Date", "Time of Turnover"]])

# Facility Performance Comparison (Matplotlib)
st.subheader("3. Facility Performance Comparison")
fig, ax = plt.subplots()
df.set_index("Facility")[["Occupancy Rate (%)", "Units Offline", "Units Under Repair"]].plot(kind="bar", ax=ax)
plt.title("Facility Performance Comparison")
plt.ylabel("Metrics")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)
st.write(df[["Facility", "Occupancy Rate (%)", "Units Offline", "Units Under Repair", "Days Offline"]])

# Efficiency Metric: Occupied Units vs Available Units (Occupancy Efficiency - Matplotlib)
st.subheader("4. Occupancy Efficiency Metric")
fig, ax = plt.subplots()
df.set_index("Facility")["Occupancy Efficiency (%)"].plot(kind="barh", color="#d62728", ax=ax)
plt.title("Occupancy Efficiency by Facility")
plt.xlabel("Occupancy Efficiency (%)")
plt.ylabel("Facility")
plt.xlim(0, 100)
for index, value in enumerate(df["Occupancy Efficiency (%)"]):
    plt.text(value + 1, index, f"{value:.1f}%", va='center')
st.pyplot(fig)
st.write(df[["Facility", "Occupancy Efficiency (%)", "Cribs", "Days Offline"]])

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
