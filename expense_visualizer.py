import streamlit as st 
import sqlite3
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
#Getting The expense data

with sqlite3.Connection("expense.db") as conn:
    expense_df=pd.read_sql_query("SELECT * FROM Expenses",conn)
    # print(expense_df)

#Setting page
st.title("Let's Do Some Data Visualization")


#--------------------------Setting Date v/s Amount Spent Chart---------------------------

expenses_by_date = expense_df.groupby("expense_date", as_index=False)["expense_amount"].sum()
expense_df = expense_df.drop(columns=["expense_id"])
y_range_max=expenses_by_date["expense_amount"].max()
y_range_max=y_range_max*1.1
fig=px.line(expenses_by_date,x='expense_date',y='expense_amount',range_y=[0,y_range_max],title="Expenses By Date")
fig.update_layout(xaxis_title="Date", yaxis_title="Amount spent")
fig.update_traces(mode="lines+markers", marker=dict(size=8, color='white'))
st.plotly_chart(fig,width='stretch')
#--------------------------Setting Date v/s Amount Spent Chart Using Matplotlib---------------------------
# expenses_by_date = expense_df.groupby("expense_date", as_index=False)["expense_amount"].sum()
# expense_df = expense_df.drop(columns=["expense_id"])
# print(expenses_by_date)
# fig,ax=plt.subplots()
# expenses_by_date.plot(ax=ax)
# st.pyplot(fig)
# fig=plt.plot(expenses_by_date)

###---------------------------------Setting Pie charts---------------------------------
col1,col2=st.columns(2)
col1.markdown("<h4>Expenses Based on Category</h3>",unsafe_allow_html=True)

#Getting Data and grouping it based on category
expenses_by_cat=expense_df.groupby("expense_category",as_index=False)["expense_amount"].sum()
# print(expenses_by_cat)
# print(type(expenses_by_cat))
# column_list = expenses_by_cat.columns.tolist()
# print(column_list)

#Drawing Chart
fig=px.pie(expenses_by_cat,values='expense_amount', names = 'expense_category')
col1.plotly_chart(fig,width="stretch")


#Getting Data and grouping it based on category
expenses_by_tag=expense_df.groupby("expense_tag",as_index=False)["expense_amount"].sum()

#Drawing Charts
col2.markdown("<h3>Expenses Based On Tags</h3>", unsafe_allow_html=True)
fig=px.pie(expenses_by_tag,values='expense_amount',names='expense_tag')
fig.update_layout(showlegend=False)
col2.plotly_chart(fig,width="stretch")

###----------------------------Bar Charts For monthly Data----------------------------
expense_df['expense_date']=pd.to_datetime(expense_df["expense_date"],format="%d-%m-%Y")
expenses_by_month=expense_df.groupby(expense_df["expense_date"].dt.to_period('M'),as_index=False)['expense_amount'].sum()
print(expenses_by_month)
expenses_by_month["expense_date"]=expenses_by_month["expense_date"].astype(str)
fig=px.bar(expenses_by_month,x='expense_date',y='expense_amount')
st.plotly_chart(fig,width="stretch")


