import streamlit as st
import pandas as pd
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
    "Units Offline": [10, 8, 8, 2, 1, 5, 3, 0, 31, 6, 8, 8, 0],
    "Occupancy Rate (%)": [85, 96, 84, 99, 99, 94, 93, 100, 87, 94, 92, 93, 100],
    "Cribs": [10, 20, 5, 15, 7, 9, 4, 2, 12, 6, 10, 8, 5],
    "Days Offline": [5, 8, 10, 12, 2, 14, 7, 5, 25, 6, 12, 10, 0],
    "Daily Rate ($)": [227, 200, 227, 230, 210, 220, 225, 240, 250, 215, 200, 220, 235]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Add new metrics
df['Revenue Lost Due to Offline Units'] = df['Units Offline'] * df['Daily Rate ($)'] * df['Days Offline']

# Assumed average repair cost per unit
average_repair_cost = 500
df['Repair Costs ($)'] = df['Units Offline'] * average_repair_cost

# Crib Utilization Rate
df['Crib Utilization (%)'] = (df['Cribs'] / df['Total Units']) * 100

# Time to Return to Full Capacity (estimated in days)
df['Return to Full Capacity (Days)'] = df['Units Offline'] / (df['Total Units'] - df['Units Offline']) * 100

# Streamlit App Title
st.title("CRF Vacancy Control Dashboard with Enhanced Metrics")

# Display the raw data as a table
st.subheader("Facility Data Overview")
st.write(df)

# Business Summary for Table
st.markdown("""
**Business Summary**:  
The table above shows additional metrics such as **Revenue Lost Due to Offline Units**, **Repair Costs**, and **Crib Utilization**. **Hope House** and **Light House** show the highest offline unit costs, indicating the need for operational improvements.
""")

# Function to plot comparison chart
def plot_comparison_chart(metrics):
    fig, ax = plt.subplots()
    df.set_index("Facility")[metrics].plot(kind="bar", ax=ax)
    plt.title(f"Comparison of Metrics: {', '.join(metrics)}")
    plt.ylabel("Values")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

# Multiselect for choosing metrics to compare
st.subheader("Choose Metrics to Compare")
metrics = st.multiselect(
    "Select Metrics for Comparison",
    options=df.columns.drop("Facility"),  # Exclude Facility column
    default=["Occupancy Rate (%)", "Units Offline", "Revenue Lost Due to Offline Units", "Repair Costs ($)", "Crib Utilization (%)"]
)

# Display comparison chart
if metrics:
    plot_comparison_chart(metrics)

# Business Summary for Comparison Chart
st.markdown("""
**Business Summary**:  
This comparison highlights the revenue loss due to offline units and repair costs. Facilities like **Light House** and **Hope House** have significant losses that should be addressed to improve financial performance.
""")

# Occupancy Rate Overview (Matplotlib)
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

# Business Summary for Occupancy Rate
st.markdown("""
**Business Summary**:  
Occupancy rates across most facilities are efficient, with **Kenilworth** and **Park Overlook Stabilization** leading. **Hope House** shows room for improvement with an 84% occupancy rate.
""")

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
