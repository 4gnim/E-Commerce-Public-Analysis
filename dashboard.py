import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Analisis Data E-Commerce")

# Load Data
data = pd.read_csv('all_data.csv')

# Konversi kolom tanggal
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'])

# Sidebar untuk filter interaktif
st.sidebar.header("Filter Data")

# Filter berdasarkan rentang tanggal
min_date = data['order_purchase_timestamp'].min()
max_date = data['order_purchase_timestamp'].max()
default_start_date = max_date - pd.DateOffset(months=6)
default_end_date = max_date
date_range = st.sidebar.date_input("Pilih Rentang Tanggal:", [default_start_date, default_end_date])

if len(date_range) == 2:
    data = data[(data['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
                (data['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))]

# Filter berdasarkan kategori produk
product_categories = data['product_category_name_english'].unique()
selected_categories = st.sidebar.multiselect("Pilih Kategori Produk:", options=product_categories, default=product_categories)
data = data[data['product_category_name_english'].isin(selected_categories)]

# Filter berdasarkan wilayah
states = data['customer_state'].dropna().unique()
selected_states = st.sidebar.multiselect("Pilih Wilayah:", options=states, default=states)
data = data[data['customer_state'].isin(selected_states)]

# Visualisasi: 10 Produk Terlaris dalam 6 Bulan Terakhir
if 'product_category_name_english' in data.columns and 'order_id' in data.columns:
    st.subheader("Top 10 Produk dengan Transaksi Terbanyak (6 Bulan Terakhir)")
    product_sales = data.groupby('product_category_name_english').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='product_category_name_english', data=product_sales)
    plt.xlabel('Jumlah Transaksi')
    plt.ylabel('Nama Produk')
    plt.title('10 Produk Terlaris dalam 6 Bulan Terakhir')
    st.pyplot(plt)

# Visualisasi: Distribusi Skor Ulasan
if 'review_score' in data.columns:
    st.subheader("Distribusi dan Faktor yang Mempengaruhi Skor Ulasan Pelanggan")
    plt.figure(figsize=(6, 4))
    sns.boxplot(x=data['review_score'])
    plt.title('Boxplot Distribusi Skor Ulasan')
    plt.xlabel('Skor Ulasan')
    st.pyplot(plt)

# Visualisasi: Distribusi Skor Ulasan Berdasarkan Kategori Waktu Pengiriman
if 'order_delivered_customer_date' in data.columns and 'order_purchase_timestamp' in data.columns and 'review_score' in data.columns:
    data['actual_delivery_time'] = (data['order_delivered_customer_date'] - data['order_purchase_timestamp']).dt.days
    data['delivery_category'] = pd.qcut(data['actual_delivery_time'], q=4, labels=["Sangat Cepat", "Cepat", "Lambat", "Sangat Lambat"])
    plt.figure(figsize=(8, 5))
    ax = sns.boxplot(x='delivery_category', y='review_score', data=data, palette="Set2")
    medians = data.groupby("delivery_category")["review_score"].median()
    for i, median in enumerate(medians):
        ax.text(i, median + 0.1, f"{median:.1f}", horizontalalignment='center', fontsize=12, color='black')
    plt.title("Distribusi Skor Ulasan Berdasarkan Kategori Waktu Pengiriman")
    plt.xlabel("Kategori Waktu Pengiriman")
    plt.ylabel("Skor Ulasan")
    st.pyplot(plt)

# Visualisasi: Distribusi Skor Ulasan Berdasarkan Kategori Harga Produk
if 'price' in data.columns and 'review_score' in data.columns:
    data['price_category'] = pd.qcut(data['price'], q=4, labels=['Murah', 'Menengah', 'Mahal', 'Sangat Mahal'])
    plt.figure(figsize=(9, 6))
    sns.boxplot(x='price_category', y='review_score', data=data, palette='viridis')
    plt.title("Distribusi Skor Ulasan Berdasarkan Kategori Harga Produk", fontsize=14, fontweight='bold')
    plt.xlabel("Kategori Harga Produk", fontsize=12)
    plt.ylabel("Skor Ulasan", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(plt)

# Visualisasi: 10 Wilayah dengan Pesanan Terbanyak
if 'customer_state' in data.columns:
    st.subheader("Top 10 Wilayah dengan Jumlah Pesanan Terbanyak (1 Tahun Terakhir)")
    state_names = {
        "SP": "São Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais", "RS": "Rio Grande do Sul", "PR": "Paraná",
        "SC": "Santa Catarina", "BA": "Bahia", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás"
    }
    data['customer_state'] = data['customer_state'].map(state_names)
    top_states = data['customer_state'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_states.values, y=top_states.index, palette='Set2')
    plt.xlabel("Jumlah Pesanan")
    plt.ylabel("Provinsi")
    plt.title("10 Wilayah dengan Pesanan Terbanyak")
    st.pyplot(plt)

st.write("\n**Catatan:** Gunakan filter di sidebar untuk menyesuaikan data visualisasi.")
