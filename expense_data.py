import streamlit as st
import sqlite3
import pandas as pd
from datetime import date,timedelta

col1,col2,col3=st.columns(3)
date_filter=col1.selectbox("Select Date Range",options=["All","Today","Yesterday","Last 7 Days","Last 30 Days", "Last 1 Year",  "Custom"])
category_filter=st.multiselect("Category Filter",options=["Needs","Wants","Savings"],default=[])
with sqlite3.Connection("expense.db") as conn:
    df_tags=pd.read_sql_query("SELECT Tags FROM TAGS",conn)
    tag_list=df_tags["Tags"].to_list()
tag_filter=st.multiselect("Tag Filter",options=tag_list,default=[])
col3,col4=st.columns([5,4])
col3.subheader("Expenses Record")
with sqlite3.Connection("expense.db") as conn:
    df=pd.read_sql_query("SELECT * FROM Expenses",conn)
    display_df=df.drop(columns=["expense_id"])
    if tag_filter ==[]:
        tag_filter=tag_list
    if category_filter==[]:
        category_filter=["Needs","Wants","Savings"]
    filtered_df=display_df[
        (df['expense_category'].isin(category_filter)) &
        (df['expense_tag'].isin(tag_filter))
    ]
    filtered_df["expense_date"]=pd.to_datetime(filtered_df["expense_date"])
    today=date.today()
    if date_filter=="Today":
        filtered_df=filtered_df[
            filtered_df['expense_date'].dt.date==today
        ]
    elif date_filter=="Yesterday":
        yesterday=today-timedelta(days=1)
        filtered_df=filtered_df[
            filtered_df['expense_date'].dt.date==yesterday
        ]
    elif date_filter=="Last 7 Days":
        seven_days_ago=today-timedelta(days=7)
        filtered_df=filtered_df[
            filtered_df['expense_date'].dt.date>=seven_days_ago
        ]
    elif date_filter=="Last 30 Days":
        thirty_days_ago=today-timedelta(days=30)
        filtered_df=filtered_df[
            filtered_df['expense_date'].dt.date>=thirty_days_ago
        ]
    elif date_filter=="Last 1 Year":
        one_year_ago=today-timedelta(days=365)
        filtered_df=filtered_df[
            filtered_df['expense_date'].dt.date>=one_year_ago
        ]
    elif date_filter=="Custom":
        start_date=col2.date_input("Pick Start Date",max_value="today")
        end_date=col3.date_input("Pick End Date",max_value="today")
        if end_date<start_date:
            st.warning("End Date can not be smaller than start date")
        filtered_df=filtered_df[
            (filtered_df['expense_date'].dt.date>=start_date) &
            (filtered_df["expense_date"].dt.date<=end_date)
        ]
    filtered_df=filtered_df.sort_values(by="expense_date", ascending=False)
    filtered_df["expense_date"]=pd.to_datetime(filtered_df["expense_date"],format="%d-%m-%Y").dt.date
    st.dataframe(filtered_df,hide_index=True,width="stretch")
    total=filtered_df['expense_amount'].sum()
    txt=f"<span style='font-size:24px;'>Your Total Expense is: ₹{total}</span>"
    col4.markdown(txt,width="stretch",text_alignment="center",unsafe_allow_html=True)


