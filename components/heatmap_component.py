import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dataset import counters_list, heatmap_column


heatmap_frequency = list(heatmap_column.keys())


heatmap_Output = (
    Output(component_id='heatmap-chart', component_property='figure'),
)

heatmap_Input = (
    Input(component_id='heatmap-counter-dropdown', component_property='value'),
    Input(component_id='heatmap-frequency-dropdown', component_property='value'),
    Input(component_id='heatmap-date-range', component_property='start_date'),
    Input(component_id='heatmap-date-range', component_property='end_date')
)

heatmap_container = lambda df: dbc.Container([
    html.H2("Passages Moyens Horaires", className="mt-1 mb-1 title text-center"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("### Periode : "),
            dcc.DatePickerRange(
                id="heatmap-date-range",
                min_date_allowed=df.index[-1],
                max_date_allowed=df.index[0],
                start_date=df.index[-1],
                end_date=df.index[0],
            )
        ], width=4),
        dbc.Col([
            dcc.Markdown("### Compteurs : "),
            dcc.Dropdown(["Tous"] + counters_list(df), None, id="heatmap-counter-dropdown")
        ], width=4),
        dbc.Col([
            dcc.Markdown("### Periode : "),
            dcc.Dropdown(heatmap_frequency, heatmap_frequency[0], id="heatmap-frequency-dropdown")
        ], width=4)],
        className="mb-1"
    ),
    dbc.Row([
            dbc.Col([
                dcc.Graph(figure={}, id='heatmap-chart', style={'height': '70vh'})
            ], width=12)
        ], style={'width': '100%', 'height': '60vh'}),
    html.Br(),
    html.Br()
    ], className="chart-container")