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
min_temp = min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'M'))['Air Temp. Min. (C)'].min()

fancy_page_stuff = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVEhgVFRYYGBgYGBgYGBgZGRgYGBgYGBgZGRgaGBgcIS4lHB4rIRgYJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QHxISHzQrJCs0NDQ0NDQ0NDQ6NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NP/AABEIALcBEwMBIgACEQEDEQH/xAAbAAACAwEBAQAAAAAAAAAAAAACAwABBAUGB//EADMQAAICAAUCBQMEAgAHAAAAAAECABEDBBIhMUFRBRNhcYEikaEyscHw0eEUQlJicpLx/8QAGgEAAwEBAQEAAAAAAAAAAAAAAAECAwQFBv/EACgRAAICAgIBAwQCAwAAAAAAAAABAhESIQMxURMiQWFxkeEEsRQyQv/aAAwDAQACEQMRAD8A+aKsYqwlWMRZ9CkeY5AqsdhrIFjUSWkZSkGqS9FQlNSSkjG2Qw1EoLGKsqiZMenEF2qVqi2joyS2MDXD2iBDEY2h1wGMGzJcCUgkWzKZd4SGoR3gF7BN1FmNYQDGCZAsgENDBqAWWpjkMWqxyJAiTRpy41UD0m/KOoJG+1CIyeVNj1nTRET9dXMJtdG/FF9mhgSNpS5RghJXf9r4mjIZvDuz0G1y8x4sBf7dJz+66SOv21bYrH8RKqFJ4X8jtOcAcRWfUABsDf79uJmzJLEsTseP9RSu6rpA2/max40lrs5pczbp9GzDxCh6N6jtOpks+zEWpHqJyMsu1/eb0OkfSKu6IMmcUzXik+zdn8qriyxLVwZkyGUTDUs66tR9yO1RuDhseW35mzI4Zojm/kiYtuMas3SUpZUXmM2ukChxsT/MX5DPTBxp5qdBvDVrU259YtMroXbcH7DvMslWjXF/Jl8v/wAf/YSTq4WQsDapJPqIrFnw1VhqsOoSrPTSOJyKVYYEJVh6JSRm5FAQgJAIYEqiGygIayqhgRkNlGVUKpKhQWUoj0SAizSgjM5SElYIUCPI7SgsBKQAWQjaoRkCxBYkwlWEySIIx3oFlqVUbiDeDUAT0XhzTggWLMzCXES+ztZfNKtkEE1M+NmtbGxz1mBCY9MM80ZGKTsp8kmqOnh4A0AijXPvAOL9VV/uZkxHGwgYuISbviSou9jfKklSN+gAktW0HEYNsPvOc2ITyZpwrVbI9uPz2jcaGuS3VaNWEhJC0QDyeB952FRPpA2PH9ucnL4xP6iPQdp1VzoUDgVyTz8TDkTs6+FxqzVh5Mgahub39ptTGCqNA55qtq5nKzeeJFIW44AvpL8Fy2Jive4Xg36dBU55ReOUjpUknUTpDMlhYPWt+s6WUwLFkV83LwvClRgT770ZvLaf0qTt2nNOaekdEYv5DqVFW/aSZUWfAVWNCwlSuZoCqV43nvJHiykZgsYqwlWN8v39DLohyKbCAGxuAFjaJ5MMoKrrAjIQFhBIaiHqjE5MTUgEMiSoBZaiMDRYEICBLGcwWEK4BMCUTTLsSgDKKwKLJlKd5DDCbQDoAmSXpkqAFAQwJQEdhp3gS2Py2Ep5nTTSmGbE565jSKCgevMS2KzHckzOUW2XGaitbZofNUKA77+8zuhHPXpN2X8MdiCduNus342SU7nau8lzinSKXDOatnGTAvpDwQ1jqB0m0kcKI3L5UiiBv26/6g562OPDtUaMrkhqJJKmgSP1H5+0pcg2JiHiu5EmNguPqvcbGzOhlFLgKulTwTZF9vec8pNbs7Yxi/a1+zRkMqyfRq1N2objpR5nVyeUxhd/RZ9P4l5JPJAFA77tsTZ/ibsVmY7Ee93XxOGc22dsIpIZpoWTZHzcHGz4UdB79Jnwy4vVRO8S2BdsUHydvtM1FfJpb+AD4uve/YmSTYcKo+0k0qPgi35PkC4d7CpGwiDvCX0Mfg4ZbtPbPDcmgdAB4hrhGhZ2nQwtSLbccaTRuZE0h9xtEnZm2xv/AA6rsTYIsEdPiZnwuvTvHqwL3vXpuajsXLOxOhSy88b/AGhddkq29HO0SFZoYkbG+1Hp6SkwzyP8fmUOxFS6hESERhYFSVCIkqA7Iqx+HgX8QENRr45MTIbZRcAUB89YqoQjUy5IuHQGdVja+ZrGXUADqRvfEW+BXqBzFkmDTMrJfEYmBNC4G1gj5jnyzINQN3v8ROSGlJr6HMK1GYZHWU25kAlCseuDq43v8e86Ph2RKvbgenWX4LhrRYiz+07eGB0nNy8jVo7ODhTSkw8VwF2Fn8fMxrgFj9R5m5U3rmKfGCt3I/ec6ddHY15FplVU8QmYDcbdJhx/EDZoARSYj9r67y8JPbMvUitRG42+13fzOjlsNQmzAN8EX/y/Mw5fKsWprXfe9vidc+GOFFDbbrx7SJyS1Zpxpu3Q18q719djkj095pwEZV0qCo9SJpy+XTD5YE+tS8V0J3F/tOVyb18HWopbCwcAKD9Z39qhNutWSfeLw2UClAPWu0x4+cZT+nb0kqLbKySRWNmXDEUPsZJkfGYm/q+0uaYmeR4PMZVFP0tfO1cQMDC3u66iUHJYna5NU9dJ0eA27NeI7Mm+kV067zLhoDya+Lmzw/ywT5gJ226ge4lLlWZjoQkWaoEjmJNK0PbVrYeGMNGUqwY7BgRtOs+eRCWUKTsCFPT2PvOVg5YtiLrXSpNE1Q/E1+I+HLhFWU6txY/aZyUW0mzWDmk2l+hGaybOysoGrEN6OSN+TfSdBcqyYbLiAKdyNgU9ya2M0PnQwAW0deunUB3G37zZ4dj+dhkuRfBH8+xmUpySVrSN4Qg20nt/g8gcuzAkVsdwJnK1zO/kcsis9nayKJFEb1vObn0TX9H2u50wnbo5JwxVnPqSo2pVTUzyKRd5brUMQTEK9hZNQXF8dZ0izXpSgLq5zk2PEdrYN6/3tIkrZUZ0dQZEkhmIv22mPOqqsRf1de024GA7LZdh8cRWKgvSq2RyW5v09ZjF72zpnFOOlV+TNlf+47dJoLF2rhe8zHKP/wBP+4ZLoN6F3wOvvLaTejKMpRVSToTncFVoAH1J69qmSo1ySeSfeHl0BNGaLS2ZSeT0a8gK/T1r++072HiHih7zg4GAQwKE112nodNAbGcvNVnofxrxrwU+MOLs+n93iMfDsHkEw0Qg6iPjbaDjuxFUQO8ySp6Ohu1s5zYFmh0nSy+WJ6cRGEADU6a41LQrftKnJ/BHHCPY3KYYDBjZNfE6L4wIonaYsshI32rpNS4U5JU3s7I6WiFFP6VuNwsC+dvTpGItDaCzVM238F0A+BXBr8TG9r0LGaMbEoXyZgx8+6joB+TLimyZSSFHNnsZJoQ2AbUfeSXa8EU/J89TLuRYVj60ZL9J6EM6CwQa6EXc52ezRexoVd9zQ1bes9KM3J9aPFnFRW3sdlM7hKuyU1cnqe20bkfGmQaaBXp3HpOSBOhkcizNuDW3Tv7xShFJuQocnI2lE9BlsTDxDbKA2+xI+4qZs7gq5C4bVXSxt7XxNTeFYZUa9QbpR49oCeG4JNWde29kb9JyZRTtNnoOM5Kml+aCwfCUCjUCWA53v8S8LLrh/oFdz/m5vwicM7uDfC1x7Gc/xDMNZoButDtJjKUnV6NHGMY3WzLh26MSoNM1cbKf4nHw8sHP0rVfq7X6GdvIZN2OovpXelqgfe43FyyJ9Kr6EAzdTUW0jmlxOaTl1/Z5Z8CmoivyKgNh1uOPWejxdkLAKOQL57TjaLFgA1yLqu9d50R5Mjj5eLF0mKy2EGajDOCq/qv2HMYjBW+kbGvX/wCTRi5bXueewjct/QIxuOttHMxiCbUUI/JYBZgSDXettu5mxvBzo1KbPNQUyjcOx09gT+0TnFrTBcU1K2jptiiqBF/iIZPq3II9OJlGVUWQTxYHt69J0Mll9t7qhMGlFWjsi5SdNF4aXxxRM4uYGI9swNXx29hPXYeWFUKkGUVR0s/MzjzKL6NeT+O5qro8UMsxv6TtztN/hmAaO3NdL+J6F8MBdh34E4iBkO1jfaxNlyuaaOb/AB1xSTuzs5bLAVt8TTjaQPqYD4mfA10NRhYuEH/5vzvOR97Z6EdR0hLY6Dj6vUQsPcEi6qz/AEx+XyqKKG9xuIgXjYQcl0gUX2zlnAZzdbdLnQyvh9Ud7hphlqobTUmIRsN/XpFKbqkVGCTtj0wtv3htQ5MzjDYnmPTAqYP7myIz7bTFj5hjwvE2vg9eYpj7RxoHZhOIwXtc4+ZdtR+07GLijsDMb4RY6tNX/eJtB1sxmr0jBrfuZJ1hhjsPtJKzXgnB+Thtm8PEAQmtx+JvXJK6jfb0qz7zj4mEnl6gK9fXtc7vgboU0gVVbdprye2Nxs4+F5yqVbQeB4Ol3XPv+Y58uUsjf7TccD12lYiqN2PpObNt7dnauOMVpUcbGd22ICncA3tXf0jMLKaf1MG4o9f6J18LAQC6FV1mXGXD1Vxv0/zKXJekiXx1tsQ+Tq2D79Loj7TnPmiGplBN7kTs5hQGB4A9Zmx8oj/UpAPcGXCS+SJxf/Jmxc6wT6Vb3qc05p2fYgGva67zfj4VcP8ABqYxgXe4Hp3m8MUujm5c20rMr4ravrAYH8dDUNsHC0bEg/vI6SKgHvNfsc1O3e/uacl4ehUMSdXoaNftAxMUo1VfYkjj1id7uQKfeTi7tuzXJJJRVHWVyALFE9NoL4d7kbTJhYu+82k6qMxcaZ0xkpIU+GDtVd9p1MBRpAAroJzg6g1V/wAxr44PO3b0kyTei4NJtnVTKEb6t/tIEYHgH12mbL4hfYEgDqdrm3SAKsTndp7OiNNaActWw+04+Zw31XXrO6iMID4iL+qOM8XpWKcMlt0cXDxnbYgAdTNKaBxz3hZrQR9KmLyybzV01fRmrTrsfg5ZmPND8wsbIBRd3NakDpJovk/Eyydm2KoDKjbYV/E1YeXlYaD4jgPiZSZpGJFWuBCgrh1yYFg7LJKAx8UCc7Mu5O1/E6yZcdpZwhcqMlEmUWzlZPKHkjeazl+L6TXsBM+LiV3g5OTBRUUDoHpJM+o9jJHiFnz4Ezu5LxFE3C++1GcRRNOCk9ecYyWz5rh5ZRl7T0q+OL0UwPP1tbOB108/mcpEjkScz4oro9GPPOX+x6NRqHIG3eZlyA1XZPpc5qMR1MeMd+8ywa6Zv6ql2h2c22Cn5P7znsnxNb4rHmLK3LjpGc2m7RmKQSk1eXBOHNMiMRCoOu8FkHSaNMnlx5CxMuiWEmjRL8uGQYmfRCCmP8uWMOLIaiLSMABO8LRLCSWy0ma8s3absIDkkzlJtHK5J5mE42bwlR1GBI/xOcyKCbF/59ZtQkiv5i8ZQAe5kRdaNZbRlwhZ7V0mgADp9oGHXJPxHFi3SNiQtx1hIpbrQkKk8iPy6SW6RSVsdhJUepMNBGLhzCUjZIzsveNw1FbRhTvLC0KElyKoWVgkRhWURCwFFYt0NbATSRBZI7Cjn+S3f8S5q0iSVkTij5rhYdzdhYcmFhzUiT1pSPn+LiopEjkSWiRyJMnI6oxBVIYSMVIYSQ5GqiLCS9EcEl6ZNlYmfTK8uatEmiFhRl8uV5c1aZNMeQYmXy5Yw5p0y9EMgwMww5eiadMgSKx4mcJC8uaPLk0RZDxM2mMQUbjfLlhInIaiRcWukrFfVC0yBItFbAGFXMdhEw1O2+8JPtJbLSGoL5qPRQOIvDQd49UHMxkzWKCw16zREC47DFDeZSNETy7MvTIXviRbk7HovRKOELuHqgl4bHoFlESyxhbeUYxC9MkOSFio8IiTQiRgwj1EcmHPTczyVxgIkaqRqIOojBhjpM3I2URarGBIaJH4GX1HtJcki1BszhJYSdH/AIEdGlNlBvvM/VRp6TMGiXomhsOpNMrIWBn0SaJo0ywkMgwM2iXpmjy5NEMgoz6Zflx+iTRDIeInRJ5cfol6IshUZ9EvTH6JNMMh0I0yBI/RL0wyChOmGm0PTLCRNlJDkrvGi5mCw1JmTRaZoWWWgK0LVJZaYxYRMTqlEmTQ7DZ4ssZUrVHQWGBIWgF4DYkVBYy5Jm1mXHQWc1UuF5S9orDxZoTEm9tGFJgjBHeWEj1YRgqLJhijOi1NCOJCssJE5WUo10aEeM5mVdo8PM2i0FoF31kxRYqpQf0jFYRWOjOMIy9E0BR3gMseQsaFeV6yhgiN8uVojsWP0BOGJXlCMlwthSElBIMOPCyyDDIMRDYUryzNAb0l6oZMeKM2iVomomCYZBiZ9MvTGkSqjsWIK12jKHaDUu5LZSL0CWIBMrVEMaTIWidUovFQWMLwCYsvALR0FhkRbNUFni2eVQrD1S4jzJI6Czj4TGaUeSSbM5kPR49HkkkMtDFxIxHkkkstB2IatJJEUgxCEkkkYQMvVJJAC9UotJJEMu5NUkkBEuVckkBl6pWqSSAiwZckkBoGUZJIAXqgEy5IACTBuSSMCiYBMkkABLQGaSSUhCmaLZpJIITF6pJJIyD/2Q==")
}

[data-testid="stVerticalBlock"] {
    margin: auto;
    width: 750px;
    padding: 20px;
    background-color: rgba(78, 212, 245,0.5)
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