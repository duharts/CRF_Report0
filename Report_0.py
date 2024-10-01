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
    "Turnover Time (days)": [7, 14, 10, 12, 5, 20, 15, 10, 22, 12, 9, 8, 4]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Add an Efficiency Metric: Occupied Units / Total Units * 100
df['Occupancy Efficiency (%)'] = (df["Total Units"] - df["Units Offline"]) / df["Total Units"] * 100

# Add Daily Rate for Hope House
daily_rate_hope_house = 227  # $227 per day for Hope House
df['Daily Cost Impact (Hope House)'] = df['Units Offline'] * daily_rate_hope_house * df['Days Offline']  # Calculating cost impact for Hope House

# Streamlit App Title
st.title("CRF Vacancy Control Dashboard with Cost Analysis and Business Summaries")

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
This chart compares the **Occupancy Rate** and **Units Offline**. High occupancy rates at **Lenox** and **Kenilworth** show optimal utilization, whereas **Light House** and **Comfort Inn** have more offline units that impact their performance.
""")

### Cost Impact Analysis for Hope House
st.subheader("Cost Impact Analysis for Hope House")
fig_cost = px.bar(df[df["Facility"] == "Hope House"], x="Facility", y="Daily Cost Impact (Hope House)", text="Daily Cost Impact (Hope House)",
                  title="Cost Impact Due to Offline Units at Hope House")
fig_cost.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_cost)

st.markdown("""
**Business Summary**:  
The offline units at **Hope House** have a significant cost impact, with a daily rate of $227 per day. The more units that remain offline, the more revenue is lost. Strategies to minimize offline units will help reduce the cost impact.
""")

### Existing Matplotlib Plots and Business Summaries:

# Occupancy Rate Overview (Matplotlib)
st.subheader("Occupancy Rate Overview")
fig, ax = plt.subplots()
df.set_index("Facility")["Occupancy Rate (%)"].plot(kind="barh", color="#1f77b4", ax=ax)
plt.title("Occupancy Rate by Facility")
plt.xlabel("Occupancy Rate (%)")
plt.ylabel("Facility")
plt.xlim(0, 100)
for index, value in enumerate(df["Occupancy Rate (%)"]):
    plt.text(value + 1, index, f"{value}%", va='center')
st.pyplot(fig)

st.markdown("""
**Business Summary**:  
Occupancy rates remain strong across most facilities, with **Lenox** and **Kenilworth** achieving 100%. **Hope House** and **Best Western** could increase occupancy rates with targeted interventions.
""")

# Efficiency Metric (Matplotlib)
st.subheader("Occupancy Efficiency Metric")
fig, ax = plt.subplots()
df.set_index("Facility")["Occupancy Efficiency (%)"].plot(kind="barh", color="#d62728", ax=ax)
plt.title("Occupancy Efficiency by Facility")
plt.xlabel("Occupancy Efficiency (%)")
plt.ylabel("Facility")
plt.xlim(0, 100)
for index, value in enumerate(df["Occupancy Efficiency (%)"]):
    plt.text(value + 1, index, f"{value:.1f}%", va='center')
st.pyplot(fig)

st.markdown("""
**Business Summary**:  
**Kenilworth** and **Lenox** are operating at full efficiency, while **Light House** struggles due to a high number of offline units, lowering overall efficiency. Improving unit availability can enhance performance.
""")

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
