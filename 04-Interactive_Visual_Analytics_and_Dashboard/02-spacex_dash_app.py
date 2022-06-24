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

# Get launch sites' names 
sites_name = spacex_df.groupby(['Launch Site'], as_index=False).first()
sites_name = sites_name["Launch Site"]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': sites_name[0], 'value': sites_name[0]},
                                                {'label': sites_name[1], 'value': sites_name[1]},
                                                {'label': sites_name[2], 'value': sites_name[2]},
                                                {'label': sites_name[3], 'value': sites_name[3]},
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500 : '7500', 10000 : '10000'},
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # pie chart of total success launches  (the total count of class column)
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')

        return fig
    else:
        # return the outcomes piechart for a selected site

        # filter data for selected launch site
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        
        # compute success and failed count for the selected site
        filtered_df= filtered_df.groupby(["Launch Site", "class"], as_index=False).size()
        filtered_df.rename(columns = {'size':'class count'}, inplace = True)
        
        # pie chart of success (class=1) count and failed (class=0) count for the selected site.
        fig = px.pie(filtered_df, values='class count', names='class',  title='Total Success Launches for site ' + str(entered_site))
        
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload):
    # filter dataframe with only relevant columns for chart
    filtered_df = spacex_df[['Launch Site','Payload Mass (kg)', 'class', 'Booster Version Category']]
    # filter dataframe for selected payload range 
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'].between(payload[0],payload[1])]

    if entered_site == 'ALL':
        
        # scatter chart of Correlation between Payload and Success for all Sites
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for all Sites")
        return fig

    else:
        # filter data for selected launch site
        filtered_df = filtered_df[filtered_df["Launch Site"]==entered_site]
        
         # scatter chart of Correlation between Payload and Success for selected site
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",title="Correlation between Payload and Success for site " + str(entered_site))
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
