import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Dataset/cleaned_kwanza_tukule_data.csv")  # Replace with your actual dataset

data = load_data()

# Streamlit app layout
st.title("Kwanza Tukule Sales Dashboard")

# Total Quantity & Value by Category
st.subheader("Total Quantity and Value by Category")
category_summary = data.groupby('ANONYMIZED CATEGORY').agg(
    total_quantity=('QUANTITY', 'sum'),
    total_value=('VALUE', 'sum')
).reset_index()

fig1 = px.bar(category_summary, x='ANONYMIZED CATEGORY', y=['total_quantity', 'total_value'],
              title="Total Quantity and Value by Category", barmode='group')

st.plotly_chart(fig1)

# Top-performing products
st.subheader("Top Performing Products")
top_products = data.groupby('ANONYMIZED PRODUCT')['VALUE'].sum().reset_index().sort_values(by="VALUE", ascending=False).head(10)
fig2 = px.bar(top_products, x='ANONYMIZED PRODUCT', y='VALUE', title="Top 10 Products by Sales Value")

st.plotly_chart(fig2)

# Time-Series Sales Trends
st.subheader("Sales Trends Over Time")
time_series = data.groupby('Month-Year')['VALUE'].sum().reset_index()
fig3 = px.line(time_series, x='Month-Year', y='VALUE', title="Sales Value Over Time")

st.plotly_chart(fig3)

# Customer Segmentation
st.subheader("Customer Segmentation")
top_businesses = data.groupby('ANONYMIZED BUSINESS')['VALUE'].sum().reset_index().sort_values(by="VALUE", ascending=False).head(10)
fig4 = px.pie(top_businesses, names='ANONYMIZED BUSINESS', values='VALUE', title="Top Businesses by Sales Value")

st.plotly_chart(fig4)
