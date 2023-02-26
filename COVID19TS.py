import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

covid_df = pd.read_csv('/Users/macbookpro/Desktop/LinkedIn Work/LinkedIn Posts/COVID 19/time_series_covid19_confirmed_global.csv')
covid_df = covid_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
covid_df['Date'] = pd.to_datetime(covid_df['Date'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("COVID-19 Dashboard", style={'text-align': 'center'}),
    
    html.Div([
        html.Div([
            html.H2("Time-Series Line Chart"),
            dcc.Dropdown(id='country-dropdown', options=[{'label': country, 'value': country} for country in covid_df['Country/Region'].unique()], value='Algeria', multi=True),
            dcc.Graph(id='covid-graph') 
        ], className='six columns'),
        
        html.Div([
            html.H2("Bubble Chart of Total Cases"),
            dcc.Graph(id='covid-bubble') 
        ], className='six columns')
    ], className='row')
])

@app.callback(
    Output(component_id='covid-graph', component_property='figure'),
    Input(component_id='country-dropdown', component_property='value')
)
def update_graph(countries):
    if isinstance(countries, str):
        countries = [countries]
    filtered_df = covid_df[covid_df['Country/Region'].isin(countries)]
    traces = []
    for country in filtered_df['Country/Region'].unique():
        temp_df = filtered_df[filtered_df['Country/Region'] == country]
        trace = go.Scatter(x=temp_df['Date'], y=temp_df['Confirmed'], mode='lines', name=f'{country} - Confirmed')
        traces.append(trace)
    layout = go.Layout(title='COVID-19 Time Series', xaxis={'title': 'Date'}, yaxis={'title': 'Count'}, template="plotly_dark")
    return {'data': traces, 'layout': layout}

@app.callback(
    Output(component_id='covid-bubble', component_property='figure'),
    Input(component_id='country-dropdown', component_property='value')
)
def update_bubble_chart(countries):
    if isinstance(countries, str):
        countries = [countries]
    filtered_df = covid_df[covid_df['Country/Region'].isin(countries)]
    total_confirmed = filtered_df.groupby('Country/Region')['Confirmed'].max().reset_index()
    fig = px.scatter(total_confirmed, x='Country/Region', y='Confirmed', size='Confirmed', color='Country/Region', hover_name='Country/Region')
    fig.update_layout(title='Bubble Chart of Total COVID-19 Cases', template="plotly_dark")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
