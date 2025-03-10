#libraries
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from shapely.wkt import loads
from dash.dependencies import Input, Output

# Load the preprocessed data
data_path = "../data/preprocessed/zipatlas_bulk_merge.csv"
df = pd.read_csv(data_path)
df["Zip Code"] = df["Zip Code"].astype(str)

# Load ZIP Code shapefile
df_shapefile = pd.read_csv("Boundaries_-_ZIP_Codes_20250222.csv")
df_shapefile["ZIP"] = df_shapefile["ZIP"].astype(str)
df_shapefile["the_geom"] = df_shapefile["the_geom"].apply(loads)
gdf = gpd.GeoDataFrame(df_shapefile, geometry="the_geom", crs="EPSG:4326")
gdf.to_file("zcta_shapefile.shp", driver="ESRI Shapefile")
gdf_zcta = gpd.read_file("zcta_shapefile.shp")
gdf_zcta["ZIP"] = gdf_zcta["ZIP"].astype(str)
merged_gdf = gdf_zcta.merge(df, left_on='ZIP', right_on='Zip Code')
merged_gdf["lon"] = merged_gdf.geometry.centroid.x
merged_gdf["lat"] = merged_gdf.geometry.centroid.y
geojson_data = merged_gdf.to_json()

# Define variables
non_discrete_vars = [
    "median_property_prices", "median_housing_costs", "owner_median_housing_costs",
    "renter_median_housing_costs", "housing_cost_perc_income", "unemployment_rates",
    "poverty_levels", "Normalized Accessibility Index"
] 

# Dash App
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Zip & Link: Exploring Housing Prices and Access to Essential Services in Chicago"),

    html.Label("Select Variable:"),
    dcc.Dropdown(
        id="variable-dropdown",
        options=[{'label': var.replace('_', ' ').title(), 'value': var} for var in non_discrete_vars],
        value="median_property_prices",
        clearable=False
    ),

    dcc.Graph(id="choropleth-map"),
    dcc.Graph(id="scatter-plot"),
    
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

    dcc.Graph(id='price-chart'),
    dcc.Graph(id='housing-cost-chart'),
    dcc.Graph(id='economic-indicators-chart')
])

# Callback to update maps
@app.callback(
    [Output("choropleth-map", "figure"), Output("scatter-plot", "figure")],
    Input("variable-dropdown", "value")
)
def update_maps(selected_variable):
    fig_map = px.choropleth(
        merged_gdf, geojson=merged_gdf.geometry, locations=merged_gdf.index, color=selected_variable,
        hover_name="Zip Code", color_continuous_scale="Blues"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_scatter = px.scatter(df, x=selected_variable, y="Normalized Accessibility Index")
    return fig_map, fig_scatter

# Callback to update bar charts
@app.callback(
    [Output('price-chart', 'figure'), Output('housing-cost-chart', 'figure'), Output('economic-indicators-chart', 'figure')],
    [Input('zip1-selector', 'value'), Input('zip2-selector', 'value')]
)
def update_charts(zip1, zip2):
    df_selected = df[df["Zip Code"].isin([zip1, zip2])]
    price_metrics = ["median_property_prices"]
    housing_cost_metrics = ["median_housing_costs", "owner_median_housing_costs", "renter_median_housing_costs"]
    economic_metrics = ["housing_cost_perc_income", "poverty_levels", "unemployment_rates"]
    
    def create_bar_chart(metrics, title):
        fig = go.Figure()
        for i, zip_code in enumerate([zip1, zip2]):
            values = df_selected[df_selected["Zip Code"] == zip_code][metrics].values[0]
            fig.add_trace(go.Bar(y=metrics, x=values, name=f'ZIP {zip_code}', orientation='h'))
        fig.update_layout(title=title, xaxis_title='Value', yaxis_title='Metric', barmode='group')
        return fig
    
    fig1 = create_bar_chart(price_metrics, f'Comparison of Median Property Prices for ZIP {zip1} vs ZIP {zip2}')
    fig2 = create_bar_chart(housing_cost_metrics, f'Comparison of Housing Costs for ZIP {zip1} vs ZIP {zip2}')
    fig3 = create_bar_chart(economic_metrics, f'Comparison of Economic Indicators for ZIP {zip1} vs ZIP {zip2}')
    return fig1, fig2, fig3

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
