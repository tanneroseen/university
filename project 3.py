import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mpld3

'''
Step One importing Data and Filtering through Data and Creating the figure
Data Set Chosen: Daily Weather Recordings from the Jasper Warden Station in Jasper National Park.
Outlines Dates from October 3rd, 2019 until October 3rd, 2022 (Well over 1000 rows and more then 2 columns as per the project outlines)

In the csv it given the completness of each measurement given in percentage, and we are only intererested in 100% complete data so we
must filter through and romove any columns with any of the five completeness percentage that aren't 100
'''

jasper_data = pd.read_csv('Jasper_Daily_Weather_Data.csv', encoding= 'unicode_escape')  #Importing the daily data
jasper_data['Date (Local Standard Time)'] = pd.to_datetime(jasper_data['Date (Local Standard Time)']) #Converting tbe 'Date (Local Standard Time)' row to Date time data type for easy use to bundle by week, month etc

jasper_data = jasper_data[(jasper_data['Air Temp. Min. Record Completeness (%)'] == 100)]   #Filtering Each completeness column and only taking rows with 100 in the specified column
jasper_data = jasper_data[jasper_data['Air Temp. Max. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Air Temp. Avg. Record Completeness (%)']  == 100]
jasper_data = jasper_data[jasper_data['Wind Speed 10 m Avg. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Wind Dir. 10 m Avg. Record Completeness (%)'] == 100]

'''
Step Two:
Graphing The average wind speed and average direction of the wind each month to draw conclusions as to how wind speed varies month to month
This will be done on a polar plot as to denote the magnitude of the wind speed and the direction of the wind
Inspiration for this graph is cited below
Note not showing each month with the data point was intentional this graph more or less attempts to display the wind variation across the months in the three years
Gavin's Portion
'''
fig = plt.figure(figsize = [15,10]) #Creates the figure for everything to be graphed on
fig.suptitle('Daily Weather Data Recorded in Jasper National Park', family = 'Times New Roman', size = 15) #creates a title for the entire figure outlining the data set

monthly_average_windspeed = jasper_data.groupby(pd.Grouper(key='Date (Local Standard Time)',freq='MS'))['Wind Speed 10 m Avg. (km/h)'].mean().reset_index()   #Groups wind speed data by the respective month and takes the average of it
monthly_average_windspeed_direction = jasper_data.groupby(pd.Grouper(key='Date (Local Standard Time)',freq='MS'))['Wind Dir. 10 m Avg. '].mean().reset_index() #groups wind direction average in each month and takes the average of all days avg direction

r = monthly_average_windspeed['Wind Speed 10 m Avg. (km/h)'] #Makes the magnitude of the polar plot the monthly avg windspeed
theta = monthly_average_windspeed_direction['Wind Dir. 10 m Avg. '] #makes the angle (or poisiton on the polar plot the avg direction for each month)
colors = r

ax1 = fig.add_subplot(221, projection='polar')  #adds a subplot for the graph in the figure first spot of 2x2 grid
ax1.set

ax1.set_theta_zero_location('N')    #Sets zero degrees on the plot to represent geographic north (as wind measurements to take North as 0 degrees, NE as 45, E as 90, etc)
ax1.set_theta_direction(-1)
c = ax1.scatter(theta, r, c = r, cmap='plasma')   #creates the plot specifying the angle (theta) the magnitude of wind speed (r) what to base the color map off of (the magnitude r) and the type of colormap used

#Formatting the graph
ax1.set_title('Monthly Average Wind Speed and Direction', family = 'Times New Roman', size = 12, pad = 5)
ax1.set_rmin(4)
ax1.set_rmax(10)
ax1.set_xticks(ax1.get_xticks()) #Sets a FixedLocator for the Fixed Values I set below (Gets rid of warning)
ax1.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']) #Labels the corresponding angles (0, 45, 90, 135, 180, 225, 270, 315, 360) as thier geographical counterparts
ax1.set_thetamin(0)
ax1.set_thetamax(360)
ax1.tick_params('x', size = 2)
ax1.set_rlabel_position(25) #sets the magnitude label postion at 25 degrees

cbar = fig.colorbar(c) #adds the colour bar to the plot
cbar.set_label('Wind Speed Range (km/h)', family = 'Times New Roman') #labels the colorbar

'''
Step 3:
Plotting a scatter plot displaying the monthly average temperature as well as the corresponding months total percipitation
and given these two variables a colormap displaying the corresponding phase of the percipitation in the given month
(ranging from snow on the cold end to sleet inbetween and rain on the high temp end)
Tanner's Portion
'''

avg_precip = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Precip. (mm)'].sum() #Sums the percipitation in each month
avg_temp = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Air Temp. Avg. (C)'].mean() #Does the avg monthly air temp from the daily averages

ax2 = fig.add_subplot(222) #adds a subplot for the graph in the figure (2nd spot in 2x2 grid)
cax = plt.scatter(pd.date_range("2019-10-03", "2022-11-03", freq='M'), avg_temp, s = avg_precip, c = avg_temp, cmap= 'winter')

plt.legend(*cax.legend_elements("sizes", num=4), loc='lower right', title='Precipitation (mm)', title_fontsize = 6 ,fontsize = 6) #creates a legend to show how size of point depicts percipitation amount

cbar = fig.colorbar(cax, ticks=[-13,0,17]) #sets up a color bar for the plot for the average temp ticks param gives the low range mid range and high range of the color bar
cbar.ax.set_yticklabels(['Snow','Sleet','Rain']) #labels the three ranges of the color bar

plt.axhline(color='k', alpha=0.25) #creats a horizontal line at zero degrees marks freezing point
plt.xlabel('Date', family = 'Times New Roman', size = 10)
plt.ylabel('Temperature (\u00B0C)', family = 'Times New Roman', size = 10)
plt.title('Monthly Average Temperature and Monthly Total Precipitation', family = 'Times New Roman', size = 12, pad = 5)
plt.tick_params(axis = 'x', labelsize = 5)


'''
Step 4:
Take the daily min max and average temp and group it into the calendar week sunday until following saturday (inclusive) and graph:
the max of the maximum temperatures in the week
the min of the minimum temperatures in the week
and the difference between these extremes for each week
Reid's Portion
'''

ax3 = fig.add_subplot(212) #adds a subplot for the graph in the figure (2nd spot in 2x1 grid)

#Manipulating the data from the CSV to give insight
min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Min. (C)'].min() #On graph date shown is end of the week
max_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Max. (C)'].max()
differce_in_max_and_min = max_grouped_by_week - min_grouped_by_week


#Plots the data with time
min_grouped_by_week.plot(style = '.-', color = 'royalblue', label = 'Minimum', alpha = 0.4, axes = ax3)
max_grouped_by_week.plot(style = '.-', color = 'r', label = 'Maximum', alpha = 0.4, axes = ax3)
differce_in_max_and_min.plot(style ='.-', color = 'limegreen', label = 'Difference', alpha = 1, axes = ax3)


#Formatting the Graph
plt.title('Weekly Temperature Extremes and their Difference', family = 'Times New Roman', size = 12, pad = 5)
plt.xlabel('Date', family = 'Times New Roman', size = 10)
plt.ylabel('Temperature (\u00B0C)', family = 'Times New Roman', size = 10)
plt.axhline(color = 'k', alpha = 0.25) #creates line at temperature of 0 degrees celcius (freezing temp)
plt.minorticks_on()
plt.legend(loc = 'lower right', shadow = True)
plt.tick_params(axis = 'both', labelsize = 8)

st.pyplot(fig)
