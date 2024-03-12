import plotly.express as px
from dataset import resample_data, get_localisation_data, add_counter_location
from ipyleaflet import Map, CircleMarker
from IPython.display import display

def line_plot(df, names, frequency):
    data = resample_data(df, names, frequency=frequency)
    return px.line(data,x="date", y="counts", color="name")


def update_time(df, time):
    data_localisation = get_localisation_data()
    df = add_counter_location(df)
    map_center = [data_localisation['results'][0]['coordinates']['lat'], data_localisation['results'][0]['coordinates']['lon']]
    m = Map(center=map_center, zoom=10)
    time = time.strftime("%m-%Y")
    if time in df['mois'].unique():
        max_volume = df['volume_month'].max()
        
        for record in data_localisation['results']:
            lon = record['coordinates']['lon']
            lat = record['coordinates']['lat']
            
            # Filtrage des données en fonction du temps
            filtered_data = df[(df['mois'] == time) & (df['name'] == record['name'])]
            volume = filtered_data['volume_month'].iloc[0] if not filtered_data.empty else 0
            
            # Calcul du rayon proportionnel au volume maximal
            scaled_radius = int(volume / max_volume * 50)  # 10 est le rayon maximal souhaité
            
            circle_marker = CircleMarker(location=(lat, lon), radius=scaled_radius, color="red", fill_color="red")
            m.add_layer(circle_marker)
    
    #display(m)
    return m

    # # Créer un slider interactif pour sélectionner une plage de dates
    # dates = [(date.month, date.year) for date in pd.date_range(start='2022-04-01', end='2024-02-01', freq='M')]
    # date_strings = [f"{month}-{year}" for month, year in dates]

    # time_slider = widgets.SelectionSlider(options=date_strings, description='Time Range:', layout={'width': '500px'})

    # # Mettre à jour la carte en fonction de la valeur du curseur
    # widgets.interact(update_time, time=time_slider)
