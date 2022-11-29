import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st

jasper_data = pd.read_csv('Jasper_Daily_Weather_Data.csv', encoding= 'unicode_escape')  #Importing the daily data
jasper_data['Date (Local Standard Time)'] = pd.to_datetime(jasper_data['Date (Local Standard Time)']) #Converting tbe 'Date (Local Standard Time)' row to Date time data type for easy use to bundle by week, month etc

jasper_data = jasper_data[(jasper_data['Air Temp. Min. Record Completeness (%)'] == 100)]   #Filtering Each completeness column and only taking rows with 100 in the specified column
jasper_data = jasper_data[jasper_data['Air Temp. Max. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Air Temp. Avg. Record Completeness (%)']  == 100]
jasper_data = jasper_data[jasper_data['Wind Speed 10 m Avg. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Wind Dir. 10 m Avg. Record Completeness (%)'] == 100]

avg_precip = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Precip. (mm)'].sum() #Sums the percipitation in each month
avg_temp = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Air Temp. Avg. (C)'].mean() #Does the avg monthly air temp from the daily averages
min_temp = min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'M'))['Air Temp. Min. (C)'].min()

fancy_page_stuff = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #face0c
}
</style>

"""

st.markdown(fancy_page_stuff, unsafe_allow_html=True)

option = st.multiselect(
    'What graphs would you like to display?',
    ['Precipitation', 'Average Temp', 'Min Temp'],
    []
)

fig1 = go.Figure()
fig2 = go.Figure()
fig3 = go.Figure()

if 'Precipitation' in option:
    fig1.add_trace(go.Scatter(
        x = pd.date_range("2019-10-03", "2022-11-03", freq='M'),
        y = avg_temp,
        mode='markers',
        marker=dict(
            color=avg_temp,
            colorscale="Viridis",
            size=avg_precip,
            colorbar = dict(
                title="Type"
            ),
        ),
    ))

    st.plotly_chart(fig1)

if 'Average Temp' in option:   
    fig2.add_trace(go.Scatter(
        x=pd.date_range("2019-10-03", "2022-11-03", freq='M'),
        y=avg_temp),
    )

    st.plotly_chart(fig2)

if 'Min Temp' in option:
    fig3.add_trace(go.Scatter(
        x=pd.date_range("2019-10-03", "2022-11-03", freq='M'),
        y=min_temp),
    )

    st.plotly_chart(fig3)