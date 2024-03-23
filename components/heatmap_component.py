import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dataset import counters_list, frequencies_to_column


heatmap_frequency = list(frequencies_to_column.keys())


heatmap_Output = (
    Output(component_id='heatmap-chart', component_property='figure'),
)

heatmap_Input = (
    Input(component_id='heatmap-counter-dropdown', component_property='value'),
    Input(component_id='heatmap-frequency-dropdown', component_property='value')
)

heatmap_container = lambda df: dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Markdown("### Compteurs : "),
                dcc.Dropdown(["Tous"] + counters_list(df), None, id="heatmap-counter-dropdown")
            ], width=6),

            dbc.Col([
                dcc.Markdown("### Periode : "),
                dcc.Dropdown(heatmap_frequency, heatmap_frequency[0], id="heatmap-frequency-dropdown")
        ], width=6)]
    ),
    dbc.Row([
            dbc.Col([
                dcc.Graph(figure={}, id='heatmap-chart')
            ], width=12)
        ])
    ])