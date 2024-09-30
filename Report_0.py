import streamlit as st
import pandas as pd

# Sample Data extracted from the CRF Vacancy Control Dashboards
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

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_facilities = st.sidebar.multiselect("Select Facilities", df['Facility'].unique())
occupancy_range = st.sidebar.slider("Select Occupancy Rate Range", 0, 100, (80, 100))

# Apply filters to DataFrame
filtered_df = df[(df['Occupancy Rate (%)'] >= occupancy_range[0]) & (df['Occupancy Rate (%)'] <= occupancy_range[1])]

if selected_facilities:
    filtered_df = filtered_df[filtered_df['Facility'].isin(selected_facilities)]

# Section: Filtered Data
with st.expander("Filtered Facility Data"):
    st.subheader("Filtered Facility Data")
    st.dataframe(filtered_df)

# Section: Occupancy Rate Line Chart
with st.expander("Occupancy Rate by Facility (Line Chart)"):
    st.subheader("Occupancy Rate by Facility")
    st.line_chart(filtered_df.set_index("Facility")["Occupancy Rate (%)"])

# Section: Detailed Units Breakdown
with st.expander("Detailed Units Breakdown"):
    st.subheader("Detailed Units Breakdown")
    st.write("This table shows detailed information about the units under repair, in long-term repair, or offline.")
    st.dataframe(filtered_df[[
        "Facility", "Available Units", "Reserved Units", 
        "Units in Maintenance", "Units Under Repair", 
        "Units in Long-Term Repair", "Units Offline"
    ]])

# Section: Summary Statistics
with st.expander("Overall Summary Statistics"):
    st.subheader("Overall Summary Statistics")
    total_units = df["Total Units"].sum()
    occupied_units = df["Total Units"].sum() - df["Units Offline"].sum()

    st.write(f"Total Units Across All Facilities: {total_units}")
    st.write(f"Total Occupied Units Across All Facilities: {occupied_units}")
    st.write(f"Average Occupancy Rate Across All Facilities: {df['Occupancy Rate (%)'].mean():.2f}%")

# Download Filtered Data
with st.expander("Download Filtered Data"):
    st.sidebar.subheader("Download Filtered Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_facility_data.csv',
        mime='text/csv',
    )
