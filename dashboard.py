import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.image as mpimg

# Load dataset
@st.cache_data
def load_data():
    all_df = pd.read_csv('all_data.csv')
    customer = pd.read_csv('dataset/olist_customers_dataset.csv')
    geolocation = pd.read_csv('dataset/olist_geolocation_dataset.csv')
    return all_df, customer, geolocation

all_df, customer, geolocation = load_data()

# Dashboard UI
st.title("📊 Dashboard Analisis Data Olist")

# Produk Terlaris
st.header("🔥 Produk Terlaris dan Kurang Laris")
product_count = all_df.groupby('product_category_name_english').product_id.count().reset_index()
sorted_product = product_count.sort_values(by='product_id', ascending=False)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name_english", data=sorted_product.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk dengan Penjualan Tertinggi", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

sns.barplot(x="product_id", y="product_category_name_english", data=sorted_product.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk dengan Penjualan Terendah", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Status Pengiriman
st.header("🚚 Status Pengiriman")
delivery_status = all_df['order_status'].value_counts().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=delivery_status.index, y=delivery_status.values, order=delivery_status.index, palette=colors, ax=ax)
ax.set_title("Status Pengiriman yang Berhasil", fontsize=15)
ax.set_xlabel("Status Pengiriman")
ax.set_ylabel("Jumlah")
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

# Lokasi dengan Jumlah Pelanggan Terbanyak
st.header("📍 Lokasi dengan Jumlah Pelanggan Terbanyak")
customers_location = customer.merge(geolocation, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='inner')
brazil = mpimg.imread('brazil-map.jpeg')
fig, ax = plt.subplots(figsize=(10, 10))
customers_location.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", alpha=0.3, s=0.3, c='green', ax=ax)
ax.imshow(brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
ax.set_title('Lokasi dengan Jumlah Pelanggan Terbanyak')
ax.axis('off')
st.pyplot(fig)
