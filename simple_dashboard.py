import requests
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

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

    # Create a stacked bar chart
    def create_stacked_bar_chart():
        x = range(len(quantities))
        plt.figure(figsize=(8, 6))
        plt.bar(x, df['Buying Price'], label='Buying Price', color='b')
        plt.bar(x, df['Selling Price'], label='Selling Price', color='g', bottom=df['Buying Price'])
        plt.xlabel('Quantities')
        plt.ylabel('Prices')
        plt.title('Stacked Bar Chart')
        plt.xticks(x, quantities)
        plt.legend()
        plt.tight_layout()

    # Create a line chart
    def create_line_chart():
        plt.figure(figsize=(8, 6))
        plt.plot(quantities, df['Buying Price'], marker='o', color='b', label='Buying Price')
        plt.plot(quantities, df['Selling Price'], marker='o', color='g', label='Selling Price')
        plt.xlabel('Quantities')
        plt.ylabel('Prices')
        plt.title('Line Chart')
        plt.legend()
        plt.tight_layout()

    # Create a pie chart
    def create_pie_chart():
        plt.figure(figsize=(8, 6))
        plt.pie(df['Buying Price'], labels=quantities, autopct='%1.1f%%', startangle=140)
        plt.title('Pie Chart')

    # Initialize the Dash app
    app = dash.Dash(__name__)

    # Define the layout of the Dash app
    app.layout = html.Div([
        html.H1("Gold Prices Visualization"),
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Stacked Bar Chart', 'value': 'bar'},
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Pie Chart', 'value': 'pie'}
            ],
            value='bar',
            clearable=False
        ),
        html.Div(id='chart-container')
    ])

    # Define callback to update chart based on dropdown selection
    @app.callback(
        Output('chart-container', 'children'),
        [Input('chart-type', 'value')]
    )
    def update_chart(selected_chart):
        if selected_chart == 'bar':
            create_stacked_bar_chart()
        elif selected_chart == 'line':
            create_line_chart()
        else:
            create_pie_chart()

        # Save the Matplotlib plot to a BytesIO object and encode it to base64
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()

        # Return the chart as an image
        return html.Img(src='data:image/png;base64,{}'.format(image_base64), style={'width': '80%', 'height': '80%'})

    if __name__ == '__main__':
        app.run_server(debug=True)

else:
    print("Failed to retrieve data from the API.")
