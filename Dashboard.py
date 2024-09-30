import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime 

# Set style for the plots
sns.set(style='whitegrid')


df = pd.read_csv("https://raw.githubusercontent.com/Asalulzy/Dashboard-Bangkit/main/all_data.csv")

# Helper function to classify season based on temperature
def classify_season(temp):
    if temp < 0:
        return 'Gelombang Dingin'
    elif 0 <= temp < 10:
        return 'Musim Dingin'
    elif 10 <= temp < 20:
        return 'Musim Semi'
    elif 20 <= temp < 30:
        return 'Musim Panas'
    elif 30 <= temp < 35:
        return 'Musim Panas Intens'
    elif temp >= 35:
        return 'Gelombang Panas'
    else:
        return 'Tidak Diketahui'

# Add a season column based on temperature
df['Season'] = df['TEMP'].apply(classify_season)

# Sidebar to filter by season
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox(
    "Select Season:",
    df['Season'].unique()
)

# Filter data by selected season
filtered_data = df[df['Season'] == selected_season]

# Create plots
st.title('Air Quality Analysis Dashboard')

# Show the selected season's data
st.subheader(f'Data for {selected_season}')
st.write(filtered_data)

# Plot the concentration of air quality compounds by season
st.subheader(f'Average Concentration of Compounds in {selected_season}')

# Define compounds to visualize
compounds = ['NO2', 'SO2', 'PM10', 'PM2.5']

# Barplot of compound concentration by season
avg_compound = filtered_data[compounds].mean()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=avg_compound.index, y=avg_compound.values, ax=ax, palette='coolwarm')
ax.set_title(f'Average Concentration of Air Compounds in {selected_season}')
ax.set_xlabel('Compound')
ax.set_ylabel('Concentration (µg/m³)')
st.pyplot(fig)

# Time-series plot of NO2 over time
st.subheader('NO2 Concentration Over Time')

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=filtered_data['datetime'], y=filtered_data['NO2'], ax=ax)
ax.set_title('NO2 Concentration Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('NO2 Concentration (µg/m³)')
st.pyplot(fig)

# Additional plots and analytics can be added similarly
st.caption('Air Quality Data Dashboard © 2024')
