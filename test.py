import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime as dt
from datetime import date
import pytz

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
min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'M'))['Air Temp. Min. (C)'].min()
max_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Max. (C)'].max()
date_range = min_grouped_by_week.keys() #grabs each date (start of each week grouped by) that is used by all graphs as common x-values
differce_in_max_and_min = max_grouped_by_week - min_grouped_by_week

fancy_page_stuff = """
<style>
[data-testid="stAppViewContainer"] > .main{
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/007/515/187/original/timelapse-of-beautiful-blue-sky-in-pure-daylight-with-puffy-fluffy-white-clouds-background-amazing-flying-through-beautiful-thick-fluffy-clouds-nature-and-cloudscape-concept-free-video.jpg');
    background-size: 300%;
}

[data-testid="stVerticalBlock"] {
    margin: auto;
    width: 750px;
    padding: 20px;
    background-color: rgba(255,255,255,0.6)
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0)
}

[data-testid="stToolbar"] {
    right: 2rem
}
</style>
"""

st.markdown(fancy_page_stuff, unsafe_allow_html=True)

#current_time = start_time = dt.strftime(dt.now(pytz.timezone('Canada/Mountain')),'%X') 
#current_date = date.today().strftime("%B %d, %Y")

now = dt.now(pytz.timezone('Canada/Mountain')).strftime('%B %d, %Y %X')

st.write(
    'The current date and time is: ',
    now
)

option = st.multiselect(
    'What graphs would you like to display?',
    ['Precipitation', 'Temperature', 'Wind'],
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
        plot_bgcolor = 'rgba(0,0,0,0.2)',
        paper_bgcolor = 'rgba(0,0,0,0)'
    )


    st.plotly_chart(fig1)

    with st.expander("Explanation"):
        st.write(
            'The above chart displays date vs temperature throughout each month from October 2019 to September 2022.',
            'The size of each bubble represents the ammount of precipitation in the month and the colour corresponds to the type of precipitation whether that is rain or snow.'
        )

if 'Temperature' in option:   
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x = date_range,
        y = [0 for i in range(len(date_range))],
        name = '0\u00B0 C',
        opacity = 0.5,
        line = dict(color = 'black')
        ))
    fig3.add_trace(go.Scatter(
        x = date_range,
        y = min_grouped_by_week,
        name = 'Minimum Temperature',
        mode = "lines+markers",
        line = dict(color = '#0000FF')
        ))
    fig3.add_trace(go.Scatter(
        x = date_range,
        y = max_grouped_by_week,
        name = 'Maximum Temperature',
        mode = 'lines+markers',
        line = dict(color = '#FF0000')
        ))
    fig3.add_trace(go.Scatter(
        x = date_range,
        y = differce_in_max_and_min,
        name = 'Difference in Min and Max Temperatures',
        mode = 'lines+markers',
        line = dict(color = '#00FF00')
        ))
    fig3.update_layout(
        title = 'Weekly Temperature Extremes and their Difference',
        xaxis_title = 'Date',
        yaxis_title = 'Temperature (\u00B0C)',
        plot_bgcolor = 'rgba(0,0,0,0.2)',
        paper_bgcolor = 'rgba(0,0,0,0)'
        )

    st.plotly_chart(fig3)

if 'Wind' in option:
    fig2.add_trace(go.Scatter(
        x=pd.date_range("2019-10-03", "2022-11-03", freq='M'),
        y=min_grouped_by_week),
    )

    st.plotly_chart(fig2)