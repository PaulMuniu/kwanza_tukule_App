import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit Page Configuration
st.set_page_config(page_title="Kwanza Tukule Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_kwanza_tukule_data.csv")  # Replace with your cleaned dataset

data = load_data()

# ---- SIDEBAR ----
st.sidebar.header("Filter Data")
category_filter = st.sidebar.multiselect("Select Category", data["ANONYMIZED CATEGORY"].unique(), default=data["ANONYMIZED CATEGORY"].unique())
business_filter = st.sidebar.multiselect("Select Business", data["ANONYMIZED BUSINESS"].unique(), default=data["ANONYMIZED BUSINESS"].unique())

# Apply Filters
filtered_data = data[(data["ANONYMIZED CATEGORY"].isin(category_filter)) & (data["ANONYMIZED BUSINESS"].isin(business_filter))]

# ---- MAIN DASHBOARD ----
st.title("📊 Kwanza Tukule Sales Dashboard")

# **1. Summary Metrics**
st.subheader("🔹 Key Sales Metrics")
total_quantity = filtered_data["QUANTITY"].sum()
total_value = filtered_data["VALUE"].sum()

col1, col2 = st.columns(2)
col1.metric(label="📦 Total Quantity Sold", value=f"{total_quantity:,}")
col2.metric(label="💰 Total Sales Value", value=f"Ksh {total_value:,.2f}")

# **2. Total Quantity & Sales Value by Category**
st.subheader("📌 Sales by Category")
category_summary = filtered_data.groupby('ANONYMIZED CATEGORY').agg(
    total_quantity=('QUANTITY', 'sum'),
    total_value=('VALUE', 'sum')
).reset_index()

fig1 = px.bar(category_summary, x='ANONYMIZED CATEGORY', y=['total_quantity', 'total_value'], 
              title="Total Quantity and Sales Value by Category", barmode='group', color_discrete_sequence=["#636EFA", "#EF553B"])
st.plotly_chart(fig1, use_container_width=True)

# **3. Top Performing Products**
st.subheader("🏆 Top Performing Products")
top_products = filtered_data.groupby('ANONYMIZED PRODUCT')['VALUE'].sum().reset_index().sort_values(by="VALUE", ascending=False).head(10)

fig2 = px.bar(top_products, x='ANONYMIZED PRODUCT', y='VALUE', title="Top 10 Products by Sales Value", color='VALUE',
              color_continuous_scale="blues")
st.plotly_chart(fig2, use_container_width=True)

# **4. Sales Trends Over Time**
st.subheader("📈 Sales Trends")
time_series = filtered_data.groupby('Month-Year')['VALUE'].sum().reset_index()
time_series["Month-Year"] = pd.to_datetime(time_series["Month-Year"])

fig3 = px.line(time_series, x='Month-Year', y='VALUE', title="Sales Value Over Time", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# **5. Customer Segmentation**
st.subheader("🎯 Customer Segmentation")
top_businesses = filtered_data.groupby('ANONYMIZED BUSINESS')['VALUE'].sum().reset_index().sort_values(by="VALUE", ascending=False).head(10)

fig4 = px.pie(top_businesses, names='ANONYMIZED BUSINESS', values='VALUE', title="Top Businesses by Total Sales")
st.plotly_chart(fig4, use_container_width=True)

# **6. Footer**
st.markdown("---")
st.markdown("Developed by **[Your Name]** | Powered by Streamlit & Plotly")