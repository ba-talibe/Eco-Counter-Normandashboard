import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dataset import counters_list, frequencies_to_column


bar_frequency = list(frequencies_to_column.keys())

bar_plot_Output = (
    Output(component_id='bar-plot-chart', component_property='figure'),
)

bar_plot_Input = (
        Input(component_id='bar-plot-compare-dropdown', component_property='value'),
        Input(component_id='bar-plot-frequency-dropdown', component_property='value'),
        Input(component_id='bar-plot-date-range', component_property='start_date'),
        Input(component_id='bar-plot-date-range', component_property='end_date')
)

bar_plot_container = lambda df: dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Markdown("### Periode : "),
                dcc.DatePickerRange(
                    id="bar-plot-date-range",
                    min_date_allowed=df.index[-1],
                    max_date_allowed=df.index[0],
                    start_date=df.index[-1],
                    end_date=df.index[0],
                )
            ], width=4),

            dbc.Col([
                dcc.Markdown("### Frequence : "),
                dcc.Dropdown(bar_frequency, bar_frequency[0], id="bar-plot-frequency-dropdown")
            ], width=4),

            dbc.Col([
                dcc.Markdown("### Comparer à : "),
                dcc.Dropdown(["None"]+counters_list(df), None, id="bar-plot-compare-dropdown")
        ], width=4)]
    ),
    dbc.Row([
            dbc.Col([
                dcc.Graph(figure={}, id='bar-plot-chart')
            ], width=12)
        ])
    ])