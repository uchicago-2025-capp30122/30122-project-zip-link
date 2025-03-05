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
import plotly.graph_objects as go

#*Adding Interactivity like Filters on top of viz: *
from dash.dependencies import Input, Output
import dash_leaflet as dl

#data sources
#https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-ZIP-Codes-Map/gdcf-axmw 
#To run code:
# uv run python visualization.py

#CSV ==> ShapeFile
#loading the data
df_chicago_unique = pd.read_csv("demo_data_for_visualization.csv")
df_chicago_unique['Zip code'] = df_chicago_unique['Zip code'].astype(str)

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
merged_gdf = gdf_zcta.merge(df_chicago_unique, left_on='ZIP', right_on='Zip code')

#GeoDataFrame to GeoJSON
geojson_data = merged_gdf.to_json()

#creating the Dash app
app = dash.Dash(__name__)

#choropleth map using Plotly Express
fig = px.choropleth(merged_gdf,
                    geojson = merged_gdf.geometry,
                    locations = merged_gdf.index,
                    color = "median_property_prices",
                    hover_name = "Zip code",
                    hover_data={"median_property_prices": ':$,.0f',
                                "accessibility_index": ':.2f',
                                "poverty_levels":':.2f',
                                "Unemployment rate":':.2f'},
                    color_continuous_scale = "Blues",
                    labels = {"median_property_prices": "Median Property Price (USD)",
                                "accessibility_index": "Accessibility Index",
                                "poverty_levels": "Poverty Level",
                                "Unemployment rate": "Unemployment Rate"})

#layout for display
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title="Chicago Median Property Prices by Zip Code",
    geo=dict(showcoastlines=True, coastlinecolor="Blue"),
    
)

#layout of the Dash app
app.layout = html.Div([
    html.H1("Chicago Zip Code Data Visualization"),
    dcc.Graph(id="choropleth-map", figure=fig),
])

#running the appi
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)

app.layout = html.Div([
    html.H1("Chicago Zip Code Data Visualization", style={"textAlign": "center"}),

    #dropdown menu
    html.Div([
        html.Label("Select Variable:", style={"fontSize": "16px", "fontWeight": "bold"}),
        dcc.Dropdown(
            id="variable-dropdown",
            options=[
                {'label': 'Median Property Prices', 'value': 'median_property_prices'},
                {'label': 'Number of Schools', 'value': 'school_count'},
                {'label': 'Number of Parks', 'value': 'park_count'},
            ],
            value='median_property_prices',
            clearable=False,
            style={"width": "60%", "margin": "auto"}
        ),
    ], style={"padding": "20px", "textAlign": "center"}),

    #Choropleth Map
    #to increase the size of the size of the map - not working
    #how to change the place of the map on the page
    dcc.Graph(id="choropleth-map", style={"height": "70vh", "width": "100%"}),

    #map overlay: Dash Leaflet
    #no change on the visualization
    html.Div([
        dl.Map([
            dl.TileLayer(
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                attribution="OpenStreetMap Contributors"
            ),
            dl.GeoJSON(
                id="geojson-layer",
                data=merged_gdf.__geo_interface__,
                style={"fillColor": "blue", "color": "black", "weight": 1, "fillOpacity": 0.5}
            ),
            dl.LayerGroup(id="labels-layer")
        ], id="map", center=[41.8781, -87.6298], zoom=10, style={"height": "70vh", "width": "100%"})
    ], style={"padding": "20px"})
])

#updating the map based on dropdown selection
#cannot see the dropdown
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
        color_continuous_scale="Blues_r",
        labels={selected_variable: selected_variable},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title=f"Chicago {selected_variable} by Zip Code",
        geo=dict(showcoastlines=True, coastlinecolor="Black"),
        coloraxis_colorbar=dict(
            title=selected_variable,
            tickformat=':$,.0f',
            ticks="outside",
        )
    )
    #to add the zip code labels on the map
    #not visible  on the map
    fig.add_trace(go.Scattergeo(
        lon=merged_gdf["lon"],
        lat=merged_gdf["lat"],
        mode="text",
        text=merged_gdf["Zip code"],
        textfont={"size": 10, "color": "black"},
        showlegend=False
    ))
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator"
    )
    fig.update_layout(
        height=900,  # Adjust height
        margin={"r":0, "t":50, "l":0, "b":0}
    )
    return fig