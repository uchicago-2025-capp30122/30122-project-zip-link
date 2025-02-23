#Necessary packages download: 
import dash
import plotly
import pandas as pd

#for shapefiles
import geopandas as gpd
from shapely.wkt import loads

#DASH APP:

import dash
from dash import dcc, html
import plotly.express as px

#*Adding Interactivity like Filters on top of viz: *
from dash.dependencies import Input, Output

#data sources
#https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-ZIP-Codes-Map/gdcf-axmw 
#       (CSV to be converted to a shapefile)
#To run code: uv run python visualization.py

#CSV ==> ShapeFile
#loading the data
df_chicago_unique = pd.read_csv("demo_data_for_visualization.csv")
df_chicago_unique['Zip code'] = df_chicago_unique['Zip code'].astype(str)

#creating the shapefile
df_shapefile = pd.read_csv("Boundaries_-_ZIP_Codes_20250222.csv")
df_shapefile["ZIP"] = df_shapefile["ZIP"].astype(str)

# Convert WKT geometry column to Shapely geometries
df_shapefile["the_geom"] = df_shapefile["the_geom"].apply(loads)
df_shapefile["SHAPE_AREA"] = df_shapefile["SHAPE_AREA"] / 1e6

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df_shapefile, geometry="the_geom", crs="EPSG:4326")

# Save as a shapefile
gdf.to_file("zcta_shapefile.shp", driver="ESRI Shapefile")

# Load the ZCTA shapefile
zcta_shapefile = ("zcta_shapefile.shp")
gdf_zcta = gpd.read_file(zcta_shapefile)
print(gdf_zcta.columns)
gdf_zcta['ZIP'] = gdf_zcta['ZIP'].astype(str)

# Merge the data with the shapefile
merged_gdf = gdf_zcta.merge(df_chicago_unique, left_on='ZIP', right_on='Zip code')

# Create the Dash app
app = dash.Dash(__name__)

# Create the choropleth map using Plotly Express
fig = px.choropleth(merged_gdf,
                    geojson=merged_gdf.geometry,
                    locations=merged_gdf.index,
                    color="median_property_prices",
                    hover_name="Zip code",
                    hover_data=["median_property_prices"],
                    color_continuous_scale="Viridis_r",
                    labels={"median_property_prices": "Median Property Price (USD)"})

# Update layout for proper display
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title="Chicago Median Property Prices by Zip Code",
    geo=dict(showcoastlines=True, coastlinecolor="Black"),
)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Chicago Zip Code Data Visualization"),
    dcc.Graph(id="choropleth-map", figure=fig),
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)

# Update layout to include a dropdown for selecting the variable
app.layout = html.Div([
    html.H1("Chicago Zip Code Data Visualization"),
    dcc.Dropdown(
        id="variable-dropdown",
        options=[
            {'label': 'Median Property Prices', 'value': 'median_property_prices'},
            {'label': 'Number of Schools', 'value': 'school_count'},
            {'label': 'Number of Parks', 'value': 'park_count'},
            # Add more options if needed
        ],
        value = 'median_property_prices',
    ),
    dcc.Graph(id="choropleth-map")
])

# Update the map based on dropdown selection
@app.callback(
    Output("choropleth-map", "figure"),
    Input("variable-dropdown", "value")
)
def update_map(selected_variable):
    fig = px.choropleth(
        merged_gdf,
        geojson=merged_gdf.geometry,
        locations=merged_gdf.index,
        color=selected_variable,
        hover_name="Zip code",
        hover_data=[selected_variable],
        color_continuous_scale="YlGnBu",
        labels={selected_variable: selected_variable}
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title=f"Chicago {selected_variable} by Zip Code",
        geo=dict(showcoastlines=True, coastlinecolor="Black"),
    )
    return fig