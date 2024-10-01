import streamlit as st
import pandas as pd
import plotly.express as px

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
st.title("CRF Vacancy Control Dashboard with Full Data & Interactive Stacked Bar Charts")

# Function to plot interactive stacked bar chart with Plotly
def plot_comparison_chart(metrics):
    df_melted = df.melt(id_vars="Facility", value_vars=metrics, var_name="Metric", value_name="Value")
    fig = px.bar(df_melted, x="Facility", y="Value", color="Metric", 
                 title=f"Comparison of Metrics: {', '.join(metrics)}",
                 labels={"Value": "Values", "Facility": "Facility"},
                 hover_data={"Value": ":.2f"},  # Show values with 2 decimal places
                 text="Value")  # Display values on hover
    fig.update_layout(barmode='stack', xaxis_tickangle=-45)
    st.plotly_chart(fig)

# Multiselect for choosing metrics to compare
st.subheader("Choose Metrics to Compare")
metrics = st.multiselect(
    "Select Metrics for Comparison",
    options=df.columns.drop("Facility"),  # Exclude Facility column
    default=["Occupancy Rate (%)", "Units Offline", "Cribs", "Days Offline"]  # Preselect common metrics
)

# Display comparison chart
if metrics:
    plot_comparison_chart(metrics)

# Full Data Visualization for Repairs and Status
st.subheader("Unit Repair Status and Details")
fig_status = px.bar(df, x="Facility", y="Days Offline", text="Days Offline", color="Status",
                    title="Days Offline by Facility and Repair Status",
                    labels={"Days Offline": "Days Offline", "Facility": "Facility", "Status": "Repair Status"},
                    hover_data=["Details (Repairs Needed)", "Expected Date", "Time of Turnover"])
fig_status.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_status)

# Efficiency Metric: Occupied Units vs Available Units (Occupancy Efficiency)
st.subheader("Occupancy Efficiency by Facility")
fig_efficiency = px.bar(df, x="Facility", y="Occupancy Efficiency (%)", text="Occupancy Efficiency (%)",
                        title="Occupancy Efficiency by Facility",
                        labels={"Occupancy Efficiency (%)": "Efficiency (%)"})
fig_efficiency.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_efficiency)

# Displaying the data in a table
st.write(df[["Facility", "Occupancy Efficiency (%)", "Cribs", "Days Offline", "Status", "Details (Repairs Needed)", "Expected Date", "Time of Turnover"]])

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
