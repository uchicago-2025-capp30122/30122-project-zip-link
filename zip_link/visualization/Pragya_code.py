import dash
from dash import dcc, html
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_leaflet as dl

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

app = dash.Dash(__name__)
# App layout
app.layout = html.Div(style={"backgroundColor": "#f4f4f4", "padding": "20px"}, children=[
    html.H1("Zip & Link: Exploring Housing Prices and Access to Essential Services in Chicago", 
            style={"textAlign": "center", "fontSize": "30px", "color": "#2a3f5f", "font-weight": "bold"}),

    # Abstract or brief description below the title
    html.P("This dashboard examines the connection between housing prices and various economic indicators, including housing costs, unemployment rates, poverty rates, and access to essential services. We focus on five key services: healthcare, schools, public transit, grocery stores, and parks within Chicago. Using this data, we have developed an Accessibility Index to investigate how it correlates with these economic factors across different Zip Codes in the city. Feel free to select the variables you'd like to visualize and explore their distribution across the city. Enjoy exploring!", 
           style={"textAlign": "left", "fontSize": "16px", "color": "#888", "marginTop": "10px"}),
    
    html.Div([
    html.Label("Select Variable:"),
    dcc.Dropdown(
        id="variable-dropdown",
        options=[{'label': var.replace('_', ' ').title(), 'value': var} for var in df.columns if var not in ["Zip Code", "lon", "lat"]],
        value="median_property_prices",
        clearable=False,
        style={"width": "100%", "margin": "auto", "backgroundColor": "#ffffff", "border": "1px solid #ddd"}
    ),
    ], style={"textAlign": "center", "padding": "20px"}),


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
        hover_name="Zip Code", color_continuous_scale="Viridis"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    
    # Add zip code labels
    fig_map.add_trace(go.Scattergeo(
        lon=merged_gdf["lon"],
        lat=merged_gdf["lat"],
        mode="text",
        text=merged_gdf["Zip Code"],
        textfont={"size": 7, "color": "black"},
        showlegend=False,
        hoverinfo="skip"
    ))

    # Figure size
    fig_map.update_layout(
        height=750,
        width=1680,
        margin={"r": 50, "t": 50, "l": 0, "b": 0}
    )
    
    fig_scatter = px.scatter(df, x=selected_variable, y="Normalized Accessibility Index", hover_name="Zip Code")
    
    # Add horizontal line for average Normalized Accessibility Index
    avg_accessibility_index = df["Normalized Accessibility Index"].mean()
    fig_scatter.add_hline(
        y=avg_accessibility_index, 
        line_dash="dash", 
        line_color="red", 
        annotation_text="Average Accessibility Index", 
        annotation_position="top left"
    )
    
    return fig_map, fig_scatter

# Callback to update bar charts
@app.callback(
    [Output('price-chart', 'figure'), Output('housing-cost-chart', 'figure'), Output('economic-indicators-chart', 'figure')],
    [Input('zip1-selector', 'value'), Input('zip2-selector', 'value')]
)
def update_charts(zip1, zip2):
    df_selected = df[df["Zip Code"].isin([zip1, zip2])]
    colors = ["#1f77b4", "#85C1E9"]  # Different shades of blue
    
    def create_bar_chart(metrics, title):
        fig = go.Figure()
        for i, zip_code in enumerate([zip1, zip2]):
            values = df_selected[df_selected["Zip Code"] == zip_code][metrics].values[0]
            fig.add_trace(go.Bar(y=metrics, x=values, name=f'ZIP {zip_code}', marker=dict(color=colors[i]), orientation='h'))
        fig.update_layout(title=title, xaxis_title='Value', yaxis_title='Metric', barmode='group')
        return fig
    
    fig1 = create_bar_chart(["median_property_prices"], "Comparison of Median Property Prices")
    fig2 = create_bar_chart(["median_housing_costs", "owner_median_housing_costs", "renter_median_housing_costs"], "Comparison of Housing Costs")
    fig3 = create_bar_chart(["housing_cost_perc_income", "poverty_levels", "unemployment_rates"], "Comparison of Economic Indicators")
    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
