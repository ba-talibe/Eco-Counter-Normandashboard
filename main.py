from dataset import load_dataset
from charts import *
from components import *
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc




# update and load dataset
df = load_dataset("dataset", update=True)
f = list(frequencies.keys())


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app.layout = dbc.Container([
    html.Br(),
    html.Br(),
    dbc.Row([
       dbc.Col([
           dcc.Markdown("# Fréquentation des Pistes Cyclables", style={ 'text-align' : 'center'}, className="title")
       ], width=12)
    ]),
    map_container(prepare_map_data(df)),
    html.Hr(),
    station_container(df),
    html.Hr(),
    stats_container(df),
    html.Hr(),
    heatmap_container(df),
    html.Hr(),
    line_plot_container(df),
    html.Hr(),   
    bar_plot_container(df),
])
# dcc.Dropdown(f,f[0], id="frequency-dropdown")
@callback(*line_plot_Output, *line_plot_Input)
def update_line_plot(selected_counter, name, frequency, start_date, end_date):
    date_value = pd.to_datetime(start_date)
    return line_plot(df,[selected_counter, name], frequency, start_date=start_date, end_date=end_date)


@callback(*bar_plot_Output, *bar_plot_Input)
def update_bar_plot(selected_counter, name, frequency, start_date, end_date):
    return bar_plot(df,[selected_counter, name], frequency, start_date=start_date, end_date=end_date)



@callback(*map_Output, *map_Input)
def update_map(selected_time):
    return render_map(df, selected_time, geojson_data, data_localisation)

@callback(*heatmap_Output, *heatmap_Input)
def update_heatmap(selected_counter, frequency, start_date, end_date):
    return plot_heatmap(df,selected_counter, frequency, start_date, end_date)


if __name__ == '__main__':
    app.run(port=8000)
    print("[+] Done")
