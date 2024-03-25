import plotly.express as px
import dash_leaflet as dl
from dataset import resample_data, get_top_10_days, prepare_bar_data,prepare_heatmap_data, prepare_map_data, frequencies_to_column




def line_plot(df, names, frequency, start_date, end_date, x_col="date", y_col="counts"):
    data = resample_data(
        df, 
        [name for name in names if name != None], 
        frequency=frequency, 
        start_date=start_date, 
        end_date=end_date
        )
    return px.line(data,x="date", y="counts", color="name")

def bar_plot(df, names, frequency, start_date, end_date, x_col="date", y_col="counts"):
    data = prepare_bar_data(df, names, start_date=start_date, end_date=end_date, frequency_column=frequency)
    return px.bar(data,x=frequencies_to_column[frequency], y="counts", color="name", barmode="group",)

def plot_heatmap(df, counter_name, frequency, start_date=None, end_date=None):
    data = prepare_heatmap_data(df, counter_name, heatmap_freq=frequency)
    fig = px.imshow(data.to_numpy(), x=data.columns, y=data.index, color_continuous_scale='Viridis', aspect="auto")
    fig.update_traces(text=data.to_numpy(), texttemplate="%{z:.0f}")
    fig.update_xaxes(side="top")
    return fig

def render_map(df, selected_time, geojson_data, data_localisation):
    df = prepare_map_data(df)
    map_children = [
        dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
    ]
    
    # Si la valeur sélectionnée est nulle, utilisez le premier mois de la liste
    if not selected_time:
        selected_time = df['mois'].iloc[0]
    
    max_volume = df['volume_month'].max()
    
    for record in data_localisation['results']:
        lon = record['coordinates']['lon']
        lat = record['coordinates']['lat']
      
        filtered_data = df[(df['mois'] == selected_time) & (df['name'] == record['name'])]
        volume = 0 if filtered_data.empty else filtered_data['volume_month'].iloc[0]
        
        scaled_radius = int(volume / max_volume * 50)
        
        circle_marker = dl.CircleMarker(center=(lat, lon), radius=scaled_radius, color="red", fillColor="red")
        map_children.append(circle_marker)
    
    # Ajouter la couche GeoJSON (exemple fictif)
    map_children.append(dl.GeoJSON(data=geojson_data))

    return map_children

def plot_top_10_counter(df):
    top_10_days = get_top_10_days(df)

    # Créer le graphique à barres interactif avec Plotly
    fig = px.bar(top_10_days, x='date_j', y='counts', color='date_j', title='Top 10 des Jours les Plus Fréquentés (Sommes Journalières)',
                labels={'date_j': 'Date', 'counts': 'Passages Journaliers'})

    # Personnaliser l'apparence du graphique
    fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig.update_yaxes(title_text='Passages Journaliers')
    fig.update_layout(showlegend=False)

    # Afficher le graphique
    return fig