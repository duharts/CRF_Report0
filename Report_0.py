import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Add and center the logo
logo_url = "https://th.bing.com/th/id/OIP.gEfQtRo5_UR48_2Ms_Ag8wAAAA?w=275&h=180&c=7&r=0&o=5&dpr=1.8&pid=1.7"

st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="{logo_url}" alt="Logo" width="200"/>
    </div>
    """, 
    unsafe_allow_html=True
)

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
st.title("Sample Vacancy Control Dashboard")

# Plotly Stacked Bar Chart for Comparison
def plot_comparison_chart(metrics):
    df_melted = df.melt(id_vars="Facility", value_vars=metrics, var_name="Metric", value_name="Value")
    fig = px.bar(df_melted, x="Facility", y="Value", color="Metric", barmode="stack", text_auto='.2s',
                 title="Comparison of Metrics", height=400)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

# Multiselect for choosing metrics to compare
st.subheader("Choose Metrics to Compare")
metrics = st.multiselect(
    "Select Metrics for Comparison",
    options=df.columns.drop("Facility"),  # Exclude Facility column
    default=["Occupancy Rate (%)", "Units Offline"]
)

# Display comparison chart
if metrics:
    plot_comparison_chart(metrics)

# Business Summary for Comparison Chart
st.markdown("""
**Business Summary**:  
This chart shows **occupancy rate** and **units offline** across facilities. Facilities like **Lenox** and **Kenilworth** perform optimally, while **Hope House** and **Comfort Inn** struggle with higher offline units.
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
Most facilities have an occupancy rate above 90%, showing strong utilization. **Hope House** and **Best Western** could increase occupancy to match the performance of top facilities like **Lenox**.
""")

# Days Offline and Unit Status (Matplotlib)
st.subheader("2. Days Offline and Unit Status")
fig, ax = plt.subplots()
df.set_index("Facility")[["Days Offline", "Units Offline"]].plot(kind="bar", stacked=True, color=['#ff7f0e', '#2ca02c'], ax=ax)
plt.title("Days Offline vs Units Offline")
plt.ylabel("Days/Units")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Business Summary for Days Offline and Status
st.markdown("""
**Business Summary**:  
**Light House** and **Comfort Inn** have long periods of offline units, likely due to maintenance issues. Addressing these quickly could reduce downtime and improve efficiency.
""")

# Facility Performance Comparison (Matplotlib)
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
Facilities like **Ellington** and **Apollo** show strong performance with high occupancy rates and minimal offline units, while **Light House** and **Hope House** need improvements.
""")

# Efficiency Metric (Matplotlib)
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
**Kenilworth** and **Lenox** operate at full capacity, showing 100% efficiency. However, **Light House** and **Comfort Inn** suffer from low efficiency due to offline units.
""")

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
