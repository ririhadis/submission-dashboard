import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='darkgrid')

#membuat data frame
def create_monthly_sharing_df(df):
    monthly_sharing_df = df.resample(rule = 'D', on ='dteday').agg({
        "mnth_x" :"nunique",
        "cnt_x" : "sum"
    })
    monthly_sharing_df = monthly_sharing_df.reset_index()
    monthly_sharing_df.rename(columns ={
        "mnth_x" : "month_sharing",
        "cnt_x" : "total"
    }, inplace= True)

    return monthly_sharing_df

def create_sum_sharing_df(df):
    sum_sharing_df = df.groupby("mnth_x").cnt_x.sum().sort_values(ascending=False).reset_index()
    return sum_sharing_df

def create_byweekday_df(df):
    byweekday_df = df.groupby('weekday_x').cnt_x.sum().reset_index()
    byweekday_df.rename(columns={
          "cnt_x" : "sum"
    }, inplace =True)

    return byweekday_df

def create_byseason_per_yr_df(df):
    byseason_per_yr_df = df.groupby(['season_x', 'yr_x']).cnt_x.sum().reset_index()
    byseason_per_yr_df.rename(columns={
        "cnt_x" : "sum"
    }, inplace=True)

    return byseason_per_yr_df

def create_byworkingday_per_yr_df(df):
    byworkingday_per_yr_df = df.groupby(['workingday_x', 'yr_x']).cnt_x.sum().reset_index()
    byworkingday_per_yr_df.rename(columns={
        "cnt_x" : "sum"
    }, inplace=True)

    return byworkingday_per_yr_df

def create_byworkingday_per_hr_df(df):
    byworkingday_per_hr_df = df.groupby(['workingday_y', 'hr']).cnt_y.sum().reset_index()
    byworkingday_per_hr_df.rename(columns={
        "cnt_y" : "sum"
    }, inplace=True)

    return byworkingday_per_hr_df

def create_byweathersit_per_hr_df(df):
    byweathersit_per_hr_df = df.groupby(['weathersit_y','hr']).cnt_y.sum().reset_index()
    byweathersit_per_hr_df.rename(columns={
        "cnt_y" : "sum"
    }, inplace=True)

    return byweathersit_per_hr_df

def create_byclustime_df(df):
    byclustime_df = df.groupby(['yr_y', 'hr']).cnt_x.sum().reset_index()
    byclustime_df.rename(columns={
        "cnt_x" : "sum"
    }, inplace = True)

    return byclustime_df

def create_byclusseason_df(df):
    byclusseason_df = df.groupby("season_x").casual_x.sum().reset_index()
    byclusseason_df.rename(columns={
        "casual_x" : "sum"
    }, inplace=True)

    return byclusseason_df

def create_byclusseason1_df(df):
    byclusseason1_df = df.groupby("season_x").registered_x.sum().reset_index()
    byclusseason1_df.rename(columns={
        "registered_x" : "sum"
    }, inplace = True)

    return byclusseason1_df

#load dataset
all_df = pd.read_csv("main_data.csv")

#mengubah dataframe dteday agar tetap bertipe data datetime
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

#membuat komponen filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    #mengambil start dan end date dari date input
    start_date, end_date = st.date_input(
        label = 'Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value = [min_date, max_date]
    )

#menyimpan data setelah difilter menggunakan min_date dan max_date
main_df = all_df[(all_df['dteday'] >= str(start_date)) &
                 (all_df['dteday'] <= str(end_date))]

#tahap awal visualisasi dataframe
monthly_sharing_df = create_monthly_sharing_df(main_df)
sum_sharing_df =create_sum_sharing_df(main_df)
byweekday_df = create_byweekday_df(main_df)
byseason_per_yr_df = create_byseason_per_yr_df(main_df)
byworkingday_per_yr_df = create_byworkingday_per_yr_df(main_df)
byworkingday_per_hr_df = create_byworkingday_per_hr_df(main_df)
byweathersit_per_hr_df = create_byweathersit_per_hr_df(main_df)
byclustime_df = create_byclustime_df(main_df)
byclusseason_df = create_byclusseason_df(main_df)
byclusseason1_df = create_byclusseason1_df(main_df)

#melengkapi dashboard dengan berbagai visualisasi
st.header('Bike Sharing Visualisation :sparkles:')

#menampilkan data penyewaan dalam bentuk matrik
st.subheader('Monthly Bike Sharing')

col1, col2 =st.columns(2)

with col1:
    total_day = monthly_sharing_df.month_sharing.sum()
    st.metric("Total day", value = total_day)

with col2:
    total_cnt_x = monthly_sharing_df.total.sum()
    st.metric("Total Tenancy (times)", value=total_cnt_x)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_sharing_df["dteday"],
    monthly_sharing_df["total"],
    marker ='o',
    linewidth = 2,
    color = "#90CAF9"
)

ax.tick_params(axis = 'y', labelsize = 20)
ax.tick_params(axis = 'x', labelsize = 15)

st.pyplot(fig)

#menampilkan visualisasi penyewaan per musim per tahun
fig, ax = plt.subplots(figsize=(10,5))

colors=["#73bca4", "#f8a4c7"]

sns.barplot(
    y ="sum",
    x = "season_x",
    hue = "yr_x",
    data =byseason_per_yr_df.sort_values(by ="sum", ascending=False),
    palette = colors,
    ax=ax                
)

ax.set_title("Visualisation Bike Sharing Based on Season per Year", loc='center', fontsize=15)
ax.set_ylabel("Summary")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#menampilkan visualisasi penyewaan yang dilakukan saat weekday
fig, ax = plt.subplots(figsize=(10,5))

colors=["#73bca4", "#f8a4c7", "#a57bdc", "#1facf7", "#2c6fda", "#e3bca4", "#d3d2d4"]
explode = (0.1, 0, 0, 0, 0, 0, 0)

ax.pie(
    x = byweekday_df['sum'],
    labels = byweekday_df['weekday_x'],
    autopct = '%1.2f%%',
    colors=colors,
    explode = explode,
    shadow=True,
    wedgeprops={'width':0.6}
)
ax.set_title("Bike Sharing Based on Using at Weekday", loc="center", fontsize=15)
st.pyplot(fig)

#menampilkan penyewaan sepeda pada tanggal merah di hari kerja ataupun hari libur
fig, ax = plt.subplots(figsize=(10,5))

colors=["#73bca4", "#2c6fda"]

sns.barplot(
    y ="sum",
    x = "workingday_x",
    hue = "yr_x",
    data =byworkingday_per_yr_df.sort_values(by ="sum", ascending=False),
    palette = colors,
    ax=ax
)

ax.set_title("Visualisation Bike Sharing Based on Workingday per Year", loc='center', fontsize=15)
ax.set_ylabel("Summary")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#menampilkan visualisasi penyewaan sepeda pada tanggal merah dihari kerja ataupun hari libur berdasarkan jam
fig, ax = plt.subplots(figsize=(10,5))

colors=["#e3bca4", "#a57bdc"]

sns.barplot(
    y ="sum",
    x = "hr",
    hue = "workingday_y",
    data =byworkingday_per_hr_df.sort_values(by ="sum", ascending=False).sample(10),
    palette = colors,
    ax=ax                
)

ax.set_title("Visualisation Bike Sharing Based on Workingday per Hour", loc='center', fontsize=15)
ax.set_ylabel("Summary")
ax.set_xlabel("Hour")
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#menampilkan visualisasi penyewaan sepeda berdasarkan cuaca per jam
fig, ax = plt.subplots(figsize=(10,5))

colors=["#e3bca4", "#a57bdc", "#f8a4c7", "#2c6fda" ]

sns.barplot(
    y ="sum",
    x = "hr",
    hue = "weathersit_y",
    data =byweathersit_per_hr_df.sort_values(by ="sum", ascending=False).sample(10),
    palette = colors,
    ax=ax                
)

ax.set_title("Visualisation Bike Sharing Based on Weathersit per Hour", loc='center', fontsize=15)
ax.set_ylabel("Summary")
ax.set_xlabel("Hour")
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#menampilkan visualisasi clusterring penyewaan sepeda per jam per tahun
fig, ax = plt.subplots(figsize=(10,5))

colors=["#e3bca4", "#a57bdc", "#f8a4c7"]

sns.barplot(
    y ="sum",
    x = "hr",
    hue="yr_y",
    data =byclustime_df.sort_values(by ="sum", ascending=False).head(10),
    palette = colors,
    ax=ax                
)

ax.set_title("Visualisation Time Clusterring per Hour", loc='center', fontsize=15)
ax.set_ylabel("Summary")
ax.set_xlabel("Hour")
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#menampilkan clusterring penyewaan pada musim
st.subheader("Clusstering Bike Sharing Based on Casual or Registered on Season")
fig, ax= plt.subplots(nrows=1, ncols=2, figsize=(40, 10))

colors=["#e3bca4", "#a57bdc", "#f8a4c7", "#2c6fda"]

sns.barplot(
    y ="sum",
    x = "season_x",
    #hue="yr_y",
    data =byclusseason_df.sort_values(by ="sum", ascending=False).head(10),
    palette = colors,
    ax=ax[0]
)

ax[0].set_title("Visualisation Time Clusterring on Season", loc='center', fontsize=15)
ax[0].set_ylabel("Summary")
ax[0].set_xlabel("Season")
ax[0].tick_params(axis='x', labelsize=12)

sns.barplot(
    y ="sum",
    x = "season_x",
    #hue="yr_y",
    data =byclusseason1_df.sort_values(by ="sum", ascending=False).head(10),
    palette = colors,
    ax=ax[1]
)

ax[1].set_title("Visualisation Registered on Season", loc="center", fontsize=18)
ax[1].set_ylabel("Summary")
ax[1].set_xlabel("Season")
ax[1].tick_params(axis='x', labelsize=12)

st.pyplot(fig)

st.caption('Copyright (c) Submission Dicoding 2024')