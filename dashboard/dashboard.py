import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='white')

bs_day_df = pd.read_csv('day_clean_df.csv')
bs_hour_df = pd.read_csv('hour_clean_df.csv')

# =============================================
# KUMPULAN HELPER
# Total penyewaan perhari
def create_daily_total_df(bs_hour_df):
  daily_count = bs_hour_df.groupby('dteday')['cnt'].sum().reset_index()

  return daily_count


# Skema jumlah penyewaan berdasarkan pengguna casual
def create_casual_total_df(bs_day_df):
  total_casual = bs_day_df.groupby(by='casual').agg({'casual':'sum'})
  total_casual.rename(columns={'casual':'casual_sum'},inplace=True)

  return total_casual

# Skema jumlah penyewaan berdasarkan pengguna registered
def create_registered_total_df(bs_day_df):
  total_registered = bs_day_df.groupby(by='registered').agg({'registered':'sum'})
  total_registered.rename(columns={'registered':'registered_sum'},inplace=True)

  return total_registered

# Skema rata rata penyewaan 2011
def create_year_first_total_df(bs_day_df):
  first_year = bs_day_df[bs_day_df['yr'] == 0]
  avg_mnth_first = first_year.groupby('mnth')['cnt'].mean().reset_index()

  return avg_mnth_first

# Skema rata rata penyewaan 2012
def create_year_second_total_df(bs_day_df):
  second_year = bs_day_df[bs_day_df['yr'] == 1]
  avg_mnth_second = second_year.groupby('mnth')['cnt'].mean().reset_index()

  return avg_mnth_second

# Skema jumlah penyewaan berdasarkan musim
def create_season_total_df(bs_day_df):
  total_season = bs_day_df.groupby('season')['cnt'].mean().reset_index()

  return total_season

# Skema jumlah penyewaan berdasarkan pengguna casual dan registered
def create_user_total_df(bs_day_df):
  avg_users = bs_day_df[['casual', 'registered']].sum()

  return avg_users

def create_highest_time_df(bs_hour_df):
  sum_hour = bs_hour_df.groupby('hr')['cnt'].sum()
  sum_hour = sum_hour.sort_values(ascending=False)
  top_hour = sum_hour.head(5)

  return top_hour

def create_lowest_time_df(bs_hour_df):
  sum_hour = bs_hour_df.groupby('hr')['cnt'].sum()
  sum_hour = sum_hour.sort_values(ascending=False)
  bottom_hour = sum_hour.tail(5)

  return bottom_hour

# Skema jumlah penyewaan berdasarkan suhu
def create_temp_total_df(bs_day_df):
  total_temp = bs_day_df[['temp', 'cnt']].reset_index()

  return total_temp

# Skema jumlah penyewaan berdasarkan kelembaban
def create_hum_total_df(bs_day_df):
  total_hum = bs_day_df[['hum', 'cnt']].reset_index()

  return total_hum

# Skema jumlah penyewaan berdasarkan kecepatan angin windspeed
def create_windspeed_total_df(bs_day_df):
  total_windspeed = bs_day_df[['windspeed', 'cnt']].reset_index()

  return total_windspeed

# =============================================

# Memastikan kolom date itu tipe datanya date time
datetime_columns = ["dteday"]
bs_day_df.sort_values(by="dteday", inplace=True)
bs_day_df.reset_index(inplace=True)

for column in datetime_columns:
    bs_day_df[column] = pd.to_datetime(bs_day_df[column])
    bs_hour_df[column] = pd.to_datetime(bs_hour_df[column])

# Membuat filter widget date input dan gambar
min_date = bs_day_df["dteday"].min()
max_date = bs_day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/syifagusriani/pad-assets/refs/heads/main/bike-sharing-photo.jpg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Menyimpan filter
main_df = bs_hour_df[(bs_hour_df["dteday"] >= str(start_date)) &
                (bs_hour_df["dteday"] <= str(end_date))]


daily_total_df = create_daily_total_df(main_df)
casual_total_df = create_casual_total_df(main_df)
registered_total_df = create_registered_total_df(main_df)
year_first_total_df = create_year_first_total_df(bs_day_df)
year_second_total_df = create_year_second_total_df(bs_day_df)
season_total_df = create_season_total_df(main_df)
user_total_df = create_user_total_df(main_df)
highest_time_df = create_highest_time_df(main_df)
lowest_time_df = create_lowest_time_df(main_df)
temp_total_df = create_temp_total_df(bs_day_df)
hum_total_df = create_hum_total_df(bs_day_df)
windspeed_total_df = create_windspeed_total_df(bs_day_df)


# =============================================
# Bagian 1
st.header('Bike Sharing Dashboard')

col1, col2, col3 = st.columns(3)

with col1:
     all_total_df = daily_total_df.cnt.sum()
     st.metric("Total Penyewaan", value=all_total_df)

with col2:
     casual_total_df = casual_total_df.casual_sum.sum()
     st.metric("Total Penyewaan Casual", value=casual_total_df)

with col3:
    registered_total_df = registered_total_df.registered_sum.sum()
    st.metric("Total Penyewaan Registered", value=registered_total_df)

# =============================================
# Bagian 2
st.subheader("Distribusi Penyewaan Sepeda Per Bulan Tahun 2011 dan 2012")

fig, ax1 = plt.subplots(1, 2, figsize=(20, 8), sharey=True)

sns.lineplot(x=year_first_total_df['mnth'], y=year_first_total_df['cnt'], marker='o', ax=ax1[0])
ax1[0].set_title('Distribusi Penyewaan Sepeda Per Bulan Tahun 2011', fontsize=20)
ax1[0].set_xlabel('Bulan', fontsize=15)
ax1[0].set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=15)
ax1[0].set_xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax1[0].grid(True)

sns.lineplot(x=year_second_total_df['mnth'], y=year_second_total_df['cnt'], marker='o', ax=ax1[1])
ax1[1].set_title('Distribusi Penyewaan Sepeda Per Bulan Tahun 2012', fontsize=20)
ax1[1].set_xlabel('Bulan', fontsize=15)
ax1[1].set_xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax1[1].grid(True)

for ax in ax1:
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)

plt.tight_layout()
st.pyplot(fig)

# =============================================
# Bagian 3
st.subheader("Distribusi Penyewaan Sepeda Harian")
fig, ax2 = plt.subplots(figsize=(20, 8))
ax2.plot(
    daily_total_df['dteday'],
    daily_total_df['cnt'],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax2.set_title("Distribusi Penyewaan Sepeda Harian", fontsize=30)

ax2.tick_params(axis='y', labelsize=20)
ax2.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


# =============================================
# Bagian 4
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
fig, ax3 = plt.subplots(figsize=(20, 8))
sns.barplot(data=season_total_df, x='season', y='cnt', palette='viridis')

ax3.set_xlabel('Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)', fontsize=18)
ax3.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=18)
ax3.tick_params(axis='x', labelsize=15)
ax3.tick_params(axis='y', labelsize=15)

st.pyplot(fig)

# =============================================
# Bagian 5
st.subheader("Presentase Total Pengguna Casual dan Registered")

fig, ax4 = plt.subplots(figsize=(3, 3))
exploded = (0.1, 0)
ax4.pie(
    user_total_df,
    labels=user_total_df.index,
    colors=plt.cm.Dark2.colors,
    autopct='%.0f%%',
    textprops={'color':'black'},
    explode=exploded
)

st.pyplot(fig)

# =============================================
# Bagian 6
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Jam")
top = highest_time_df.sort_index(ascending=True)
bottom = lowest_time_df.sort_index(ascending=True)

top_index = highest_time_df.idxmax()
bottom_index = lowest_time_df.idxmin()

colors1 = ['red' if i == top_index else 'skyblue' for i in top.index]
colors2 = ['skyblue' if i == bottom_index else 'red' for i in bottom.index]

fig, ax6 = plt.subplots(1, 2, figsize=(12, 6))

sns.barplot(x=highest_time_df.index, y=highest_time_df.values, ax=ax6[0], palette=colors1)
ax6[0].set_title('Jam dengan Penyewaan Tertinggi')
ax6[0].set_xlabel('Jam')
ax6[0].set_ylabel('Jumlah Penyewaan')

sns.barplot(x=lowest_time_df.index, y=lowest_time_df.values, ax=ax6[1], palette=colors2)
ax6[1].set_title('Jam dengan Penyewaan Terendah')
ax6[1].set_xlabel('Jam')
ax6[1].set_ylabel('Jumlah Penyewaan')

plt.tight_layout(rect=[0, 0, 1, 0.95])

st.pyplot(fig)

# =============================================
# Bagian 7
st.subheader("Hubungan Jumlah Penyewaan Sepeda Dengan Faktor Cuaca Tahun 2011 - 2012")
fig, ax7 = plt.subplots(1, 3, figsize=(20, 8), sharey=True)

sns.regplot(data=temp_total_df, x='temp', y='cnt', scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'}, ax=ax7[0])
ax7[0].set_title('Suhu vs Penyewaan', fontsize=20)
ax7[0].set_xlabel('Suhu (Normalized)', fontsize=19)
ax7[0].set_ylabel('Jumlah Penyewaan', fontsize=19)

sns.regplot(data=hum_total_df, x='hum', y='cnt', scatter_kws={'alpha': 0.5}, line_kws={'color': 'blue'}, ax=ax7[1])
ax7[1].set_title('Kelembaban vs Penyewaan', fontsize=20)
ax7[1].set_xlabel('Kelembaban (Normalized)', fontsize=19)
ax7[1].set_ylabel(None)

sns.regplot(data=windspeed_total_df, x='windspeed', y='cnt', scatter_kws={'alpha': 0.5}, line_kws={'color': 'green'}, ax=ax7[2])
ax7[2].set_title('Kecepatan Angin vs Penyewaan', fontsize=20)
ax7[2].set_xlabel('Kecepatan Angin (Normalized)', fontsize=19)
ax7[2].set_ylabel(None)

for ax in ax7:
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)

fig.tight_layout(rect=[0, 0, 1, 0.95])
st.pyplot(fig)

st.caption('Copyright © Syifa Gusriani Rohman 2024')