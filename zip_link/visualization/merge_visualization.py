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



non_discrete_vars = [
    "median_property_prices", "median_housing_costs", "owner_median_housing_costs",
    "renter_median_housing_costs", "housing_cost_perc_income", "unemployment_rates",
    "poverty_levels", "park_count", "total_healthcare_services", "num_public_transit_stops", "grocery_store_count" ,"school_count", "Normalized Accessibility Index"
] 
format_dict = {
    "median_property_prices": lambda x: f"${x:,.2f}",
    "median_housing_costs": lambda x: f"${x:,.2f}",
    "owner_median_housing_costs": lambda x: f"${x:,.2f}",
    "renter_median_housing_costs": lambda x: f"${x:,.2f}",
    "housing_cost_perc_income": lambda x: f"{x:.2f}%",
    "unemployment_rates": lambda x: f"{x:.2f}%",
    "poverty_levels": lambda x: f"{x:.2f}%",
    "park_count": lambda x:x,
    "total_healthcare_services": lambda x:x,
    "num_public_transit_stops": lambda x:x, 
    "grocery_store_count": lambda x:x,
     "school_count": lambda x:x,
    "Normalized Accessibility Index": lambda x: x 
}

app = dash.Dash(__name__)
# App layout
app.layout = html.Div(style={"backgroundColor": "#041C24", "padding": "20px"}, children=[
    html.H1("Zip & Link: Exploring Housing Prices and Access to Essential Services in Chicago", 
            style={"textAlign": "center", "fontSize": "30px", "color": "#E1E1E8", "font-weight": "bold", "font-family": "Times, sans-serif"}),

    # Abstract or brief description below the title
    html.P("This dashboard examines the connection between housing prices in Chicago and the accessibility to essential services at a zip-code level. We focus on five key services: healthcare, schools, public transit, grocery stores, and parks to calculate an Accessibility Index, which encapsulates how easily people can reach these essential services within a given area. We've also included additional economic indicators such as unemployment rates and poverty levels to extract any other relevant insights. Feel free to select the variables you'd like to visualize and let us know what you think. Enjoy exploring!", 
           style={"textAlign": "left", "fontSize": "17px", "color": "#E1E1E8", "marginTop": "10px", "font-family": "Times, sans-serif"}),
    
    # Dropdown to select variable for both map and scatter
    html.Div([
        html.Label("Select Variable:", style={"fontSize": "18px", "color": "#E1E1E8"}),
        dcc.Dropdown(
            id="variable-dropdown",
            options=[{'label': var.replace('_', ' ').title(), 'value': var} for var in non_discrete_vars],
            value="median_property_prices",
            clearable=False,
            style={"width": "100%", "margin": "auto", "backgroundColor": "#ffffff", "border": "1px solid #ddd"}
        ),
    ], style={"textAlign": "center", "padding": "20px"}),


    dcc.Graph(id="choropleth-map"),
    dcc.Graph(id="scatter-plot"),

    html.Label("Select First ZIP Code:",style={"fontSize": "18px", "color": "#E1E1E8"}),
    dcc.Dropdown(
        id='zip1-selector',
        options=[{'label': str(zip_code), 'value': zip_code} for zip_code in df["Zip Code"].unique()],
        value=df["Zip Code"].unique()[0],
        clearable=False, 
    ),

    html.Label("Select Second ZIP Code:", style={"fontSize": "18px", "color": "#E1E1E8"}),
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
def update_visualizations(selected_variable):

    formatted_column_name = selected_variable.replace('_', ' ').title()
    merged_gdf[formatted_column_name] = merged_gdf[selected_variable].apply(format_dict[selected_variable])

    variable_titles = {
        "median_property_prices": "Median Property Prices",
        "median_housing_costs": "Median Housing Costs",
        "owner_median_housing_costs": "Owner Median Housing Costs",
        "renter_median_housing_costs": "Renter Median Housing Costs",
        "housing_cost_perc_income": "Housing Cost % of Income",
        "unemployment_rates": "Unemployment Rates",
        "poverty_levels": "Poverty Levels",
        'school_count': "Number of Schools",
        'park_count': "Number of Parks",
        "total_healthcare_services": "Number of Health Services",
        "num_public_transit_stops": "Number of Public Transport Transits",
        "grocery_store_count": 'Number of Grocery Stores',
        "poverty_levels": 'Poverty Levels',
        "Normalized Accessibility Index": "Normalized Accessibility Index"
    }

    fig_map = px.choropleth_map(
        merged_gdf,
        geojson=merged_gdf.geometry,
        locations=merged_gdf.index,
        color=selected_variable,
        hover_name="Zip Code",
        hover_data={selected_variable: ':.0f',
                        "median_property_prices": ':$,.0f',
                        "Accessibility Index": ':.2f',
                        "poverty_levels":':.2f',
                        "unemployment_rates":':.2f'},
        color_continuous_scale="Blues",
        labels={selected_variable: variable_titles.get(selected_variable, selected_variable),
                "median_property_prices": "Median Property Price (USD)",
                "Accessibility Index": "Accessibility Index",
                "poverty_levels": "Poverty Level",
                "unemployment_rates": "Unemployment Rate"},
        opacity=0.8,
        center={"lat": 41.8500, "lon": -87.6000},
        zoom=9.69,
    )

    fig_map.update_geos(
        fitbounds="locations", 
        visible=False, 
        projection_type="mercator",
        showcountries=True,
        showcoastlines=True,
        coastlinecolor="black"
    )

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
        textposition="top center",
        textfont={"size": 12, "color": "black"},
        showlegend=False,
        hoverinfo="skip"
    ))

    # Figure size
    fig_map.update_layout(
        height=750,
        width=1415,
        margin={"r": 50, "t": 50, "l": 0, "b": 0}
    )
    
    # Scatter Plot

    df[formatted_column_name] = df[selected_variable].apply(format_dict[selected_variable])


    fig_scatter = px.scatter(
        df,
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
def update_bar_charts(zip1, zip2):
    df_selected = df[df["Zip Code"].isin([zip1, zip2])]
    colors = ["#1f77b4", "#85C1E9"]  # Different shades of blue
    
    def create_bar_chart(metrics, title):
        fig = go.Figure()
        for i, zip_code in enumerate([zip1, zip2]):
            values = df_selected[df_selected["Zip Code"] == zip_code][metrics].values[0]
            fig.add_trace(go.Bar(y=metrics, x=values, name=f'ZIP {zip_code}', marker=dict(color=colors[i]), orientation='h'))
        fig.update_layout(title=title, xaxis_title='Value', yaxis_title='Metric', barmode='group')
        return fig
    
    fig1 = create_bar_chart(["median_property_prices"], "Comparison of Median Property Prices Across 2 Zip Codes")
    fig2 = create_bar_chart(["median_housing_costs", "owner_median_housing_costs", "renter_median_housing_costs"], "Comparison of Housing Costs Across 2 Zip Codes")
    fig3 = create_bar_chart(["housing_cost_perc_income", "poverty_levels", "unemployment_rates"], "Comparison of Economic Indicators Across 2 Zip Codes")
    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
