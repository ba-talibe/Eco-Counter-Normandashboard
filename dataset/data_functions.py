import pandas as pd
from datetime import timedelta
from typing import List
from .data_loading import add_counter_location
import requests


frequencies = {
    "journaliere" : "D",
    "horaire" : 'H',
    "mensuelle" : "M",
    "hebdomadaire" : "W"
}

def process_data(df):
    df['Time'] = pd.to_datetime(df['Date_JJMMAA HH:MM'].str.split('+').str[0],format="%Y-%m-%dT%H:%M:%S")
    df['Date'] = pd.to_datetime(df['Date_JJMMAA'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.day_of_week
    df['Hour'] = df['Time'].dt.hour
    df['Month-Year'] = pd.to_datetime(df['Month'].astype(str)+'-'+df['Year'].astype(str))
    
def counters_list(df):
    return sorted(df['name'].unique())



def resample_data(df, counter_names: List, start_date=None, end_date=None, period=None, frequency='journaliere'):
    
    def get_data_by_counter(name):
        date_range = pd.date_range(start=start_date, end=end_date, freq="H")
        date_range = date_range.intersection(df.index)
        data = df.loc[date_range]
        data = data.loc[data.name==name, ["counts", "name"]].resample(frequencies[frequency]).sum(numeric_only=True)
        data["name"] = name
        data["date"] = data.index
        return data
    
    if end_date is None:
        end_date = df.index[0]
    else:
        end_date = pd.to_datetime(end_date, format='%d-%m-%Y')

    if start_date is None:
        if period is not None:
            start_date = end_date - timedelta(days=period)
        else:
            start_date = df.index[-1]
    else:
        start_date = pd.to_datetime(start_date, format='%d-%m-%Y')


    
    data  = pd.concat([get_data_by_counter(name) for name in counter_names])
    return data

def prepare_map_data(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['Time'] = df['date']
    df['Date'] = pd.to_datetime(df['date_j'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.day_of_week

    # Convert 'Time' to datetime if it's not already
    df['Time'] = pd.to_datetime(df['Time'])

    # Extract the hour
    df['Hour'] = df['Time'].dt.hour




    # Ajout de la colonne 'Month-Year' à df
    df['Month-Year'] = df['Month'].astype(str) + '-' + df['Year'].astype(str)

    # L'URL de l'API pour localisation des sites de comptage
    counter_and_location_data =  add_counter_location(df)

    # Création d'une liste de tous les mois de janvier 2022 à janvier 2024
    months = counter_and_location_data['Month-Year'].unique()

    # Création de la liste de dictionnaires
    result_data = []
    for mois in months:
        for nom in counter_and_location_data['name'].unique():
            # Filtrage des données pour le mois et le nom
            filtered_data = counter_and_location_data[(counter_and_location_data['name'] == nom) & (counter_and_location_data['Month-Year'] == mois)]
            # Calcul de la somme des valeurs de la colonne 'counts' pour ces données filtrées
            sum_count = filtered_data['counts'].sum()
            # Ajout des données à la liste de dictionnaires
            result_data.append({'mois': mois, 'name': nom, 'volume_month': sum_count})

    # Création du DataFrame à partir de la liste de dictionnaires
    df_result = pd.DataFrame(result_data)
    return df_result




if __name__ == '__main__':
    from data_loading import load_dataset
    import os
    from datetime import timedelta



    df = load_dataset(os.getcwd()+"/dataset/", update=False)

    end_date = df.index[0]
    start_date = end_date - timedelta(days=7)


    resample_data(df, ["Eco 28 - Pont Jaurès ELBEUF", "Eco 00 - Quai du Havre ROUEN"], "20-12-2023", "20-02-2024")