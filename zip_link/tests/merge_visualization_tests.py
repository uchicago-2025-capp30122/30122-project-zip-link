import pytest
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

@pytest.fixture
def app():
    app = Dash(__name__)
    app.layout = html.Div([
        dcc.Dropdown(
            id="variable-dropdown",
            options=[
                {'label': 'Median Property Prices', 'value': 'median_property_prices'},
                {'label': 'Number of Schools', 'value': 'school_count'},
                {'label': 'Number of Parks', 'value': 'park_count'},
                {'label': 'Poverty Levels', 'value': 'poverty_levels'},
                {'label': 'Unemployment Rates', 'value': 'unemployment_rates'},
            ],
            value='median_property_prices',
            clearable=False,
            style={"width": "50%", "margin": "auto"}
        ),
        html.Div(id='output-container', style={"textAlign": "center"}),
        dcc.Graph(id='choropleth-map')  # Assuming you want to test the map too
    ])

    @app.callback(
        Output('output-container', 'children'),
        Input('variable-dropdown', 'value')
    )
    def update_output(selected_variable):
        return f'You have selected: {selected_variable}'

    return app


def test_app_layout(app):
    """
    Tests if the layout is as should be
    """
    dropdown, output_div = app.layout.children[0], app.layout.children[1]

    assert isinstance(dropdown, dcc.Dropdown)
    assert dropdown.id == "variable-dropdown"
    assert isinstance(output_div, html.Div)
    assert output_div.id == "output-container"

def test_dropdown_options(app):
    """
    Tests if the dropdown options are available
    """
    dropdown = app.layout.children[0]
    option_labels = [option['label'] for option in dropdown.options]

    expected_labels = ['Median Property Prices', 'Number of Schools', 'Number of Parks', 'Poverty Levels', 'Unemployment Rates']
    assert all(label in option_labels for label in expected_labels)
