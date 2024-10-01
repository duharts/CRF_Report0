import streamlit as st
import pandas as pd
import plotly.express as px

# Data: Extracted from the PDF
data = {
    "Facility Name": ["Icahn House", "House East", "Hope House", "Kenilworth", "Park Overlook Stabilization",
                      "Ellington", "Apollo", "Lenox", "Light House", "Comfort Inn", "Best Western", "Park West",
                      "Belnord", "Cauldwell", "Union Hall", "Union Hall Drop in"],
    "Total Units": [65, 192, 51, 200, 91, 83, 43, 41, 240, 101, 101, 113, 130, 66, 200, 40],
    "Available Units": [3, 1, 5, 0, 1, 4, 2, 0, 22, 1, 2, 4, 0, 1, 1, 0],
    "Reserved Units": [0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 6, 0],
    "Maintenance Units": [0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 1, 0, 0, 0, 0, 0],
    "Under Repair Units": [2, 1, 2, 2, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    "Long Term Repair Units": [1, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2, 0, 3, 0, 0],
    "Other Units": [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "Renovated Units": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0],
    "Unoccupied Units": [10, 8, 8, 2, 1, 5, 3, 0, 31, 6, 8, 8, 0, 6, 7, 0],
    "Occupied Units": [55, 184, 43, 198, 90, 78, 40, 41, 209, 95, 93, 105, 130, 60, 173, 37],
    "Occupancy Rate (%)": [85, 96, 84, 99, 99, 94, 93, 100, 87, 94, 92, 93, 100, 91, 87, 93]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Title for the app
st.title("CRF Vacancy Control Dashboard with Plotly")

# Display the raw data as a table
st.write("### Facility Data Overview")
st.dataframe(df)

# Plotly: Occupancy Rate by Facility
st.write("### Occupancy Rate by Facility")
fig = px.bar(df, x='Facility Name', y='Occupancy Rate (%)', text='Occupancy Rate (%)',
             title='Current Occupancy Rate by Facility')
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45)
st.plotly_chart(fig)

# Plotly: Unoccupied Units by Facility
st.write("### Unoccupied Units by Facility")
fig2 = px.bar(df, x='Facility Name', y='Unoccupied Units', text='Unoccupied Units',
              title='Unoccupied Units by Facility', color='Unoccupied Units')
fig2.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2)

# Plotly: Breakdown of Unit Status (Stacked Bar Chart)
st.write("### Unit Status Breakdown by Facility")
df_status = df[['Facility Name', 'Available Units', 'Reserved Units', 'Maintenance Units',
                'Under Repair Units', 'Long Term Repair Units', 'Other Units']]
df_status_melted = df_status.melt(id_vars='Facility Name', var_name='Status', value_name='Units')
fig3 = px.bar(df_status_melted, x='Facility Name', y='Units', color='Status', title='Breakdown of Unit Status by Facility')
fig3.update_layout(barmode='stack', xaxis_tickangle=-45)
st.plotly_chart(fig3)

# Download data option
st.write("### Download Data")
st.download_button(label="Download data as CSV", data=df.to_csv(index=False), file_name='CRF_Vacancy_Control_Data.csv', mime='text/csv')
