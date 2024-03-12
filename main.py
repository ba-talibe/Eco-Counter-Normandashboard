from dash import Dash, html, dash_table,dcc, callback, Output, Input
import os
from dataset import *
from charts import line_plot, update_time


print(os.getcwd())

# update and load dataset
df = load_dataset("dataset", update=False)


app = Dash(__name__)
f = list(frequencies.keys())
app.layout = html.Div([
    html.Div(children='Compteur Vélo Sabine'),
    html.Div([
        dcc.Dropdown(counters_list(df), counters_list(df)[0], id="counter-dropdown"),
        dcc.Dropdown(f,f[0], id="frequency-dropdown")
        ]),

        html.Div([
            dcc.DatePickerSingle(
                id="date-range",
                min_date_allowed=df.index[-1],
                max_date_allowed=df.index[0],
                date=df.index[0]
            )
        ]),
    html.Div([
        # The id here should match the ID used in the JavaScript below
        html.Div(id="map-container"),
        # JavaScript to render the ipyleaflet map
        dcc.Markdown("""
        ```javascript
        // JavaScript to render the ipyleaflet map
        const ipyleafletMap = document.querySelector("#map-container");
        const mapJSON = {data: JSON.parse(`{{data}}`), layout: JSON.parse(`{{layout}}`), config: JSON.parse(`{{config}}`)};
        const mapFigure = window.PyDeck.Deck(jsonString, ipyleafletMap);
        mapFigure.render();
        ```
        """)
    ]),
    dcc.Graph(figure={}, id='time-graph')
])

@callback(Output(component_id='time-graph', component_property='figure'),
        Input(component_id='counter-dropdown', component_property='value'), 
        Input(component_id='frequency-dropdown', component_property='value'))
def update_line(name, frequency):
    fig1 = line_plot(df,[name], frequency)
    return fig1


@callback(
        Output(component_id="map-container", component_property="children"),
        Input(component_id='date-range', component_property='date')
        
        )
def map_updater(date):
    return {
        "data": update_time(df, date).to_dict(),
        "layout": "",
        "config": ""
    }

if __name__ == '__main__':
    app.run(debug=True)