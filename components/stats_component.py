from dash_bootstrap_components import Container, Row , Col
from dash import dcc, Input, Output
from dash.html import  H3, H4, H5, H6, Hr, Span
from dataset import counters_list, frequencies_to_column
from charts import plot_top_10_counter
from dataset import get_stats

velos_hier = 10
upper_arrow = "▲"

lower_arrow = "▼"

stats_Output = (
    Output(component_id='10-most-visited-counter', component_property='figure'),
)

def stats_container(df):
    yesterday_stats, last_week, last_year_same_week = get_stats(df)
    
    return Container([
    Row([
        Col([
            Row([
                Col([
                    H4(f"{yesterday_stats[0]}",className="stats-number")
                ]),
                Col([
                    H6(f"vélos comptabilisés hier sur {29} stations.")
                ])
            ]),
            Row([
                Col([
                    H6("Soit"),
                    H4(f"{lower_arrow if yesterday_stats[2]<0 else upper_arrow} {yesterday_stats[2]:.1f} %", className="stats-number")
                ]),
                Col([
                    H6(f"par rapport à la semaine d'avant avec", style={'display': 'inline'}),
                    Span(f" {yesterday_stats[1]}",className="stats-number", style={'display': 'inline'}),
                    H6("vélos sur 7 jours sur 29 stations.")
                ])
            ]),
            Hr(),
           Row([
                Col([
                    H4(f"{last_week[0]}",className="stats-number")
                ]),
                Col([
                    H6(f"vélos comptabilisés sur une semaine (jusqu'hier) sur 7 jours sur 29 stations")
                ])
            ]),
            Row([
                Col([
                    H6("Soit"),
                    H4(f"{lower_arrow if last_week[2]<0 else upper_arrow} {last_week[2]:.1f} %", className="stats-number")
                ]),
                Col([
                    H6(f"par rapport à la semaine d'avant avec", style={'display': 'inline'}),
                    Span(f" {last_week[1]}",className="stats-number", style={'display': 'inline'}),
                    H6("vélos sur 7 jours sur 29 stations.")
                ])
            ]),
             Row([
                Col([
                    H6("Et"),
                    H4(f"{lower_arrow if last_year_same_week[1]<0 else upper_arrow} {last_year_same_week[1]:.1f} %", className="stats-number")
                ]),
                Col([
                    H6(f"par rapport à la même semaine l'année dernière avec", style={'display': 'inline'}),
                    Span(f" {last_year_same_week[0]}",className="stats-number", style={'display': 'inline'}),
                    H6("vélos sur 7 jours sur 21 stations.")
                ])
            ]),
        ], width=3),
        Col([
            dcc.Graph(figure=plot_top_10_counter(df), id='10-most-visited-counter', style={"height" : '100%'})
        ], width=9)
        ]),
    Row([

        ])
    ], className="chart-container")