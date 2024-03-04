import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


all_df = pd.read_csv("data/all_data.csv")

# Helper Function untuk menunjukkan jumlah penjualan produk berdasarkan kategori
def create_sales_product_df():
    sales_product_df = all_df.groupby(by="product_category_name").agg(total_sales=("order_item_id", "sum")).reset_index()
    return sales_product_df

# Helper Function untuk menunjukkan pelanggan teratas berdasarkan jumlah pembelian
def create_top_customer_df(top = 5):
    all_df["total_purchases"] = all_df.groupby("customer_unique_id")["order_id"].transform("nunique")
    all_df["total_purchases"] = all_df["total_purchases"].astype(int)
    top_customer_df = all_df.groupby("customer_unique_id").agg(total_purchases=("total_purchases", "first")).nlargest(top, "total_purchases").reset_index()
    return top_customer_df


# Helper Function untuk menunjukkan total penjualan berdasarkan state
def create_sales_by_state_df():
    sales_by_state_df = all_df.groupby(by="customer_state").agg(total_sales=("price", "sum")).reset_index()
    return sales_by_state_df

# Memanggil Helper
sales_product_df = create_sales_product_df()
top_customer_df = create_top_customer_df()
sales_by_state_df = create_sales_by_state_df()

st.header('E-Commerce Public Dashboard :sparkles:')

content = """
Data diambil dari E-Commerce Public Dataset
"""
with st.sidebar:
    st.markdown(content)

# Visualization The Most Sales Product
st.subheader("5 Kategori Produk Teratas Berdasarkan Penjualan")
st.write("Kategori produk teratas yang paling banyak jual dalam E-Commerce Public yaitu agro_industria_e_comercio, alimentos, alimentos_bebidas, artes, artes_e_artesanato untuk lebih detailnya dapat dilihat dari grafik dibawah ini. Pada grafik ini alimentos adalah produk yang paling banyak dijual.")
top_categories = sales_product_df.head(5)
plt.figure(figsize=(10, 6))
sns.barplot(x='total_sales', y='product_category_name', data=top_categories, palette='viridis')
plt.xlabel('Total Penjualan')
plt.ylabel('Kategori Produk')
st.pyplot(plt)

# Visualization Top 5 Customer Based on Number of Purchases
st.subheader("5 Pelanggan Teratas Berdasarkan Jumlah Pembelian")
st.write("Pelanggan pada E-commerce memiliki tingkat jumlah pembelian yang tinggi, dibawah ini adalah beberapa pelanggan dengan Jumlah pembelian tertinggi.")
plt.figure(figsize=(8, 6))
plt.barh(top_customer_df['customer_unique_id'], top_customer_df['total_purchases'], color='#72BCD4')
plt.xlabel('Jumlah Pembelian')
plt.ylabel('Customer Unique ID')
st.pyplot(plt)

# Visualization Total of All Sales by State
st.subheader("Total Semua Penjualan Berdasarkan State")
st.write("Beberapa state memiliki total penjualan tertinggi tetapi juga ada banyak state yang memiliki total penjualan yang rendah, dibawah ini adalah daftar total penjual state dari yang terendah hingga yang tertinggi.")
plt.figure(figsize=(10, 6))
sns.lineplot(x='customer_state', y='total_sales', data=sales_by_state_df, marker='o', color='#72BCD4')
plt.xlabel('State')
plt.ylabel('Total Penjualan')
plt.xticks(rotation=45)
st.pyplot(plt)

st.caption('Copyright (c) Jeki 2024')