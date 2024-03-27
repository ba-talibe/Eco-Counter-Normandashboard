import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dataset import counters_list, frequencies


f = list(frequencies.keys())

line_plot_Output = (
    Output(component_id='line_plot_chart', component_property='figure'),
)

line_plot_Input = (
        Input(component_id='line-plot-selected-counter', component_property='value'),
        Input(component_id='line-plot-compare-dropdown', component_property='value'),
        Input(component_id='line-plot-frequency-dropdown', component_property='value'),
        Input(component_id='line-plot-date-range', component_property='start_date'),
        Input(component_id='line-plot-date-range', component_property='end_date')
)

line_plot_container = lambda df: dbc.Container([
    html.H2("Tendance Temporelle", className="mt-1 mb-1 title text-center"),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("### Liste des compteurs : ", style={ 'text-align' : 'left'}, className=""),
       ], width=3),
        dbc.Col([
            dcc.Dropdown(counters_list(df), counters_list(df)[0], id="line-plot-selected-counter")
       ], width=9)
    ], className="mt-1 mb-1"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("### Periode : "),
            dcc.DatePickerRange(
                id="line-plot-date-range",
                min_date_allowed=df.index[-1],
                max_date_allowed=df.index[0],
                start_date=df.index[-1],
                end_date=df.index[0],
            )
        ], width=4),

        dbc.Col([
            dcc.Markdown("### Frequence : "),
            dcc.Dropdown(f, f[0], id="line-plot-frequency-dropdown")
        ], width=4),

        dbc.Col([
            dcc.Markdown("### Comparer à : "),
            dcc.Dropdown(["None"]+counters_list(df), None, id="line-plot-compare-dropdown")
    ], width=4)],
    className="mb-1"
    ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='line_plot_chart')
        ], width=12)
    ]),
    html.Br(),
    html.Br()
    ], className="chart-container")