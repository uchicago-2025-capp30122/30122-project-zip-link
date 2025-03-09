
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
# uv run python visualization.py

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

#creating the Dash app
app = dash.Dash(__name__)

#choropleth map using Plotly Express
fig = px.choropleth(merged_gdf,
                    geojson = merged_gdf.geometry,
                    locations = merged_gdf.index,
                    color = "median_property_prices",
                    hover_name = "Zip Code",
                    hover_data={"median_property_prices": ':$,.0f',
                                "Normalized Accessibility Index": ':.2f',
                                "poverty_levels":':.2f',
                                "unemployment_rates":':.2f'},
                    color_continuous_scale = "Blues",
                    labels = {"median_property_prices": "Median Property Price (USD)",
                                "Normalized Accessibility Index": "Accessibility Index",
                                "poverty_levels": "Poverty Level",
                                "unemployment_rates": "Unemployment Rate"})

#layout for display
fig.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
fig.update_layout(
    title="Chicago Median Property Prices by Zip Code",
    geo=dict(showcoastlines=True, coastlinecolor="Blue"),  
)

app.layout = html.Div([
    html.H1("Chicago Zip Code Data Visualization", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Variable:"),
        dcc.Dropdown(
            id="variable-dropdown",
            options=[
                {'label': 'Median Property Prices', 'value': 'median_property_prices'},
                {'label': 'Number of Schools', 'value': 'school_count'},
                {'label': 'Number of Parks', 'value': 'park_count'},
                {'label': 'Number of Health Services', 'value': 'total_health_services'},
                {'label': 'Number of Public Transport Transits', 'value': 'num_public_transit'},
                {'label': 'Number of Grocery Stores', 'value': 'grocery_store_count'},
                {'label': 'Poverty Levels', 'value': 'poverty_levels'},
                {'label': 'Unemployment rate', 'value': 'Unemployment rate'}
            ],
            value='median_property_prices',
            clearable=False,
            style={"width": "50%", "margin": "auto"}
        ),
    ], style={"textAlign": "center", "padding": "20px"}),

    #choropleth Map (Plotly)
    html.Div([
        dcc.Graph(id="choropleth-map", figure=fig, style={"position": "relative", "zIndex": 1})
    ])
])

#updating the map based on dropdown selection
@app.callback(
    Output("choropleth-map", "figure"),
    Input("variable-dropdown", "value")
)
variable_titles = {
    "median_property_prices": "Median Property Prices",
    "school_count": "Number of Schools",
    "total_health_services": "Number of Health Services",
    "num_public_transit_stops": "Number of Public Transport Transits",
    "grocery_store_count": "Number of Grocery Stores",
    "park_count": "Number of Parks",
    "Unemployment rate": "Unemployment Rates",
    "poverty_levels": "Poverty Levels",
    }
    
    fig = px.choropleth(
        merged_gdf,
        geojson=merged_gdf.geometry,
        locations=merged_gdf.index,
        color=selected_variable,
        hover_name="Zip code",
        hover_data={selected_variable: ':.0f',
                        "median_property_prices": ':$,.0f',
                        "accessibility_index": ':.2f',
                        "poverty_levels":':.2f',
                        "Unemployment rate":':.2f'},
        color_continuous_scale="Blues",
        labels={selected_variable: variable_titles.get(selected_variable, selected_variable),
                "median_property_prices": "Median Property Price (USD)",
                "accessibility_index": "Accessibility Index",
                "poverty_levels": "Poverty Level",
                "Unemployment rate": "Unemployment Rate"},
    )
    fig.update_geos(fitbounds="locations", visible=False, projection_type="mercator")

    fig.update_layout(
        title=f"{variable_titles.get(selected_variable, selected_variable)} in Chicagoby Zip Code",
        geo=dict(showcoastlines=True, coastlinecolor="Blue"),
        coloraxis_colorbar=dict(
            title=variable_titles.get(selected_variable, selected_variable),
            tickformat=':$,.0f',
            ticks="outside",
        )
    )
    )

    #to add the zip code labels on the map
    fig.add_trace(go.Scattergeo(
        lon=merged_gdf["lon"],
        lat=merged_gdf["lat"],
        mode="text",
        text=merged_gdf["Zip Code"],
        textfont={"size": 6, "color": "black"},
        showlegend=False
    ))

    #figure size
    fig.update_layout(
        height = 750,
        width = 1700,
        margin = {"r":50, "t":50, "l":0, "b":0}
    )
    return fig

#running the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
