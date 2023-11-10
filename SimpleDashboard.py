import requests
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Define the header parameters
headers = {
    "Accept": "application/vnd.BNM.API.v1+json"
}

api_url = "https://api.bnm.gov.my/public/kijang-emas"
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()["data"]

    # Extracting data for DataFrame
    quantities = ['One Ounce', 'Half Ounce', 'Quarter Ounce']
    buying_prices = [data["one_oz"]["buying"], data["half_oz"]["buying"], data["quarter_oz"]["buying"]]
    selling_prices = [data["one_oz"]["selling"], data["half_oz"]["selling"], data["quarter_oz"]["selling"]]

    # Creating DataFrame
    df = pd.DataFrame({
        'Quantities': quantities,
        'Buying Price': buying_prices,
        'Selling Price': selling_prices
    })

    # Initialize the Dash app
    app = dash.Dash(__name__)

    # Define the layout of the Dash app
    app.layout = html.Div([
        html.H1("Gold Prices Visualization"),
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Stacked Bar Chart', 'value': 'bar'},
                {'label': 'Pie Chart', 'value': 'pie'}
            ],
            value='bar',
            clearable=False
        ),
        dcc.Graph(id='chart-container')  # Use dcc.Graph for plotting
    ])

    # Define callback to update chart based on dropdown selection
    @app.callback(
        Output('chart-container', 'figure'),  # Output should be 'figure'
        [Input('chart-type', 'value')]
    )
    def update_chart(selected_chart):
        if selected_chart == 'bar':
            # Create a stacked bar chart using plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(x=quantities, y=df['Buying Price'], name='Buying Price'))
            fig.add_trace(go.Bar(x=quantities, y=df['Selling Price'], name='Selling Price', 
                                 marker_color='lightgreen'))

            fig.update_layout(barmode='stack', title='Gold Prices for Different Quantities')
        else:
            # Create a pie chart using plotly
            fig = go.Figure(data=[go.Pie(labels=quantities, values=df['Buying Price'],
                                         textinfo='label+percent', marker_colors=['gold', 'silver', 'darkgoldenrod'])])
            fig.update_layout(title='Percentage of Buying Price for Each Quantity')

        return fig

    if __name__ == '__main__':
        app.run_server(debug=True)

else:
    print("Failed to retrieve data from the API.")
