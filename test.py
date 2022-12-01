import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime as dt
from datetime import date

st.set_page_config(
    page_title = 'Project 3',
    page_icon = ':monkey:',
    layout = 'centered'
)


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
    background-image: url("https://cdn.getyourguide.com/img/location/5c9392236feff.jpeg/99.jpg");
}

[data-testid="stVerticalBlock"] {
    margin: auto;
    width: 50%;
    padding: 20px;
    background-color: #eef0af
}
</style>
"""

st.markdown(fancy_page_stuff, unsafe_allow_html=True)

current_time = start_time = dt.strftime(dt.now(),'%X') 
current_date = date.today().strftime("%B %d, %Y")

st.write(
    'The current date and time is: ',
    current_date,
    ' at ',
    current_time
)

option = st.multiselect(
    'What graphs would you like to display?',
    ['Precipitation', 'Average Temp', 'Min Temp'],
    []
)

fig1 = go.Figure()
fig2 = go.Figure()
fig3 = go.Figure()

if 'Precipitation' in option:
    st.info('Precipitation shown below')

    fig1.add_trace(go.Scatter(
        x = pd.date_range("2019-10-03", "2022-11-03", freq='M'),
        y = avg_temp,
        mode='markers',
        marker=dict(
            color=avg_temp,
            colorscale="Viridis",
            size=avg_precip,
            colorbar = dict(
                title="Temperature",
                tickvals = [-10,0,15],
                ticktext = ['Snow', 'Sleet', 'Rain']
            ),
        ),
    ))

    fig1.update_layout(
        title = "Precipitation",
        xaxis_title = 'Date',
        yaxis_title = 'Temperature',
        #paper_bgcolor = '#d692fc',
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)'
    )


    st.plotly_chart(fig1)

    with st.expander("Explanation"):
        st.write(
            'The above chart displays date vs temperature throughout each month from October 2019 to September 2022.',
            'The size of each bubble represents the ammount of precipitation in the month and the colour corresponds to the type of precipitation whether that is rain or snow.'
        )

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