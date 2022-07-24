# Standard Imports
from turtle import width
import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objects as go
import geopandas
import plotly.express as px


#KPIs: world = pd.read_csv('data/worldometer_data.csv')
#Graph 1: df = pd.read_csv('data/worldometer_data.csv')
#Graph 2: df = pd.read_csv('data/worldometer_data.csv')
#Graph 3: pd.read_csv('data/usa_county_wise.csv')
#Map_usa: df_usa = pd.read_csv('data/usa_county_wise.csv')

df_worldmeter = pd.read_csv('data/worldometer_data.csv')
df_usa_county = pd.read_csv('data/usa_county_wise.csv')
df_shape = geopandas.read_file('data/s_22mr22/s_22mr22.shp')


df_worldmeter_total_cases_agg = df_worldmeter.groupby(['Continent'])['TotalCases'].agg(['sum']).reset_index()
df_worldmeter_total_deaths_agg = df_worldmeter.groupby(['Continent'])['TotalDeaths'].agg(['sum']).reset_index()

df_usa_county['new_date'] = pd.to_datetime(df_usa_county['Date'], format='%m/%d/%y')
df_usa_county = df_usa_county[df_usa_county.new_date > df_usa_county['new_date'].max() - pd.to_timedelta("30day")]

df_usa_county_date_deaths_agg = df_usa_county.groupby(['Date'])['Deaths'].agg(['sum']).reset_index()

df_usa_county = df_usa_county.rename(columns ={'Province_State':'NAME'})
df_usa_county = df_usa_county.groupby(['NAME', 'Date'])['Confirmed', 'Deaths'].sum().reset_index()
df_usa_county_geo = df_shape.merge(df_usa_county, on='NAME')
df_usa_county_geo_lastday = df_usa_county_geo[df_usa_county_geo['Date'] == '7/27/20']
print(df_usa_county_geo_lastday.shape)

df_worldmeter_total_recovered_agg = df_worldmeter.groupby(['Continent'])['TotalRecovered'].agg(['sum']).reset_index()


# ======================== Setting the margins
layout = go.Layout(
    margin=go.layout.Margin(
        l=40,  # left margin
        r=40,  # right margin
        b=10,  # bottom margin
        t=35  # top margin
    )
)
# ======================== Plotly Graphs
def get_bar_chart_first():
    barChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Bar(x=df_worldmeter_total_recovered_agg['Continent'],
                                                                          y=df_worldmeter_total_recovered_agg['sum'],
                                                                          marker=dict(color='#351e15'))).update_layout(
        title='Users', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return barChart

def get_bar_chart_second():
    barChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Bar(x=df_worldmeter_total_cases_agg['Continent'],
                                                                          y=df_worldmeter_total_cases_agg['sum'],
                                                                          marker=dict(color='#351e15'))).update_layout(
        title='Users', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return barChart
    
def get_line_bar_chart():
    lineChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Bar(x=df_usa_county_date_deaths_agg['Date'],
                                                                               y=df_usa_county_date_deaths_agg['sum'],
                                                                               marker=dict(
                                                                                   color='#351e15'))).add_trace(
                                                                                    go.Scatter(x=df_usa_county_date_deaths_agg['Date'], 
                                                                                   y=df_usa_county_date_deaths_agg['sum'], line=dict(
                                                                                    color='#351e15', width=4))).update_layout(
        title='Page Views', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return lineChart

    
def get_map():
    fig = px.choropleth(df_usa_county_geo_lastday, geojson=df_usa_county_geo_lastday.geometry, locations=df_usa_county_geo_lastday.index, color="Confirmed")
    fig.update_geos(fitbounds="locations", visible=False)
    scatterPlot = dcc.Graph(figure=fig)


    return scatterPlot
def get_pie_chart():
    pieChart = dcc.Graph(
        figure=go.Figure(layout=layout).add_trace(go.Pie(
            labels=df_worldmeter_total_deaths_agg['Continent'],
            values=df_worldmeter_total_deaths_agg['sum'],
            marker=dict(colors=['#120303', '#300f0f', '#381b1b', '#4f2f2f', '#573f3f', '#695a5a', '#8a7d7d'],
                        line=dict(color='#ffffff', width=2)))).update_layout(title='Bounce Rate',
                                                                             plot_bgcolor='rgba(0,0,0,0)',
                                                                             showlegend=False),
        style={'width': '50%', 'height': '40vh', 'display': 'inline-block'})
    return pieChart

# ======================== Dash App
app = dash.Dash(__name__)
# ======================== App Layout
app.layout = html.Div([
    html.H1('Data Analytics Dashboard', style={'text-align': 'center', 'background-color': '#ede9e8'}),
    get_bar_chart_first(),
    get_bar_chart_second(),
    get_line_bar_chart(),
    get_pie_chart(),
    get_map()
])
if __name__ == '__main__':
    app.run_server(port=8051)