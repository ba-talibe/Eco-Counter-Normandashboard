import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
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

map_container = lambda df: dbc.Container([
   html.Div([
        html.Div(['Select Month'], style={'width': '37%', 'display': 'inline-block'}),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in df['mois'].unique()],
            value=df['mois'][0],
            placeholder='Select a month'
        )
    ]),
    html.Div([
        html.H2('Add Shapes to Map an Area of Interest'),
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
    ])
    ])