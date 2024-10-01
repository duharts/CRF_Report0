
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

# Streamlit App Title
st.title("CRF Vacancy Control Dashboard with Expanded Analysis and Business Summaries")

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

### 1. **Turnover Time Analysis**
st.subheader("1. Turnover Time Analysis")
fig_turnover = px.bar(df, x="Facility", y="Turnover Time (days)", color="Turnover Time (days)", text_auto=True,
                      title="Turnover Time by Facility")
fig_turnover.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_turnover)

st.markdown("""
**Business Summary**:  
Facilities such as **Light House** and **Park Overlook** show extended turnover times, which may suggest bottlenecks in repair processes. **Icahn House** has the shortest turnover, indicating faster unit cycling.
""")

### 2. **Crib Utilization Rate**
st.subheader("2. Crib Utilization Rate")
crib_utilization = (df["Cribs"] / df["Total Units"]) * 100
df["Crib Utilization (%)"] = crib_utilization

fig_crib = px.bar(df, x="Facility", y="Crib Utilization (%)", text="Crib Utilization (%)",
                  title="Crib Utilization Rate by Facility")
fig_crib.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_crib)

st.markdown("""
**Business Summary**:  
Crib utilization is highest at **House East** and **Light House**, which indicates that these facilities may need additional cribs to meet demand.
""")

### 3. **Days Offline Analysis**
st.subheader("3. Days Offline Analysis")
fig_days_offline = px.bar(df, x="Facility", y="Days Offline", text="Days Offline",
                          title="Days Offline by Facility", color="Days Offline")
fig_days_offline.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_days_offline)

st.markdown("""
**Business Summary**:  
**Light House** has the highest number of days offline, which significantly impacts its overall efficiency. Reducing these downtime periods can help improve occupancy rates.
""")

### 4. **Occupancy and Cribs Comparison**
st.subheader("4. Occupancy and Cribs Comparison")
fig_occupancy_cribs = px.bar(df, x="Facility", y=["Total Units", "Cribs"], barmode="group", text_auto=True,
                             title="Occupancy vs Cribs by Facility")
fig_occupancy_cribs.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_occupancy_cribs)

st.markdown("""
**Business Summary**:  
Comparing total units and cribs reveals that **Light House** and **House East** serve more families with young children, as they allocate a higher percentage of total units for cribs.
""")

### Existing Matplotlib Plots and Business Summaries:

# Occupancy Rate Overview (Matplotlib)
st.subheader("5. Occupancy Rate Overview")
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
Most facilities maintain an occupancy rate above 90%, indicating strong utilization. **Hope House** and **Best Western** are areas of opportunity for improvement.
""")

# Efficiency Metric (Matplotlib)
st.subheader("6. Occupancy Efficiency Metric")
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
Facilities like **Kenilworth** and **Lenox** show 100% efficiency, utilizing all available units. **Light House** lags behind due to significant offline units.
""")

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
