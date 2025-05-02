# Import required libraries
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Read the SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min and max payload
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create a list of dropdown options
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
    [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create a Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=site_options,
                 value='ALL',
                 placeholder='Select a Launch Site',
                 searchable=True),
    
    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # Payload slider
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload, max=max_payload, step=1000,
                    marks={int(min_payload): str(int(min_payload)),
                           int(max_payload): str(int(max_payload))},
                    value=[min_payload, max_payload]),

    # Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter'))
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Success vs Failure for site {selected_site}')
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site == 'ALL':
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
