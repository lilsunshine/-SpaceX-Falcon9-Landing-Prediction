# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    # dcc.Dropdown(id='site-dropdown',...)
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True,
        style={'width': '80%', 'padding': '2px', 'fontsize': '22px'}
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    # Pie chart will be displayed here
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    # dcc.RangeSlider(id='payload-slider',...)
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=500, value=[min_payload, max_payload],
        marks={0: {'label': '0 kg'},
               2500: {'label': '2500 kg'},
               5000: {'label': '5000 kg'},
               7500: {'label': '7500 kg'},
               10000: {'label': '10000 kg'}}
    ),
    html.Br(),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    # Scatter plot will be displayed here
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback function for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def site_chart(selected_site):
    if selected_site == 'ALL':
        selection_df = spacex_df
        title = 'Total Successful Launches from All Sites'
        fig = px.pie(selection_df, names='Launch Site', values='class', title=title)
    else:
        selection_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Success vs. Failure at {selected_site}'
        success_counts = selection_df['class'].value_counts().reindex([0, 1], fill_value=0)
        fig = px.pie(
            values=success_counts.values, names=['Failure', 'Success'],
            title=title, color=success_counts.index, color_discrete_map={0: 'red', 1: 'green'}
        )
    return fig

# TASK 4: Callback function for scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        size='Payload Mass (kg)', title='Payload vs. Success',
        labels={'class': 'Success (1=Yes, 0=No)'}
    )
    return fig
# Run the app
if __name__ == '__main__':
    app.run()
