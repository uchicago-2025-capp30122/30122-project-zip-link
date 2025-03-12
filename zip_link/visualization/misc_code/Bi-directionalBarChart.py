import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go

# Load the preprocessed data
data_path = "../data/preprocessed/zipatlas_bulk_merge.csv"
df = pd.read_csv(data_path)

# Debugging: Print column names to check for mismatches
print("Column Names in CSV:", df.columns.tolist())

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Chicago ZIP Code Comparison"),

    # Dropdowns to select ZIP codes
    html.Label("Select First ZIP Code:"),
    dcc.Dropdown(
        id='zip1-selector',
        options=[{'label': str(zip_code), 'value': zip_code} for zip_code in df["Zip Code"].unique()],
        value=df["Zip Code"].unique()[0],
        clearable=False
    ),

    html.Label("Select Second ZIP Code:"),
    dcc.Dropdown(
        id='zip2-selector',
        options=[{'label': str(zip_code), 'value': zip_code} for zip_code in df["Zip Code"].unique()],
        value=df["Zip Code"].unique()[1],
        clearable=False
    ),

    # Three separate graphs
    dcc.Graph(id='price-chart'),
    dcc.Graph(id='housing-cost-chart'),
    dcc.Graph(id='economic-indicators-chart')
])

# Callback to update the charts based on selected ZIP codes
@app.callback(
    [
        dash.dependencies.Output('price-chart', 'figure'),
        dash.dependencies.Output('housing-cost-chart', 'figure'),
        dash.dependencies.Output('economic-indicators-chart', 'figure')
    ],
    [
        dash.dependencies.Input('zip1-selector', 'value'),
        dash.dependencies.Input('zip2-selector', 'value')
    ]
)
def update_charts(zip1, zip2):
    df_selected = df[df["Zip Code"].isin([zip1, zip2])]
    
    # Define metric groups
    price_metrics = ["median_property_prices"]
    housing_cost_metrics = ["median_housing_costs", "owner_median_housing_costs", "renter_median_housing_costs"]
    economic_metrics = ["housing_cost_perc_income", "poverty_levels", "unemployment_rates"]
    
    # Define color shades
    colors = ["#1f77b4", "#85C1E9"]  # Lighter blue for ZIP 1, Darker blue for ZIP 2
    
    # Function to create a bar chart with custom colors
    def create_bar_chart(metrics, title):
        fig = go.Figure()
        for i, zip_code in enumerate([zip1, zip2]):
            values = df_selected[df_selected["Zip Code"] == zip_code][metrics].values[0]
            fig.add_trace(go.Bar(
                y=metrics, 
                x=values, 
                name=f'ZIP {zip_code}', 
                orientation='h',
                marker=dict(color=colors[i])  # Assign color shade
            ))
        fig.update_layout(
            title=title,
            xaxis_title='Value',
            yaxis_title='Metric',
            barmode='group',  # Group bars together
            template='plotly_white'
        )
        return fig
    
    # Generate three separate charts
    fig1 = create_bar_chart(price_metrics, f'Comparison of Median Property Prices for ZIP {zip1} vs ZIP {zip2}')
    fig2 = create_bar_chart(housing_cost_metrics, f'Comparison of Housing Costs for ZIP {zip1} vs ZIP {zip2}')
    fig3 = create_bar_chart(economic_metrics, f'Comparison of Economic Indicators for ZIP {zip1} vs ZIP {zip2}')
    
    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
