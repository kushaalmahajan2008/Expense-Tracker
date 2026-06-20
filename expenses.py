import streamlit as st

#Setting Up pages 
expense_tracker_page=st.Page(
    page="expense_tracker.py",
    default=True,
    title="Expense Tracker"
)

expense_data_page=st.Page(
    page="expense_data.py",
    title="Expense Data"
)

expense_visulizer_page=st.Page(
    page="expense_visualizer.py",
    title="Expense Visualisation"
)

pg=st.navigation(
    {"Expense Tracker App":[expense_tracker_page,expense_data_page,expense_visulizer_page]}
)
st.sidebar.text("Made with ❤️ By Kushaal Mahajan")

pg.run()