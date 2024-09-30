# Let's build the Streamlit app with the detailed visualization design.

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
    "Occupancy Rate (%)": [85, 96, 84, 99, 99, 94, 93, 100, 87, 94, 92, 93, 100]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Streamlit App Title
st.title("CRF Vacancy Control Dashboard")

# Occupancy Rate Overview
st.subheader("1. Occupancy Rate Overview")
st.bar_chart(df.set_index("Facility")["Occupancy Rate (%)"])

# Facility-Level Unit Availability (Stacked Bar Chart)
st.subheader("2. Facility-Level Unit Availability")
fig, ax = plt.subplots()
df.set_index("Facility")[["Available Units", "Reserved Units", "Units in Maintenance", "Units Under Repair", "Units Offline"]].plot(kind="bar", stacked=True, ax=ax)
plt.title("Facility-Level Unit Status")
plt.ylabel("Number of Units")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Detailed Units in Maintenance or Repair
st.subheader("3. Detailed Units in Maintenance or Repair")
fig, ax = plt.subplots()
df.set_index("Facility")[["Units in Maintenance", "Units Under Repair", "Units in Long-Term Repair"]].plot(kind="bar", stacked=True, ax=ax)
plt.title("Detailed Units in Maintenance or Repair")
plt.ylabel("Number of Units")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Offline Unit Trends (Line Chart)
st.subheader("4. Offline Unit Trends")
st.line_chart(df.set_index("Facility")["Units Offline"])

# Occupied vs. Unoccupied Units (Donut Chart)
st.subheader("5. Occupied vs. Unoccupied Units")
occupied_units = df["Total Units"] - df["Units Offline"]
unoccupied_units = df["Units Offline"]

fig, ax = plt.subplots()
ax.pie([occupied_units.sum(), unoccupied_units.sum()], labels=["Occupied Units", "Unoccupied Units"], autopct="%1.1f%%", startangle=90, colors=['#4CAF50', '#FF5722'])
ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)

# Facility Performance Comparison (Clustered Bar Chart)
st.subheader("6. Facility Performance Comparison")
fig, ax = plt.subplots()
df.set_index("Facility")[["Occupancy Rate (%)", "Units Offline", "Units Under Repair"]].plot(kind="bar", ax=ax)
plt.title("Facility Performance Comparison")
plt.ylabel("Metrics")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Download option
st.subheader("Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Data as CSV", data=csv, file_name='CRF_Facility_Data.csv', mime='text/csv')
