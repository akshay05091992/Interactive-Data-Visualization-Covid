import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


death_rawdata = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_rawdata = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_rawdata = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_rawdata = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')


country_rawdata.rename(columns={'Country_Region': 'Country', 'Long_': 'Long'}, inplace=True)
confirmed_rawdata.rename(columns={'Country/Region': 'Country'}, inplace=True)
death_rawdata.rename(columns={'Country/Region': 'Country'}, inplace=True)
recovered_rawdata.rename(columns={'Country/Region': 'Country'}, inplace=True)


country_rawdata.drop(['People_Tested', 'People_Hospitalized'], axis=1, inplace=True)
confirmed_rawdata.drop('Province/State', axis=1, inplace=True)
death_rawdata.drop('Province/State', axis=1, inplace=True)
recovered_rawdata.drop('Province/State', axis=1, inplace=True)


app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])

main_heading = dbc.Container([html.H1(["Coronavirus Pandemic Data Visualization"], className="my-3 text-center")])


navigationbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.A("Confirmed/Recovered/Deaths", href='#confirmed', style={'color': 'white'}), className="mr-5"),
        dbc.NavItem(html.A("World Map", href="#worldmap", style={'color': 'white'}), className="mr-5"),
        dbc.NavItem(html.A("Mortality & Recovery Rate", href="#mortality", style={'color': 'white'}), className="mr-5")
    ], brand="Covid-19 Data Visualízation", color='dark', dark=True, className='fixed-top p-4')

#####################################################################################################
Total_Cases = dbc.Container(
    dbc.Row(
        [
            dbc.Col(children=[html.H4('Total Confirmed'),
                              html.Div(country_rawdata['Confirmed'].sum(),
                                       style={'font-size': '24px', 'color': 'brown'})],
                    className='text-center border-right p-2',
                    ),
            dbc.Col(children=[html.H4('Total Recovered', style={'padding-top': '0px'}),
                              html.Div(country_rawdata['Recovered'].sum(),
                                       style={'font-size': '24px', 'color': 'green'})],
                    className='text-center border-right p-2'),
            dbc.Col(children=[html.H4('Total Deaths', style={'padding-top': '0px'}),
                              html.Div(country_rawdata['Deaths'].sum(),
                                       style={'font-size': '24px', 'color': 'red'})],
                    className='text-center border-right p-2'),
            dbc.Col(children=[html.H4('Total Active'),
                              html.Div(country_rawdata['Active'].sum(),
                                       style={'font-size': '24px', 'color': 'purple'})],
                    className='text-center  p-2',
                    ),
        ]
        , className='shadow my-5'))
###############################################################################################
total_confirmed = confirmed_rawdata.groupby('Country').sum().reset_index()
World_Map = html.H1(id='worldmap', children='COVID-19 Confirmed Cases', className='mt-2 py-4 pb-3 text-center')
total_confirmed.loc[:, ['Lat', 'Long']] = confirmed_rawdata.groupby('Country').mean().reset_index().loc[:, ['Lat', 'Long']]

CASE = 1000
total_confirmed = total_confirmed[total_confirmed.iloc[:, 3:].max(axis=1) > CASE]
total_confirmed = pd.melt(total_confirmed,
                                   id_vars=total_confirmed.iloc[:, :3],
                                    value_vars=total_confirmed.iloc[:, 3:],
                                   var_name='date',
                                   value_name='confirmed')
# Plotly for visualization.
fig9 = px.scatter_geo(total_confirmed,
                      lat="Lat", lon="Long", color="Country",
                      hover_name="Country", hover_data=['confirmed'], size="confirmed",
                      size_max=50, animation_frame="date",
                      projection="natural earth",
                       height=500)


######################################################################################

crd_heading = html.H1(id='confirmed', children='Confirmed, Recovered & Death cases of Top 10 Countries', className='text-center')
country_rawdata.sort_values('Confirmed', ascending=False, inplace=True)
country_name = country_rawdata.head(10)
crd = go.Figure(data=[
    go.Bar(name='Confirmed', x=list(country_name['Country'].values), y=list(country_name['Confirmed']), marker_color='blue'),
    go.Bar(name='Recovered',  x=list(country_name['Country'].values), y=list(country_name['Recovered']),marker_color='green'),
    go.Bar(name='Deaths',  x=list(country_name['Country'].values), y=list(country_name['Deaths']),marker_color='red',),
])
crd.update_layout(barmode='group')

###################################################################################
graph_heading = html.H1(children='COVID-19 cases for each country', className='mt-5 pb-3 text-center')
daily_aggregate_list=[]
daily_category_list=[]
daily_aggregate = confirmed_rawdata['Country'].unique().tolist()
daily_category = ['Confirmed cases', 'Death rate', 'Recovered cases']

for x in daily_category:
    daily_category_list.append({'label': x,'value': x})

for x in daily_aggregate:
    daily_aggregate_list.append({'label': x,'value': x})


dropdown = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children=[html.Label('Select case type'),
                                  html.Div(
                                      dcc.Dropdown(id='select-category', options=daily_category_list,
                                                   value='Confirmed cases'))],
                        className='mr-5 p-2 ', width=3),
                dbc.Col(children=[html.Label('Select Country'),
                                  html.Div(
                                      dcc.Dropdown(id='select-country', options=daily_aggregate_list, value='Germany'))],
                        className='mr-5 p-2 ', width=3),


                          ], className='my-4 justify-content-center')
    ])
#########################################################################################
def graph(graph_data):
    data = [go.Scatter(
        x=graph_data['Date'], y=graph_data['Cases'], line=dict(color='black'), mode='lines+markers',
        name='lines+markers', fill='toself', fillcolor = 'violet',)]
    layout = {'xaxis': dict(title='Dates'),
        'yaxis': dict(title='Cases'),
    }
    graph = [{'data': data,'layout': layout}]
    return graph

##########################################################################################
confirmed_world = confirmed_rawdata.iloc[:, 4:].sum(axis=0)
death_world = death_rawdata.iloc[:, 4:].sum(axis=0)
recovered_world = recovered_rawdata.iloc[:, 4:].sum(axis=0)
active_world = confirmed_world - death_world - recovered_world
mortality_graph_heading = html.H1(id='mortality',
                              children='Recovery and Mortality Rate', className='mt-5 pb-3 text-center')
total_rate = pd.DataFrame({'confirmed': confirmed_world,'deaths': death_world,'recovered': recovered_world,'active': active_world}, index=confirmed_world.index)

total_rate['Recovery'] = total_rate['recovered'] / total_rate['confirmed'] * 100
total_rate['Mortality'] = total_rate['deaths'] / total_rate['confirmed'] * 100
total_rate['date'] = total_rate.index
unpivotdata = total_rate.melt(id_vars="date",value_vars=['Recovery', 'Mortality'],var_name="status",value_name="ratio")
fig1 = px.line(unpivotdata, x="date", y="ratio", color='status',color_discrete_sequence=['green', 'red']
               )
############################################################################################################
app.layout = html.Div(
    [main_heading,navigationbar,
     Total_Cases,
     html.Div(children=[World_Map,
                        dcc.Graph(
                                figure=fig9
                        )
                        ]
              ),

     dbc.Container(children=[crd_heading,
                             dcc.Graph(
                                 figure=crd
                             )
                             ]
                   ),
     dbc.Container([graph_heading,
                    dropdown,
                    html.Div(id='total-data'),
                    dcc.Graph(
                        id='graph'
                    )
                    ]
                   ),
     html.Div(children=[mortality_graph_heading,
                        dcc.Graph(
                            figure=fig1
                        )
                        ]
              ),
     ]
)

server = app.server

@app.callback(
    [Output('total-data', 'children')],
    [Input('select-country', 'value')]
)
def number_of_country(total_nations):
    each_nation = country_rawdata[country_rawdata['Country'] == total_nations].loc[:, ['Confirmed', 'Deaths', 'Recovered', 'Active']]
    total_data = dbc.Container(
        [
            html.H3('Total case in ' + total_nations + ''),
            dbc.Row(
                [
                    dbc.Col(children=[html.H6('Confirmed'),
                                      html.Div(each_nation['Confirmed'].sum(),
                                               style={'font-size': '24px', 'color': 'brown'})],
                            className='text-center border-right p-2',
                            ),
                    dbc.Col(children=[html.H6('Recovered', style={'padding-top': '0px'}),
                                      html.Div(each_nation['Recovered'].sum(),
                                               style={'font-size': '24px', 'color': 'green'})],
                            className='text-center border-right p-2'),
                    dbc.Col(children=[html.H6('Deaths', style={'padding-top': '0px'}),
                                      html.Div(each_nation['Deaths'].sum(),
                                               style={'font-size': '24px', 'color': 'red'})],
                            className='text-center border-right p-2'),
                    dbc.Col(children=[html.H6('Active'),
                                      html.Div(each_nation['Active'].sum(),
                                               style={'font-size': '24px', 'color': 'purple'})],
                            className='text-center  p-2',
                            ),
                ]
                , className='my-4 shadow ')

        ]
    )

    return [total_data]

@app.callback(
    [Output('graph', 'figure')],
    [Input('select-country', 'value'),
     Input('select-category', 'value'),
    ])
def country(name, type):

    if type == 'Confirmed cases':
        type = confirmed_rawdata
    elif type == 'Death rate':
        type = death_rawdata
    else:
        type = recovered_rawdata

    country_group = type.groupby('Country')
    country_group = country_group.get_group(name)
    case = []
    dates = []
    for x, column in enumerate(country_group):
        if x > 3:
            case.append(country_group[column].sum())
            dates.append(column)
            concatnate = zip(dates, case)
            append = pd.DataFrame(data=concatnate, columns=['Date', 'Cases'])
    append['Country'] = country_group['Country'].values[0]
    append_new = append.copy(deep=True)
    for x in range(len(append) - 1):
        append.iloc[x + 1, 1] = append.iloc[1 + x, 1] - append_new.iloc[x, 1]
        if append.iloc[x + 1, 1] < 0:
            append.iloc[x + 1, 1] = 0
    return (graph(append))


app.run_server()
