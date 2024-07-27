import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# sns.set(style='dark')

def create_day_orders_df(day_df):
    day_orders_df = day_df.groupby('weekday')['total_count'].sum().reset_index()
    return day_orders_df

def create_weather_order_avg_df(day_df):
    weather_order_avg_df = day_df.groupby('weather')['total_count'].mean().sort_values(ascending=False).reset_index()
    return weather_order_avg_df

def create_season_order_avg_df(day_df):
    season_order_avg_df = day_df.groupby('season')['total_count'].mean().sort_values(ascending=False).reset_index()
    return season_order_avg_df

def create_month_order_df_2011(day_df):
    month_order_df_2011 = day_df.resample(rule='M', on='date')['total_count'].sum().reset_index()
    month_order_df_2011['date'] = month_order_df_2011['date'].dt.strftime('%Y-%m')
    monthly_rentals_2011 = month_order_df_2011[month_order_df_2011['date'].str.startswith('2011')]
    return monthly_rentals_2011

def create_month_order_df_2012(day_df):
    month_order_df_2012 = day_df.resample(rule='M', on='date')['total_count'].sum().reset_index()
    month_order_df_2012['date'] = month_order_df_2012['date'].dt.strftime('%Y-%m')
    monthly_rentals_2012 = month_order_df_2012[month_order_df_2012['date'].str.startswith('2012')]
    return monthly_rentals_2012

def create_hour_order_df(hour_df):
    hour_order_df = hour_df.groupby('hour')['total_count'].sum().sort_values(ascending=False).head().reset_index()
    return hour_order_df

# Load cleaned data
day_data = pd.read_csv("./dashboard/cleaned_day.csv")
hour_data = pd.read_csv("./dashboard/cleaned_hour.csv")

datetime_columns = ["date"]
day_data.sort_values(by="date", inplace=True)
day_data.reset_index(inplace=True)

datetime_columns = ["date"]
hour_data.sort_values(by="date", inplace=True)
hour_data.reset_index(inplace=True)

for column in datetime_columns:
    day_data[column] = pd.to_datetime(day_data[column])
    hour_data[column] = pd.to_datetime(hour_data[column])

# Filter data
min_day_date = day_data["date"].min()
max_day_date = day_data["date"].max()

min_hour_date = hour_data["date"].min()
max_hour_date = hour_data["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("./dashboard/image.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_day_date,
        max_value=max_day_date,
        value=[min_day_date, max_day_date]
    )

main_day_df = day_data[(day_data["date"] >= str(start_date)) & 
                    (day_data["date"] <= str(end_date))]

main_hour_df = hour_data[(hour_data["date"] >= str(start_date)) & 
                    (hour_data["date"] <= str(end_date))]

# st.dataframe(main_df)

# Menyiapkan berbagai dataframe
day_orders_df = create_day_orders_df(main_day_df)
weather_order_avg_df = create_weather_order_avg_df(main_day_df)
season_order_avg_df = create_season_order_avg_df(main_day_df)
hour_order_df = create_hour_order_df(main_hour_df)
monthly_rentals_2012 = create_month_order_df_2012(day_data)
monthly_rentals_2011 = create_month_order_df_2011(day_data)


st.header('Bike Sharing Dashboard :sparkles:')
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_type = main_day_df['total_count'].sum()
    st.metric("Total All Rides", value=total_all_type)

with col2:
    total_casual_type = main_day_df['casual_users'].sum()
    st.metric("Total Casual Rides", value=total_casual_type)

with col3:
    total_registered_type = main_day_df['registered_users'].sum()
    st.metric("Total Registered Rides", value=total_registered_type)

st.markdown("---")

st.subheader("Hari apa yang paling banyak terjadi penyewaan sepeda?")
st.markdown("###")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(data=day_orders_df.sort_values(by='total_count', ascending=False), x='weekday', y='total_count', palette=["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax)

ax.set_title('Total Bike Rentals Per Day of the Week')
ax.set_xlabel('Day of the Week')
ax.set_ylabel('Total Bike Rentals')

st.pyplot(fig)

st.markdown("---")

st.subheader("Pada kondisi cuaca apa rata rata penyewaan sepeda paling banyak terjadi?")
st.markdown("###")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(data=weather_order_avg_df, x='weather', y='total_count', palette=["#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax)

# Menambahkan judul dan label
ax.set_title('Average Bike Rentals by Weather Condition')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Average Bike Rentals')

st.pyplot(fig)

st.markdown("---")

st.subheader("Pada musim apa rata rata penyewaan sepeda paling banyak terjadi?")
st.markdown("###")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(data=season_order_avg_df, x='season', y='total_count', palette=["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax)

# Menambahkan judul dan label
ax.set_title('Average Bike Rentals by Season Condition')
ax.set_xlabel('Season Condition')
ax.set_ylabel('Average Bike Rentals')

st.pyplot(fig)

st.markdown("---")

st.subheader("Pada jam berapa paling banyak terjadi penyewaan sepeda?")
st.markdown("###")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(data=hour_order_df, x='hour', y='total_count', palette=["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax, order=hour_order_df['hour'])

# Menambahkan judul dan label
ax.set_title('Total Bike Rentals Per Hour')
ax.set_xlabel('Hour')
ax.set_ylabel('Total Bike Rentals')

st.pyplot(fig)

st.markdown("---")

st.subheader("Bagaimana tren total penyewaan sepeda berubah selama tahun 2011 dan 2012?")
st.markdown("###")

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(27, 9))

# Visualisasi tren total penyewaan sepeda berdasarkan tahun 2011
sns.pointplot(x='date', y='total_count', data=monthly_rentals_2011, errorbar=None, ax=axes[0])
axes[0].set_title('Total Bike Rentals by 2011')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Total Count')
axes[0].set_xticks(range(0, 13))
axes[0].grid(True)

# Visualisasi tren total penyewaan sepeda berdasarkan tahun 2012
sns.pointplot(x='date', y='total_count', data=monthly_rentals_2012, errorbar=None, ax=axes[1])
axes[1].set_title('Total Bike Rentals by 2012')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Total Count')
axes[1].set_xticks(range(0, 13))
axes[1].grid(True)

st.pyplot(fig)