# Interactive-Data-Visualization-Covid-Data

## About
This is a pre-requiste Mini Project in area of Interactive Data Visualization  of my Masters study , wherein I visualized COVID-19 datasets from John Hopkins University and created a Dashboard using various Visualization Techniques in Python. This project shows the real-time visualizations as the dateset which is used is a time-series live datasets.

## Dataset
We are using the Covid-19 Datasets from the GitHub repository of the 2019 Novel Coronavirus Visual Dashboard operated by the John Hopkins University Center for Systems
Science and Engineering (JHU CSSE). These datasets are time-series data of confirmed, global and recovered cases across the globe which are updated regularly.

URL for raw dataset:-

● https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv

● https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv

● https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv

Additional dataset:

● https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv

The Dataset is divided into columns with titles as Province/State, Country/Region, Lat(Latitude),Long(Longitude) and Dates. As we know these can be divided into three parts as Nominal Data,Ordinal Data & Quantitative Data.

● This Time Series Dataset has Nominal Data for the Columns: Province/State, Country/Region,Lat & Long

● Ordinal Data as Latitude, Longitude ,Dates given in column as they comprise of number of cases we would be playing with as we can Order the countries as well.

● The last would be the number of cases which is Quantitative data which would be used as sum of the confirmed, recovered and death cases.

● For additional dataset Nominal Data is for column Country_Region, Last_Update, Lat, Long_,ISO3 ,for Ordinal data its confirmed and Quantitative data confirmed,death,recovered,active,Incident_rate

# Visualization Technique: 
We would be using below visualization techniques for the given datasets:

● Geospatial Visualization:  Geo Scatter plot on Natural Earth Map Projection

● Time Oriented Visualization : Dynamic representation

● Line Plot used for mortality & recovery rate

● Bar Graph for Top 10 countries

# Note :

If there is any issue with the datasets use kindly visit https://github.com/CSSEGISandData/COVID-19 for more info.
The idea of this project is taken from many sources being a first attempt towards the visualization techniques. I would be updating the code to make the visualization better also deployement of the dashboard will be on webserver directly. Right now it is just a .py file with web server link.
