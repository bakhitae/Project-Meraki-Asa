# -------------------------------------- Import Library ------------------------------
import plotly.express as px
import pandas as pd
import streamlit as st

# ------------------------------ CONFIG ------------------------------
st.set_page_config(
    page_title="Analysis of Vehicle Sales Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# -------------------------------------- Read dataset ------------------------------
df = pd.read_pickle("data_car_prices.pkl.gz")
# -------------------------------------- Membuat Sidebar --------------------
with st.sidebar:
    # Menambahkan Logo Pribadi
    st.write("Hi there! 👋 Welcome to my Dashboard!")
    st.image("data-science.png")
    st.write("""
             I'm Bakhita Iklil Endrizal and I proudly present the Vehicle Sales Data Analysis Dashboard, which is an innovative tool designed to 
             streamline data analysis with dynamic and interactive visualizations. Explore valuable insights and uncover key trends 
             within our company's data.
             """)
    st.caption('Copyright © Bakhita Iklil Endrizal 2024')
    
# -------------------------------------- ROW 1 --------------------
st.write("# Analysis of Car Prices Dashboard")
st.write("""
         This analysis uses Python programming and interactive visualizations using Plotly Express. 
         The dataset used for this project is supermarket sales data, sourced from 
         https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data.
         """)
with st.expander("Click to look at the detailed dataset!"):
    st.write("Vehicle Sales Data",df)
    

# -------------------------------------- ROW 2 --------------------

# Convert 'saledate' to datetime format, coercing errors to NaT
df['saledate'] = pd.to_datetime(df['saledate'], errors='coerce')

# Drop rows with NaT in 'saledate' (if there are any)
df = df.dropna(subset=['saledate'])

# ---------- A. Filter Indicator
st.write("### 1. How is the Company's (model_year, make, body) Performance in a Certain Time Range?")
choices = st.radio("Pick One Indicator!", ["model_year", "make", "body"])

# ----------- B. Filter Date - Input Rentang Tanggal
min_date = df['saledate'].min()
max_date = df['saledate'].max()

# Input Date
start_date, end_date = st.date_input("Pick a Date Range!", value=[min_date, max_date], min_value=min_date, max_value=max_date)
# Ubah tipe data input date
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
# Filter data
cond_min_max = (df['saledate'] >= start_date) & (df['saledate'] <= end_date)
filtered_df = df[cond_min_max]

# --------------- C. Persiapan Data
trend = filtered_df.groupby("saledate")[choices].sum().reset_index()

# ---------- D. Count the selected indicator's distribution
indicator_distribution = df[choices.lower()].value_counts().reset_index()
indicator_distribution.columns = [choices, 'Count']  # Rename columns

# ---------- E. Create the bar chart with Plotly Express
fig_bar = px.bar(indicator_distribution,
                 x=choices,
                 y='Count',
                 title=f"Distribution of {choices}",
                 color=choices,
                 labels={choices: choices, 'Count': 'Number of Cars'},
                 height=400)

# ---------- F. Display the chart in Streamlit
st.plotly_chart(fig_bar)

# -------------------------------------- ROW 3 --------------------

st.write("### 2. What is the distribution of Cars by Make and Transmission on their Condition?")

# A. Input Choices
# Dropdown to select
category_choice = st.selectbox("Pick One Indicator!", ["Make", "Transmission"])
if category_choice == "Make":
    CMM = pd.crosstab(df["condition"], df["make"])
else:  # If Transmission is chosen, create a cross-tab based on 'Condition' and 'Transmission'
    CMM = pd.crosstab(df["condition"], df["transmission"])

# B. Create the line chart
fig_line = px.line(CMM,
                   title=f"Distribution of Cars by Condition and {category_choice}",
                   labels={"index": "Condition", "value": f"{category_choice} Count"},
                   markers=True)

# C. Display the chart in Streamlit
st.plotly_chart(fig_line)


# -------------------------------------- ROW 4 --------------------
st.write("### 3. How is the Distribution of Selling Price in Every Hour and Day?")

# A. Persiapan Data - Group by 'Day of Week' and 'Hour' and 'Selling Price'
persebaran_day_hour = df.groupby(["day_of_week", "hour"])['sellingprice'].sum().reset_index()

# B. Visualisasi Heatmap
fig_heatmap = px.density_heatmap(persebaran_day_hour,
                   x="day_of_week",
                   y="hour",
                   z="sellingprice",
                   title="Distribution of Total Selling Price in Every Hour and Day",
                   color_continuous_scale="rdbu",  # You can choose other color scales
                   nbinsy=len(persebaran_day_hour['hour'].unique()))  # Number of bins for the y-axis (Hour)

# C. Display the heatmap in Streamlit
st.plotly_chart(fig_heatmap)

# -------------------------------------- ROW 5 --------------------
# Group by car make and sum the selling price
st.write("### 4. How much is the Total Selling Price based on the Car Brand (make)?")

big_pl = df.groupby("make")['sellingprice'].sum().reset_index()

# Sort the data by total selling price in ascending order
big_pl_sorted = big_pl.sort_values(by="sellingprice", ascending=True)

# Create a bar chart
fig_bar = px.bar(big_pl_sorted,
                 x="sellingprice",
                 y="make",
                 title="Total Sales by Car Make",
                 color_discrete_sequence=['blue'],
                 labels={"sellingprice": "Total Selling Price", "make": "Car Make"})

# Display the bar chart
st.plotly_chart(fig_bar)

