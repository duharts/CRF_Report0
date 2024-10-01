import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Updated data with daily pay rates for specific facilities
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
    "Daily Rate ($)": [122.22, 154.60, 227, 230, 210, 125, 125, 240, 250, 224.40, 224.40, 220, 235]
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

# Executive Summary for Table
st.markdown("""
**Executive Summary**:  
This table presents the core operational data for each facility. **Hope House** and **Light House** show the highest revenue losses due to offline units, indicating a need for operational improvements. **Kenilworth** and **Lenox** exhibit strong performance with high occupancy rates and no offline units.
""")

# Revenue Lost Due to Offline Units
st.subheader("Revenue Lost Due to Offline Units")
fig_rev_lost = plt.figure()
df.set_index("Facility")["Revenue Lost Due to Offline Units"].plot(kind="bar", color="red")
plt.title("Revenue Lost Due to Offline Units by Facility")
plt.xlabel("Facility")
plt.ylabel("Revenue Lost ($)")
st.pyplot(fig_rev_lost)

st.markdown("""
**Executive Summary**:  
The graph highlights significant revenue losses at **Hope House** and **Light House**, which suffer from prolonged downtime. Addressing the causes of offline units could recover substantial lost revenue.
""")

# Repair Costs
st.subheader("Repair Costs")
fig_repair = plt.figure()
df.set_index("Facility")["Repair Costs ($)"].plot(kind="bar", color="orange")
plt.title("Repair Costs by Facility")
plt.xlabel("Facility")
plt.ylabel("Repair Costs ($)")
st.pyplot(fig_repair)

st.markdown("""
**Executive Summary**:  
**Light House** and **Hope House** incur the highest repair costs due to offline units, making a case for preventive maintenance programs. Facilities with lower repair costs, such as **Kenilworth** and **Lenox**, can focus on maintaining their strong performance.
""")

# Crib Utilization Rate
st.subheader("Crib Utilization Rate")
fig_crib_util = plt.figure()
df.set_index("Facility")["Crib Utilization (%)"].plot(kind="bar", color="green")
plt.title("Crib Utilization Rate by Facility")
plt.xlabel("Facility")
plt.ylabel("Crib Utilization (%)")
st.pyplot(fig_crib_util)

st.markdown("""
**Executive Summary**:  
**House East** and **Light House** exhibit high crib utilization rates, indicating that these facilities serve a higher percentage of families. Ensuring crib availability can help maintain this demand.
""")

# Occupancy Rate
st.subheader("Occupancy Rate")
fig_occ_rate = plt.figure()
df.set_index("Facility")["Occupancy Rate (%)"].plot(kind="bar", color="blue")
plt.title("Occupancy Rate by Facility")
plt.xlabel("Facility")
plt.ylabel("Occupancy Rate (%)")
st.pyplot(fig_occ_rate)

st.markdown("""
**Executive Summary**:  
**Kenilworth** and **Lenox** maintain full occupancy, showcasing optimal efficiency. **Hope House** and **Light House** have lower occupancy rates, indicating potential inefficiencies that can be addressed to improve utilization.
""")

# Return to Full Capacity
st.subheader("Return to Full Capacity")
fig_return_full = plt.figure()
df.set_index("Facility")["Return to Full Capacity (Days)"].plot(kind="bar", color="purple")
plt.title("Estimated Days to Return to Full Capacity by Facility")
plt.xlabel("Facility")
plt.ylabel("Return to Full Capacity (Days)")
st.pyplot(fig_return_full)

st.markdown("""
**Executive Summary**:  
**Light House** and **Hope House** will require longer periods to return to full capacity due to a significant number of offline units. Facilities with faster return times, like **Kenilworth**, demonstrate more efficient turnaround for repairs and availability.
""")

# Occupancy Efficiency Metric
st.subheader("Occupancy Efficiency")
fig_efficiency = plt.figure()
df.set_index("Facility")["Occupancy Efficiency (%)"].plot(kind="bar", color="#d62728")
plt.title("Occupancy Efficiency by Facility")
plt.xlabel("Facility")
plt.ylabel("Occupancy Efficiency (%)")
st.pyplot(fig_efficiency)

st.markdown("""
**Executive Summary**:  
**Kenilworth** and **Lenox** are operating at full capacity, whereas **Light House** and **Comfort Inn** face inefficiencies due to offline units. Improving repair processes and minimizing downtime can enhance occupancy efficiency.
""")

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
