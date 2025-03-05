import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the preprocessed data for visualization
data_path = "../data/preprocessed/zipatlas_bulk_merge.csv"
df = pd.read_csv(data_path)

# List of non-discrete variables from ZipAtlas
non_discrete_vars = [
    "median_property_prices", "median_housing_costs", "owner_median_housing_costs",
    "renter_median_housing_costs", "housing_cost_perc_income", "unemployment_rates",
    "poverty_levels"
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Chicago Neighborhood Data Visualization"),

    # Dropdown to select variable to plot
    dcc.Dropdown(
        id='var-selector',
        options=[{'label': var.replace('_', ' ').title(), 'value': var} for var in non_discrete_vars],
        value=non_discrete_vars[0],  # Default to the first variable in the list
        clearable=False
    ),

    # Scatterplot
    dcc.Graph(id='scatter-plot')
])

# Callback to update scatterplot based on selected variable
@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('var-selector', 'value')]
)
def update_scatter(selected_var):
    avg_value = df[selected_var].mean()

    # Create the scatter plot with hover_data (just for the Zip Code)
    fig = px.scatter(
        df, 
        x=selected_var, 
        y="unemployment_rates", 
        title=f"{selected_var.replace('_', ' ').title()} vs Unemployment Rates",
        hover_data={
            'Zip Code': True,  # Include 'Zip Code' in hover
        }
    )

    # Add horizontal line for average unemployment rate - TEMPLATE ONLY! We actually want to plot the accessibility index
    avg_unemployment = df["unemployment_rates"].mean()
    fig.add_hline(
        y=avg_unemployment, 
        line_dash="dash", 
        line_color="red", 
        annotation_text="Average Unemployment Rate", 
        annotation_position="top left"
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

