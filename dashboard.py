import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')
st.set_page_config(page_title="Automobile Sales Dashboard", layout="wide")

# Set 'Agsunset' as the default color palette
pio.templates["custom"] = pio.templates["plotly"]
pio.templates["custom"]["layout"]["colorway"] = px.colors.sequential.Agsunset
pio.templates.default = "custom"

# Title
st.title("Automobile Sales Dashboard 🚘️")

# Sidebar Controls
st.sidebar.markdown("### Select Report Type:")
statistics_type = st.sidebar.radio("Select Report Type:",
                                   ["Yearly Statistics", "Recession Period Statistics"],
                                   label_visibility='collapsed')

# Enable year selection only if "Yearly Statistics" is selected
year = 1980
if statistics_type == "Yearly Statistics":
	st.sidebar.markdown("### Select Year:")
	year = st.sidebar.selectbox("Select Year:", data['Year'].unique(), label_visibility='collapsed')

# Display Data (Optional)
if st.sidebar.checkbox("Show Raw Data"):
	st.write(data)

# Recession Report Statistics
if statistics_type == "Recession Period Statistics":
	st.subheader("Recession Period Statistics 📉")
	recession_data = data[data['Recession'] == 1]
	
	# Chart 1: Average Automobile Sales Over Recession Period
	yearly_rec = recession_data.groupby('Year', as_index=False).Automobile_Sales.mean()
	fig1 = px.line(
		yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales During Recessions"
	).update_layout(yaxis_title='Automobile Sales')
	
	# Chart 2: Automobile Sales by Vehicle Type
	avg_sales = recession_data.groupby('Vehicle_Type', as_index=False).Automobile_Sales.mean()
	fig2 = px.bar(
		avg_sales, x='Vehicle_Type', y='Automobile_Sales', title='Sales by Vehicle Type'
	).update_layout(xaxis_title='Vehicle Type', yaxis_title='Automobile Sales').update_traces(marker_line_width=0)
	
	# Chart 3: Advertising Expenditure Share
	exp_rec = recession_data.groupby('Vehicle_Type', as_index=False).Advertising_Expenditure.sum()
	fig3 = px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title='Ad Spending Share')
	
	# Chart 4: Effect of Unemployment Rate on Sales
	unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'], as_index=False).Automobile_Sales.mean()
	fig4 = px.bar(
		unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', title='Unemployment Rate vs Sales'
	).update_layout(xaxis_title='Unemployment Rate', yaxis_title='Automobile Sales').update_traces(marker_line_width=0)
	
	# Display Charts in Two Columns
	col1, col2 = st.columns(2)
	col1.plotly_chart(fig1)
	col2.plotly_chart(fig2)
	col1.plotly_chart(fig3)
	col2.plotly_chart(fig4)

# Yearly Report Statistics
elif year:
	st.subheader(f"Yearly Statistics for {year} 📊")
	yearly_data = data[data['Year'] == year]
	
	# Chart 1: Annual Automobile Sales
	yas = data.groupby('Year', as_index=False)['Automobile_Sales'].mean()
	fig1 = px.line(
		yas, x='Year', y='Automobile_Sales', title='Annual Automobile Sales'
	).update_layout(yaxis_title='Automobile Sales')
	
	# Chart 2: Monthly Sales
	mas = data.groupby('Month', as_index=False)['Automobile_Sales'].mean()
	fig2 = px.line(
		mas, x='Month', y='Automobile_Sales', title='Monthly Automobile Sales'
	).update_layout(yaxis_title='Automobile Sales')
	
	# Chart 3: Vehicles Sold by Type in Selected Year
	avg_vehicle_sales = yearly_data.groupby('Vehicle_Type', as_index=False)['Automobile_Sales'].mean()
	fig3 = px.bar(
		avg_vehicle_sales, x='Vehicle_Type', y='Automobile_Sales', title=f'Vehicles Sold by Type in {year}'
	).update_layout(xaxis_title='Vehicle Type', yaxis_title='Automobile Sales').update_traces(marker_line_width=0)
	
	# Chart 4: Advertising Expenditure Share in Selected Year
	exp_yearly = yearly_data.groupby('Vehicle_Type', as_index=False).Advertising_Expenditure.sum()
	fig4 = px.pie(exp_yearly, values='Advertising_Expenditure', names='Vehicle_Type', title=f'Ad Spending Share in {year}')
	
	# Display Charts in Two Columns
	col1, col2 = st.columns(2)
	col1.plotly_chart(fig1)
	col2.plotly_chart(fig2)
	col1.plotly_chart(fig3)
	col2.plotly_chart(fig4)
