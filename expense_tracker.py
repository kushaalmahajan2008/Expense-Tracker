import streamlit as st
import sqlite3
import pandas as pd




def add_new_tag(tag):
    add_tag="""INSERT INTO TAGS(Tags) VALUES(?)"""
    with sqlite3.connect("expense.db",timeout=10) as conn:
        conn.execute(add_tag,(tag,))
        conn.commit()
        

def track_expense(date,amount,category,tag,description):
    date_str=date.strftime("%d-%m-%Y")
    data=(date_str,amount,category,tag,description)
    record_data="""INSERT INTO Expenses
    (expense_date,expense_amount,expense_category,expense_tag,expense_description)
    VALUES(?,?,?,?,?)"""
    with sqlite3.Connection("expense.db",timeout=10) as conn:
        conn.execute(record_data,data)
        conn.commit()

tag="""CREATE TABLE IF NOT EXISTS TAGS
    (Tags Text NOT NULL)"""

with sqlite3.Connection("expense.db",timeout=10) as conn:
        conn.execute(tag)


st.title("Expense Tracker")


with st.form("Expense Tracker",clear_on_submit=False):
    with sqlite3.Connection("expense.db") as conn:
        tags_df=pd.read_sql_query("Select Tags FROM TAGS",conn)
    tags=tags_df["Tags"].to_list()
    date=st.date_input("Date*",max_value="today",format="DD/MM/YYYY")
    amount=st.number_input("Amount*",key="amount")
    category=st.selectbox("Category*",options=["Select A Category", "Wants","Needs","Savings"])
    tag=st.selectbox("Tag*",accept_new_options=True,options=tags)
    description=st.text_area("Description",max_chars=255)
    track_button=st.form_submit_button("Track")
    if track_button:
        if amount<=0:
            st.warning("Please Enter A Valid Amount")
        elif category=="Select A Category":
            st.warning("Please Select A Category")
        elif tag=="":
            st.warning("Please Select A Tag")
        else:
            if tag not in tags:
                add_new_tag(tag)
            track_expense(date,amount,category,tag,description)
            st.success("Your Expense Tracked Successfully")
        
        