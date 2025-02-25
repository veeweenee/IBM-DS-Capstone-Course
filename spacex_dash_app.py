# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})

for i in spacex_df["Launch Site"].value_counts().index:
        launch_sites.append({'label': 'item', 'value': 'item'})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown',options= launch_sites, value= 'All Sites', placeholder ='Select a launch site here', searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload], marks = {
                                    2500: '2500 kg',
                                    5000: '5000 kg',
                                    7500: '7500 kg',
                                }),
                                

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)

def update_chart(userinput):
    if(userinput == 'All Sites'):
        new_df = spacex_df[spacex_df['class']==1]
        fig = px.pie(new_df, names = 'Launch Site', title='Total Success Launches by Site')
    else:
        new_df = spacex_df.loc[spacex_df['Launch Site'] == userinput]
        fig = px.pie(new_df, names = 'class', title='Total Success Launches for site '+ userinput)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload_slider', component_property='value')]
)

def update_scat_graph(userinput, slider):
    if userinput == 'All Sites':
        low, high = slider
        new_df = spacex_df
        cond = (new_df['Payload Mass (kg)'] < high) & (new_df['Payload Mass (kg)'] > low) 
        fig = px.scatter(new_df[cond], x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        
        low, high = slider
        new_df = spacex_df.loc[spacex_df['Launch Site'] == userinput]
        cond = (new_df['Payload Mass (kg)'] < high) & (new_df['Payload Mass (kg)'] > low) 
        fig = px.scatter(new_df[cond], x='Payload Mass (kg)', y='class', color='Booster Version Category')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
