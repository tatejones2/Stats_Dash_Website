import streamlit as st
from sheets import fetch_sheet_data

st.set_page_config(page_title="Baseball Stats Dashboard", layout="wide")

st.title("Baseball Team Stats Dashboard")

# Fetch data from Google Sheets
data = fetch_sheet_data()

if data is not None:
    st.dataframe(data)
    st.subheader("Create a Chart")
    columns = data.columns.tolist()
    x_axis = st.selectbox("X Axis", columns)
    y_axis = st.selectbox("Y Axis", columns)
    chart_type = st.selectbox("Chart Type", ["Scatter", "Bar", "Line"])
    if st.button("Generate Chart"):
        if chart_type == "Scatter":
            st.scatter_chart(data[[x_axis, y_axis]])
        elif chart_type == "Bar":
            st.bar_chart(data[[x_axis, y_axis]])
        elif chart_type == "Line":
            st.line_chart(data[[x_axis, y_axis]])
else:
    st.error("Failed to load data from Google Sheets.")
