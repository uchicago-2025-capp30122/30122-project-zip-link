import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go

# Load the preprocessed data
data_path = "data/preprocessed/zipatlas_bulk_merge.csv"
df = pd.read_csv(data_path)

# List of non-discrete variables
non_discrete_vars = [
    "median_property_prices", "median_housing_costs", "owner_median_housing_costs",
    "renter_median_housing_costs", "housing_cost_perc_income", "unemployment_rates",
    "poverty_levels"
] 

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Chicago ZIP Code Comparison"),

    # Dropdowns to select ZIP codes
    html.Label("Select First ZIP Code:"),
    dcc.Dropdown(
        id='zip1-selector',
        options=[{'label': str(zip_code), 'value': zip_code} for zip_code in df["Zip Code"].unique()],
        value=df["Zip Code"].unique()[0],  # Default to first ZIP code
        clearable=False
    ),

    html.Label("Select Second ZIP Code:"),
    dcc.Dropdown(
        id='zip2-selector',
        options=[{'label': str(zip_code), 'value': zip_code} for zip_code in df["Zip Code"].unique()],
        value=df["Zip Code"].unique()[1],  # Default to second ZIP code
        clearable=False
    ),

    # Dropdown to select metric
    html.Label("Select Metric to Compare:"),
    dcc.Dropdown(
        id='var-selector',
        options=[{'label': var.replace('_', ' ').title(), 'value': var} for var in non_discrete_vars],
        value=non_discrete_vars[0],  # Default to first metric
        clearable=False
    ),

    # Bi-directional Bar Chart
    dcc.Graph(id='bi-bar-chart')
])

# Callback to update the chart based on user selection
@app.callback(
    dash.dependencies.Output('bi-bar-chart', 'figure'),
    [
        dash.dependencies.Input('zip1-selector', 'value'),
        dash.dependencies.Input('zip2-selector', 'value'),
        dash.dependencies.Input('var-selector', 'value')
    ]
)
def update_bi_bar_chart(zip1, zip2, selected_var):
    # Filter data for the selected ZIP codes
    df_selected = df[df["Zip Code"].isin([zip1, zip2])]

    # Extract values
    values_zip1 = df_selected[df_selected["Zip Code"] == zip1][selected_var].values[0]
    values_zip2 = df_selected[df_selected["Zip Code"] == zip2][selected_var].values[0]

    # Create a Bi-Directional Bar Chart
    fig = go.Figure()

    # Add bars for ZIP 1 (extending left)
    fig.add_trace(go.Bar(
        y=[selected_var.replace('_', ' ').title()],
        x=[-values_zip1],  # Negative for left alignment
        name=f"ZIP {zip1}",
        marker_color="blue",
        orientation='h'
    ))

    # Add bars for ZIP 2 (extending right)
    fig.add_trace(go.Bar(
        y=[selected_var.replace('_', ' ').title()],
        x=[values_zip2],  # Positive for right alignment
        name=f"ZIP {zip2}",
        marker_color="red",
        orientation='h'
    ))

    # Update layout
    fig.update_layout(
        title=f"Comparison of {selected_var.replace('_', ' ').title()} for ZIP {zip1} vs ZIP {zip2}",
        xaxis=dict(title="Value", zeroline=True, showgrid=True),
        yaxis=dict(title="Metric"),
        barmode="relative",
        bargap=0.2,
        bargroupgap=0.1
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)