import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
sns.set(style='dark')

def create_workingday_df(df):
    byworkingday_df = df.groupby(by="workingday").instant.nunique().reset_index()
    byworkingday_df.rename(columns={
        "instant": "count"
    }, inplace=True)
    return byworkingday_df

def create_weathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byweathersit_df.rename(columns={
        "instant": "count"
    }, inplace=True)
    return byweathersit_df

def workingday(df):
    st.subheader("Working Day")
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="workingday",
        y="count",
        data=df.sort_values(by="workingday", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Working Day", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def weathersit(df):
    st.subheader("Weather Sit")
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="weathersit",
        y="count",
        data=df.sort_values(by="weathersit", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Weather Sit", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    with st.sidebar:
        st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu", 
            min_value=min_date, max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

if __name__ == "__main__":
    st.header("Bike Sharing Dashboard")

    day_csv = Path(__file__).parents[1] / 'dashboard/day_clear.csv'

    day_df = pd.read_csv(day_csv)

    date = sidebar(day_df)
    if(len(date) == 2):
        main_df = day_df[(day_df["dteday"] >= str(date[0])) & (day_df["dteday"] <= str(date[1]))]
    else:
        main_df = day_df[(day_df["dteday"] >= str(st.session_state.date[0])) & (day_df["dteday"] <= str(st.session_state.date[1]))]

    workingday_df = create_workingday_df(main_df)
    workingday(workingday_df)
    weathersit_df = create_weathersit_df(main_df)
    weathersit(weathersit_df)

    year_copyright = datetime.date.today().year
    copyright = "Copyright © " + str(year_copyright) + " | Bike Sharing Dashboard | All Rights Reserved "
    st.caption(copyright)
