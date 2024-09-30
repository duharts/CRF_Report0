import streamlit as st
import pandas as pd

# Sample data structure to replicate the dashboard's data
data = {
    "Facility": ["Icahn House", "House East", "Hope House", "Kenilworth", "Park Overlook Stabilization"],
    "Total Units": [65, 192, 51, 200, 91],
    "Available Units": [3, 1, 5, 0, 1],
    "Reserved Units": [0, 3, 0, 0, 0],
    "Units in Maintenance": [0, 0, 0, 0, 0],
    "Units Under Repair": [2, 1, 2, 2, 0],
    "Units in Long-Term Repair": [1, 3, 0, 0, 0],
    "Units Offline": [10, 8, 8, 2, 1],
    "Occupancy Rate": [85, 96, 84, 99, 99]
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Set up the Streamlit app
st.title("CRF Vacancy Control Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Data")
facility_filter = st.sidebar.multiselect("Select Facility", df['Facility'].unique())
occupancy_filter = st.sidebar.slider("Select Occupancy Rate", 0, 100, (80, 100))

# Filter the data based on user input
filtered_df = df[(df['Occupancy Rate'] >= occupancy_filter[0]) & (df['Occupancy Rate'] <= occupancy_filter[1])]

if facility_filter:
    filtered_df = filtered_df[filtered_df['Facility'].isin(facility_filter)]

# Display the filtered data
st.subheader("Filtered Facility Data")
st.dataframe(filtered_df)

# Show occupancy rate trends
st.subheader("Occupancy Rate by Facility")
st.bar_chart(filtered_df.set_index("Facility")["Occupancy Rate"])

# Show details about units under repair
st.subheader("Units Under Repair")
st.write("The following table shows the units currently under repair at each facility.")
st.dataframe(filtered_df[["Facility", "Units Under Repair", "Units in Long-Term Repair", "Units Offline"]])
