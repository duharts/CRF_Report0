import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
st.title("CRF Vacancy Control Dashboard - Stacked Bar Charts")

# Function to create a stacked bar chart
def plot_stacked_bar(df, columns, title):
    fig, ax = plt.subplots()
    df[columns].plot(kind='bar', stacked=True, ax=ax)
    plt.title(title)
    plt.ylabel('Number of Units')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# Plot Stacked Bar Charts for each section
plot_stacked_bar(df, ["Available Units", "Reserved Units", "Units in Maintenance", "Units Under Repair", "Units in Long-Term Repair", "Units Offline"], "Unit Status by Facility")

# Summary Statistics Section
st.subheader("Summary Statistics")
total_units = df["Total Units"].sum()
occupied_units = df["Total Units"].sum() - df["Units Offline"].sum()

st.write(f"Total Units Across All Facilities: {total_units}")
st.write(f"Total Occupied Units Across All Facilities: {occupied_units}")
st.write(f"Average Occupancy Rate Across All Facilities: {df['Occupancy Rate (%)'].mean():.2f}%")

# Download Data as CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name='CRF_Facility_Data.csv',
    mime='text/csv',
)
