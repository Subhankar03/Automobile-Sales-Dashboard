import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
data = pd.read_csv(DATA_URL)

# Set page config
st.set_page_config(page_title="Automobile Sales Dashboard", layout="wide")

# Custom Agsunset Color Palette
agsunset_colors = px.colors.sequential.Agsunset

# Title
st.title("🚗 Automobile Sales Statistics Dashboard")

# Sidebar Controls
st.sidebar.header("Filters")
statistics_type = st.sidebar.radio("Select Report Type:", ["Yearly Statistics", "Recession Period Statistics"])

# Enable year selection only if "Yearly Statistics" is selected
year = None
if statistics_type == "Yearly Statistics":
	year = st.sidebar.selectbox("Select Year:", list(range(1980, 2024)))

# Display Data (Optional)
if st.sidebar.checkbox("Show Raw Data"):
	st.write(data)

# Recession Report Statistics
if statistics_type == "Recession Period Statistics":
	st.subheader("📉 Recession Period Statistics")
	
	# Filter Data
	recession_data = data[data['Recession'] == 1]
	
	# Chart 1: Average Automobile Sales Over Recession Period
	yearly_rec = recession_data.groupby('Year', as_index=False).Automobile_Sales.mean()
	fig1 = px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales During Recessions",
	               color_discrete_sequence=agsunset_colors)
	
	# Chart 2: Automobile Sales by Vehicle Type
	avg_sales = recession_data.groupby('Vehicle_Type', as_index=False).Automobile_Sales.mean()
	fig2 = px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales', title='Sales by Vehicle Type (Recession)',
	              color_discrete_sequence=agsunset_colors)
	
	# Chart 3: Advertising Expenditure Share
	exp_rec = recession_data.groupby('Vehicle_Type', as_index=False).Advertising_Expenditure.sum()
	fig3 = px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
	              title='Ad Spending Share (Recession)', color_discrete_sequence=agsunset_colors)
	
	# Chart 4: Effect of Unemployment Rate on Sales
	unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'], as_index=False).Automobile_Sales.mean()
	fig4 = px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', title='Unemployment Rate vs Sales',
	              color_discrete_sequence=agsunset_colors)
	
	# Display Charts in Two Columns
	col1, col2 = st.columns(2)
	col1.plotly_chart(fig1, use_container_width=True)
	col2.plotly_chart(fig2, use_container_width=True)
	col1.plotly_chart(fig3, use_container_width=True)
	col2.plotly_chart(fig4, use_container_width=True)

# Yearly Report Statistics
elif year:
	st.subheader(f"📊 Yearly Statistics for {year}")
	
	# Filter Data
	yearly_data = data[data['Year'] == year]
	
	# Chart 1: Annual Automobile Sales
	yas = data.groupby('Year', as_index=False)['Automobile_Sales'].mean()
	fig1 = px.line(yas, x='Year', y='Automobile_Sales', title='Annual Automobile Sales',
	               color_discrete_sequence=agsunset_colors)
	
	# Chart 2: Monthly Sales
	mas = data.groupby('Month', as_index=False)['Automobile_Sales'].mean()
	fig2 = px.line(mas, x='Month', y='Automobile_Sales', title='Monthly Automobile Sales',
	               color_discrete_sequence=agsunset_colors)
	
	# Chart 3: Vehicles Sold by Type in Selected Year
	avg_vehicle_sales = yearly_data.groupby('Vehicle_Type', as_index=False)['Automobile_Sales'].mean()
	fig3 = px.bar(avg_vehicle_sales, x='Vehicle_Type', y='Automobile_Sales', title=f'Vehicles Sold by Type in {year}',
	              color_discrete_sequence=agsunset_colors)
	
	# Chart 4: Advertising Expenditure Share in Selected Year
	exp_yearly = yearly_data.groupby('Vehicle_Type', as_index=False).Advertising_Expenditure.sum()
	fig4 = px.pie(exp_yearly, values='Advertising_Expenditure', names='Vehicle_Type',
	              title=f'Ad Spending Share in {year}', color_discrete_sequence=agsunset_colors)
	
	# Display Charts in Two Columns
	col1, col2 = st.columns(2)
	col1.plotly_chart(fig1, use_container_width=True)
	col2.plotly_chart(fig2, use_container_width=True)
	col1.plotly_chart(fig3, use_container_width=True)
	col2.plotly_chart(fig4, use_container_width=True)
