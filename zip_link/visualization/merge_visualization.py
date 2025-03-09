
#libraries
import plotly
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_leaflet as dl

#data sources
#https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-ZIP-Codes-Map/gdcf-axmw 
#To run code:
# uv run python merge_visualization.py

#CSV ==> ShapeFile
#loading the data
df_chicago_unique = pd.read_csv("../data/preprocessed/zipatlas_bulk_merge.csv")
df_chicago_unique['Zip Code'] = df_chicago_unique['Zip Code'].astype(str)

#creating the shapefile
df_shapefile = pd.read_csv("Boundaries_-_ZIP_Codes_20250222.csv")
df_shapefile["ZIP"] = df_shapefile["ZIP"].astype(str)

#convert WKT geometry column to Shapely geometries
df_shapefile["the_geom"] = df_shapefile["the_geom"].apply(loads)
df_shapefile["SHAPE_AREA"] = df_shapefile["SHAPE_AREA"] / 1e6

#convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df_shapefile, geometry="the_geom", crs="EPSG:4326")

#save as a shapefile
gdf.to_file("zcta_shapefile.shp", driver="ESRI Shapefile")

#loading ZCTA shapefile
zcta_shapefile = ("zcta_shapefile.shp")
gdf_zcta = gpd.read_file(zcta_shapefile)
gdf_zcta['ZIP'] = gdf_zcta['ZIP'].astype(str)

#merging the data with the shapefile
merged_gdf = gdf_zcta.merge(df_chicago_unique, left_on='ZIP', right_on='Zip Code')


#computing centroids for labeling
merged_gdf["lon"] = merged_gdf.geometry.centroid.x
merged_gdf["lat"] = merged_gdf.geometry.centroid.y

#GeoDataFrame to GeoJSON
geojson_data = merged_gdf.to_json()

# Define variables
non_discrete_vars = [
    "median_property_prices", "median_housing_costs", "owner_median_housing_costs",
    "renter_median_housing_costs", "housing_cost_perc_income", "unemployment_rates",
    "poverty_levels"
] 

format_dict = {
    "median_property_prices": lambda x: f"${x:,.2f}",
    "median_housing_costs": lambda x: f"${x:,.2f}",
    "owner_median_housing_costs": lambda x: f"${x:,.2f}",
    "renter_median_housing_costs": lambda x: f"${x:,.2f}",
    "housing_cost_perc_income": lambda x: f"{x:.2f}%",
    "unemployment_rates": lambda x: f"{x:.2f}%",
    "poverty_levels": lambda x: f"{x:.2f}%"
}

#creating the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Chicago Zip Code Data Visualization", style={"textAlign": "center"}),

    # Dropdown to select variable for both maps
    html.Div([
        html.Label("Select Variable:"),
        dcc.Dropdown(
            id="variable-dropdown",
            options=[{'label': var.replace('_', ' ').title(), 'value': var} for var in non_discrete_vars],
            value="median_property_prices",
            clearable=False,
            style={"width": "50%", "margin": "auto"}
        ),
    ], style={"textAlign": "center", "padding": "20px"}),

    # Choropleth Map (Plotly)
    html.Div([
        dcc.Graph(id="choropleth-map", style={"position": "relative", "zIndex": 1})
    ]),

    # Scatter Plot
    html.Div([
        dcc.Graph(id="scatter-plot")
    ])
])

# Callback to update both maps based on dropdown selection
@app.callback(
    [Output("choropleth-map", "figure"),
     Output("scatter-plot", "figure")],
    Input("variable-dropdown", "value")
)
def update_visualizations(selected_variable):
    # Mapping variable names to display-friendly labels
    variable_titles = {
        "median_property_prices": "Median Property Prices",
        "median_housing_costs": "Median Housing Costs",
        "owner_median_housing_costs": "Owner Median Housing Costs",
        "renter_median_housing_costs": "Renter Median Housing Costs",
        "housing_cost_perc_income": "Housing Cost % of Income",
        "unemployment_rates": "Unemployment Rates",
        "poverty_levels": "Poverty Levels",
    }

    # Choropleth Map
    fig_map = px.choropleth(
        merged_gdf,
        geojson=merged_gdf.geometry,
        locations=merged_gdf.index,
        color=selected_variable,
        hover_name="Zip Code",
        hover_data={selected_variable: ':.0f',
                    "median_property_prices": ':$,.0f',
                    "Normalized Accessibility Index": ':.2f',
                    "poverty_levels":':.2f',
                    "unemployment_rates":':.2f'},
        color_continuous_scale="Blues",
        labels={selected_variable: variable_titles.get(selected_variable, selected_variable),
                "median_property_prices": "Median Property Price (USD)",
                "Normalized Accessibility Index": "Accessibility Index",
                "poverty_levels": "Poverty Level",
                "unemployment_rates": "Unemployment Rate"},
    )
    
    fig_map.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
    fig_map.update_layout(
        title=f"{variable_titles.get(selected_variable, selected_variable)} in Chicago by Zip Code",
        geo=dict(showcoastlines=True, coastlinecolor="Blue"),
        coloraxis_colorbar=dict(
            title=variable_titles.get(selected_variable, selected_variable),
            tickformat=':$,.0f',
            ticks="outside",
        )
    )

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

    # Scatter Plot
    formatted_column_name = selected_variable.replace('_', ' ').title()
    df_chicago_unique[formatted_column_name] = df_chicago_unique[selected_variable].apply(format_dict[selected_variable])

    fig_scatter = px.scatter(
        df_chicago_unique,
        x=selected_variable,
        y="Normalized Accessibility Index",
        title=f"{variable_titles.get(selected_variable, selected_variable)} vs Accessibility Index",
        hover_data={
            'Zip Code': True,
            selected_variable: False,
            formatted_column_name: True,
            'Normalized Accessibility Index': True
        }
    )

    avg_accessibility_index = df_chicago_unique["Normalized Accessibility Index"].mean()
    fig_scatter.add_hline(
        y=avg_accessibility_index,
        line_dash="dash",
        line_color="red",
        annotation_text="Average Accessibility Index",
        annotation_position="top left"
    )

    return fig_map, fig_scatter

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
