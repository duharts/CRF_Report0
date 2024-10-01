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
    "Units in Maintenance": [0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 1, 0, 0],
    "Units Under Repair": [2, 1, 2, 2, 0, 1, 1, 0, 0, 3, 0, 2, 0],
    "Units in Long-Term Repair": [1, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
    "Units Offline": [10, 8, 8, 2, 1, 5, 3, 0, 31, 6, 8, 8, 0],
    "Occupancy Rate (%)": [85, 96, 84, 99, 99, 94, 93, 100, 87, 94, 92, 93, 100],
    "Cribs": [10, 20, 5, 15, 7, 9, 4, 2, 12, 6, 10, 8, 5],
    "Days Offline": [5, 8, 10, 12, 2, 14, 7, 5, 25, 6, 12, 10, 0],
    "Status": ["Under Repair", "Maintenance", "Available", "Maintenance", "Repair", "Repair", "Repair", "Available", "Maintenance", "Repair", "Available", "Maintenance", "Available"]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Add an Efficiency Metric: Occupied Units / Total Units * 100
df['Occupancy Efficiency (%)'] = (df["Total Units"] - df["Units Offline"]) / df["Total Units"] * 100

# Streamlit App Title
st.title("CRF Vacancy Control Dashboard with Business Summaries")

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
    default=["Occupancy Rate (%)", "Units Offline"]  # Preselect common metrics
)

# Display comparison chart
if metrics:
    plot_comparison_chart(metrics)

# Business Summary for Comparison Chart
st.markdown("""
**Business Summary**:  
This comparison highlights how **occupancy rates** and **offline units** differ across facilities. Facilities like **Lenox** and **Kenilworth** are highly efficient, while **Hope House** has room for improvement due to a higher number of offline units.
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
Occupancy rates across most facilities exceed 90%, showing efficient use of housing units. **Hope House**, with an occupancy rate of 84%, may need additional measures to improve usage.
""")

# Days Offline and Unit Status (Matplotlib)
st.subheader("2. Days Offline and Unit Status")
fig, ax = plt.subplots()
df.set_index("Facility")[["Days Offline", "Units Offline"]].plot(kind="bar", stacked=True, color=['#ff7f0e', '#2ca02c'], ax=ax)
plt.title("Days Offline vs Units Offline")
plt.ylabel("Days/Units")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Business Summary for Days Offline and Unit Status
st.markdown("""
**Business Summary**:  
**Light House** and **Comfort Inn** have significant downtime due to offline units, which can impact their occupancy and overall efficiency. Reducing the number of days offline could increase their performance.
""")

# Facility Performance Comparison (Clustered Bar Chart)
st.subheader("3. Facility Performance Comparison")
fig, ax = plt.subplots()
df.set_index("Facility")[["Occupancy Rate (%)", "Units Offline", "Units Under Repair"]].plot(kind="bar", ax=ax)
plt.title("Facility Performance Comparison")
plt.ylabel("Metrics")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Business Summary for Facility Performance
st.markdown("""
**Business Summary**:  
While **Kenilworth** and **Lenox** continue to excel in performance, facilities like **Hope House** and **Light House** have more offline units and repairs, reducing their overall efficiency.
""")

# Occupancy Efficiency Metric (Matplotlib)
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

# Business Summary for Occupancy Efficiency
st.markdown("""
**Business Summary**:  
**Kenilworth** and **Lenox** are running at full efficiency, while **Light House** and **Comfort Inn** need to address inefficiencies caused by offline units. Improving their occupancy efficiency could enhance overall performance.
""")

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
