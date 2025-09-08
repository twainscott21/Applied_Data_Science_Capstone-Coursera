# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()
print(launch_sites[0])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[
                                            {'label': 'All Sites', 'value': 'All Sites'},
                                            {'label': launch_sites[0], 'value': launch_sites[0]},
                                            {'label': launch_sites[1], 'value': launch_sites[1]},
                                            {'label': launch_sites[2], 'value': launch_sites[2]},
                                            {'label': launch_sites[3], 'value': launch_sites[3]}
                                            ],
                                            value ='All Sites',
                                            placeholder='Select a launch site',
                                            searchable=True),  
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value')
              )

def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        successes = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='count')
        fig = px.pie(successes, values='count', names='Launch Site',
                     title='Total Successful Launches by Site')

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        class_counts = filtered_df['class'].value_counts().reset_index()
        class_counts.columns = ['class', 'count']

        fig = px.pie(class_counts, values='count', names='class',
                     title=f'Total Successful Launches for Site {entered_site}')
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
              [Input(component_id = 'site-dropdown', component_property = 'value'), 
               Input(component_id = 'payload-slider', component_property = 'value')])

def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'All Sites':
        filtered_df = spacex_df
        title = "Successful Launches vs Payload Mass for All Sites"

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        title = f"Successful Launches vs Payload Mass for site {entered_site}"

    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    fig = px.scatter(filtered_df, 
                     x = 'Payload Mass (kg)',
                     y = 'class', 
                     color = 'Booster Version Category',
                     title = title)

    return fig

# Run the app
if __name__ == '__main__':
    app.run()
