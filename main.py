import os
from dataset import *
from charts import *
from components import *
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc




# update and load dataset
df = load_dataset("dataset", update=False)
f = list(frequencies.keys())

#global shared input
selected_counter = Input(component_id='selected-counter', component_property='value')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dbc.Row([
       dbc.Col([
           dcc.Markdown("# Compteur Vélo Sabine", style={ 'text-align' : 'center'})
       ], width=12)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("## Liste des compteurs : ", style={ 'text-align' : 'center'}),
       ], width=3),
        dbc.Col([
            dcc.Dropdown(counters_list(df), counters_list(df)[0], id="selected-counter")
       ], width=9)
    ]),
    html.Hr(),
    line_plot_container(df),
    bar_plot_container(df)

])
# dcc.Dropdown(f,f[0], id="frequency-dropdown")
@callback(*line_plot_Output, selected_counter, *line_plot_Input)
def update_line_plot(selected_counter, name, frequency, start_date, end_date):
    date_value = pd.to_datetime(start_date)
    return line_plot(df,[selected_counter, name], frequency)


@callback(*bar_plot_Output, selected_counter, *bar_plot_Input)
def update_bar_plot(selected_counter, name, frequency, start_date, end_date):
    date_value = pd.to_datetime(start_date)
    return bar_plot(df,[selected_counter, name], frequency)



# @callback(
#         Output(component_id="map-container", component_property="children"),
#         Input(component_id='date-range', component_property='date')
        
#         )
# def map_updater(date):
#     return {
#         "data": update_time(prepare_map_data(df), date).to_dict(),
#         "layout": "",
#         "config": ""
#     }

if __name__ == '__main__':
    app.run(debug=True,  port=8000)
    print("[+] Done")