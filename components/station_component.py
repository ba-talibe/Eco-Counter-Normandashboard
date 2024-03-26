from dash_bootstrap_components import Container, Row , Col, Card, CardBody, CardFooter
from dash.html import   Span, Img, H2, H6, H5, P
from charts import plot_top_10_counter
from dataset import get_stats


def station_container(df):

    # Calculer le nombre total moyen de passages par jour pour chaque station
    station_stats = df.groupby(['id', 'name', 'photourl']).agg(total_passages=('counts', 'sum'), total_days=('date_j', 'nunique')).reset_index()
    station_stats['average_passages_per_day'] = station_stats['total_passages'] / station_stats['total_days']

    # Classer les stations par le nombre total moyen de passages par jour de manière décroissante
    top_stations = station_stats.sort_values(by='average_passages_per_day', ascending=False).head(5)
    top_stations.reset_index()
    return Container([
        H2("Top 5 des Stations", style={ 'text-align' : 'center'}),
        Row([
            Col(
                [Card([
                    CardBody([
                        Img(src=row['photourl'], style={"width": "100%"}, className="counter_img")
                    ]),
                    CardFooter([
                        Row([
                            H5(f"{i + 1}", className="badge badge-primary", style={"diplay": "inline"}),
                            H6(f" {row['name']}",className="stats-number"),
                            Row([
                            Col([ H6(f"{row['average_passages_per_day']:.0f}", className="stats-number mt-1", style={"diplay": "inline"})], width=3),
                            Col([ P("Vélos en moyenne par jours")], width=9)
                            ])
                            
                        ])
                    ], className="text-muted")]
                )],
                width=3  # Adjust the column width as needed
            ) for i, (_, row) in enumerate(top_stations.iterrows())
            ])
    ], className="chart-container")