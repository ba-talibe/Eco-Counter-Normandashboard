import pandas as pd
from datetime import timedelta
from typing import List
from .data_loading import add_counter_location
import requests


frequencies = {
    "horaire" : 'H',
    "journaliere" : "D",
    "mensuelle" : "M",
    "hebdomadaire" : "W"
}

frequencies_to_column = {
    "horaire" : 'hour',
    "journaliere" : "day_name",
    "mensuelle" : "month",
    "annuelle" : "year"
}

heatmap_column  = {
    "journaliere" : "day_name",
    "mensuelle" : "month_name",
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



def prepare_heatmap_data(df, counter_names: list, start_date=None, end_date=None, period=None, heatmap_freq='journaliere'):
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

    date_range = pd.date_range(start=start_date, end=end_date, freq="H")
    date_range = date_range.intersection(df.index)
    #data = df[df['name'].isin(counter_names)]
    data = df[["counts"]].loc[date_range].groupby([pd.Grouper(freq="h")]).mean()



    data["date"] = data.index
    data['month_name'] = data['date'].dt.strftime('%B')
    data["day_name"] = data['date'].dt.day_name()
    data["hours"] = data.date.dt.hour


    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'
    ]

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


    categorie = day_order if heatmap_freq == "journaliere" else month_order

    data[heatmap_column[heatmap_freq]] = pd.Categorical(data[heatmap_column[heatmap_freq]], categories=categorie, ordered=True)


    heatmap_data = data.pivot_table(index='hours', columns=heatmap_column[heatmap_freq], values='counts', aggfunc='mean', fill_value=0)

    return heatmap_data



def prepare_bar_data(df, counter_names: List, start_date=None, end_date=None, period=None, frequency_column='journaliere'):
    
    def get_data_by_counter(name):
        date_range = pd.date_range(start=start_date, end=end_date, freq="H")
        date_range = date_range.intersection(df.index)
        data = df.loc[date_range]
        data = data.loc[data.name==name]
        #data = data.loc[data.name==name, ["counts", "name"]].resample(frequencies[frequency]).sum(numeric_only=True)

        data["date"] = data.index
        data["day_name"] = data.date.dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data['day_name'] = pd.Categorical(data['day_name'], categories=day_order, ordered=True) 
        data["hour"] = data.date.dt.hour
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.strftime('%b-%Y')
        data = data[["counts", frequencies_to_column[frequency_column]]].groupby(frequencies_to_column[frequency_column]).mean()
        data["name"] = name
        data[frequencies_to_column[frequency_column]] = data.index
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

def prepare_map_data(df : pd.DataFrame):
    df = df.copy()
    print(df.columns)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['hours'] = pd.to_datetime(df['date'])
    df['Time'] = df['date']
    df['Date'] = pd.to_datetime(df['date_j'])
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_of_week

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

    print(prepare_heatmap_data(df, heatmap_freq="journaliere"))