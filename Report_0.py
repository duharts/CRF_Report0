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

# Section 1: Occupancy Rate Line Chart
with st.expander("Occupancy Rate by Facility"):
    st.subheader("Occupancy Rate by Facility")
    st.line_chart(df.set_index("Facility")["Occupancy Rate (%)"])

# Section 2: Total Units Line Chart
with st.expander("Total Units per Facility"):
    st.subheader("Total Units per Facility")
    st.line_chart(df.set_index("Facility")["Total Units"])

# Section 3: Available Units Line Chart
with st.expander("Available Units per Facility"):
    st.subheader("Available Units per Facility")
    st.line_chart(df.set_index("Facility")["Available Units"])

# Section 4: Reserved Units Line Chart
with st.expander("Reserved Units per Facility"):
    st.subheader("Reserved Units per Facility")
    st.line_chart(df.set_index("Facility")["Reserved Units"])

# Section 5: Units in Maintenance Line Chart
with st.expander("Units in Maintenance per Facility"):
    st.subheader("Units in Maintenance per Facility")
    st.line_chart(df.set_index("Facility")["Units in Maintenance"])

# Section 6: Units Under Repair Line Chart
with st.expander("Units Under Repair per Facility"):
    st.subheader("Units Under Repair per Facility")
    st.line_chart(df.set_index("Facility")["Units Under Repair"])

# Section 7: Units in Long-Term Repair Line Chart
with st.expander("Units in Long-Term Repair per Facility"):
    st.subheader("Units in Long-Term Repair per Facility")
    st.line_chart(df.set_index("Facility")["Units in Long-Term Repair"])

# Section 8: Units Offline Line Chart
with st.expander("Units Offline per Facility"):
    st.subheader("Units Offline per Facility")
    st.line_chart(df.set_index("Facility")["Units Offline"])

# Section 9: Summary Statistics
with st.expander("Overall Summary Statistics"):
    st.subheader("Summary Statistics")
    total_units = df["Total Units"].sum()
    occupied_units = df["Total Units"].sum() - df["Units Offline"].sum()
    st.write(f"Total Units Across All Facilities: {total_units}")
    st.write(f"Total Occupied Units Across All Facilities: {occupied_units}")
    st.write(f"Average Occupancy Rate Across All Facilities: {df['Occupancy Rate (%)'].mean():.2f}%")

# Download option
with st.expander("Download Data"):
    st.write("Download the filtered data as a CSV:")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='CRF_Facility_Data.csv',
        mime='text/csv',
    )
