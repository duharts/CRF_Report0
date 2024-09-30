import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data extracted from the CRF Vacancy Control Dashboards with Cribs
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
    "Cribs": [10, 20, 5, 15, 7, 9, 4, 2, 12, 6, 10, 8, 5]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Add an Efficiency Metric: Occupied Units / Total Units * 100
df['Occupancy Efficiency (%)'] = (df["Total Units"] - df["Units Offline"]) / df["Total Units"] * 100

# Streamlit App Title
st.title("CRF Vacancy Control Dashboard")

# Sleeker Occupancy Rate Overview
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

# Summary of Occupancy Rate
st.markdown("""
**Summary of Occupancy Rate**:  
- The majority of facilities maintain an occupancy rate above 90%, which is a good indicator of operational effectiveness.
- Facilities such as **Lenox** and **Kenilworth** have achieved a 100% occupancy rate, showing their optimal performance.
- **Hope House** and **Best Western** are below 90%, indicating some underperformance.
""")

# Comparison: Occupied Units vs Offline Units (Proportion)
st.subheader("2. Occupied vs Offline Units Comparison")
fig, ax = plt.subplots()
df.set_index("Facility")[["Total Units", "Units Offline"]].plot(kind="barh", stacked=True, color=['#2ca02c', '#ff7f0e'], ax=ax)
plt.title("Occupied Units vs Offline Units by Facility")
plt.xlabel("Number of Units")
plt.ylabel("Facility")
st.pyplot(fig)
st.write(df[["Facility", "Total Units", "Units Offline", "Cribs"]])

# Summary of Occupied vs Offline Units
st.markdown("""
**Summary of Occupied vs Offline Units**:  
- Facilities like **Light House** and **Comfort Inn** have a high number of offline units, which could impact their overall efficiency. 
- By addressing these offline units, these facilities could increase their occupancy and service more clients.
""")

# Facility-Level Unit Availability (Stacked Bar Chart)
st.subheader("3. Facility-Level Unit Availability")
fig, ax = plt.subplots()
df.set_index("Facility")[["Available Units", "Reserved Units", "Units in Maintenance", "Units Under Repair", "Units Offline"]].plot(kind="bar", stacked=True, ax=ax)
plt.title("Facility-Level Unit Status")
plt.ylabel("Number of Units")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)
st.write(df[["Facility", "Available Units", "Reserved Units", "Units in Maintenance", "Units Under Repair", "Units Offline", "Cribs"]])

# Summary of Unit Availability
st.markdown("""
**Summary of Unit Availability**:  
- **Light House** has the highest number of available units (22), while **Kenilworth** and **Lenox** have no available units. 
- **Light House** and **Comfort Inn** have the most units offline, which may affect service availability.
- In terms of cribs, **House East** has the largest number (20), which could indicate a higher demand for family services.
""")

# Detailed Units in Maintenance or Repair
st.subheader("4. Detailed Units in Maintenance or Repair")
fig, ax = plt.subplots()
df.set_index("Facility")[["Units in Maintenance", "Units Under Repair", "Units in Long-Term Repair"]].plot(kind="bar", stacked=True, ax=ax)
plt.title("Detailed Units in Maintenance or Repair")
plt.ylabel("Number of Units")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)
st.write(df[["Facility", "Units in Maintenance", "Units Under Repair", "Units in Long-Term Repair", "Cribs"]])

# Summary of Units in Maintenance or Repair
st.markdown("""
**Summary of Units in Maintenance or Repair**:  
- **Light House** stands out with the highest number of units in maintenance (6), while several other facilities have little to no units under repair.
- **Kenilworth** and **Lenox** show strong performance with no units under repair or maintenance.
""")

# Facility Performance Comparison (Clustered Bar Chart)
st.subheader("5. Facility Performance Comparison")
fig, ax = plt.subplots()
df.set_index("Facility")[["Occupancy Rate (%)", "Units Offline", "Units Under Repair"]].plot(kind="bar", ax=ax)
plt.title("Facility Performance Comparison")
plt.ylabel("Metrics")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)
st.write(df[["Facility", "Occupancy Rate (%)", "Units Offline", "Units Under Repair", "Cribs"]])

# Summary of Facility Performance
st.markdown("""
**Summary of Facility Performance**:  
- **Ellington**, **Apollo**, and **Lenox** are top performers with high occupancy rates and minimal offline or under-repair units.
- **Light House** and **Hope House** have the highest number of offline or under-repair units, indicating the need for attention.
""")

# Efficiency Metric: Occupied Units vs Available Units (Occupancy Efficiency)
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
st.write(df[["Facility", "Occupancy Efficiency (%)", "Cribs"]])

# Summary of Occupancy Efficiency
st.markdown("""
**Summary of Occupancy Efficiency**:  
- **Lenox** and **Kenilworth** have achieved perfect efficiency, utilizing all their available units.
- **Light House** and **Comfort Inn** are underperforming in efficiency due to the high number of offline units.
""")

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
