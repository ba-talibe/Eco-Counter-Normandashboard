from dash_bootstrap_components import Row, Col, Container
from dash import dcc, html, Input, Output
from dash.html import H3, H4, H5
import dash_leaflet as dl
from dash_leaflet import CircleMarker
from dataset import  get_localisation_data


geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [1.0993, 49.4431]  # Exemple de coordonnées (lon, lat)
            }
        }
    ]
}

map_Output = (
    Output(component_id='leaflet-map', component_property='children'), 
)

map_Input = (
        Input(component_id='month-dropdown', component_property='value'),
)

data_localisation = get_localisation_data()

lat = data_localisation['results'][5]['coordinates']['lat']
lon = data_localisation['results'][5]['coordinates']['lon']

map_container = lambda df: Container([
    html.Hr(),
    html.H2('Volume par Mois', className="title text-center"),
    html.Br(),
    Row([
        Col([
            H4("Choisissez un mois", className="sub-title")
        ], width=4, className="mb-1"),
        Col([
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in df['mois'].unique()],
                value=df['mois'][0],
                placeholder='Select a month'
            )
        ], width=8),
        Col([
            dl.Map(
            id='leaflet-map',
            style={'width': '100%', 'height': '50vh'},
            center=[lat, lon],
            zoom=10,
            children=[
                dl.TileLayer(),
                dl.FeatureGroup([
                    dl.EditControl(id="edit_control"),
                ]),
                dl.GeoJSON(id='map-geojsons', data=geojson_data)  # Ajout de la couche GeoJSON
                ]
            )
        ], width=12)
    ])
    ], className="chart-container") 