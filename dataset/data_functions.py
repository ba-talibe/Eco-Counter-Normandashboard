import pandas as pd
from datetime import timedelta
from typing import List
from .data_loading import add_counter_location, get_localisation_data
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
    "jours" : "day_name",
    "mois" : "month_name",
}

counters_list = lambda df : sorted(df['name'].unique())
def process_data(df):
    df['Time'] = pd.to_datetime(df['Date_JJMMAA HH:MM'].str.split('+').str[0],format="%Y-%m-%dT%H:%M:%S")
    df['Date'] = pd.to_datetime(df['Date_JJMMAA'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.day_of_week
    df['Hour'] = df['Time'].dt.hour
    df['Month-Year'] = pd.to_datetime(df['Month'].astype(str)+'-'+df['Year'].astype(str))

def get_top_10_days(df):
    daily_counts = df.groupby('date_j')['counts'].sum().reset_index()

    # Trier par ordre décroissant pour obtenir les jours les plus fréquentés en premier
    top_10_days = daily_counts.sort_values(by='counts', ascending=False).head(10)

    top_10_days['date_j'] = pd.to_datetime(top_10_days['date_j'], format='%Y-%m-%d')
    top_10_days['date_j'] = top_10_days['date_j'].dt.strftime('%d %B %Y')
    return top_10_days



def get_date_range(df, start_date, end_date, period=None, frequency='H'):
    end_date = pd.to_datetime(df.index[0], ) if end_date is None else pd.to_datetime(end_date, utc=True)
    
    if start_date is None:
        if period is not None:
            start_date = end_date - timedelta(days=period)
        else:
            start_date = pd.to_datetime(df.index[-1])
    else:
        start_date = pd.to_datetime(start_date, utc=True)

    date_range = pd.date_range(start=start_date, end=end_date, freq=frequency)
    date_range = date_range.intersection(df.index)
    return date_range

def prepare_heatmap_data(df, counter_name, heatmap_freq, start_date=None, end_date=None, period=None ):
    
    date_range = get_date_range(df, start_date, end_date)
    if counter_name != "Tous":
        data = df[df['name'] == counter_name]
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


    categorie = day_order if heatmap_freq == "jours" else month_order

    data[heatmap_column[heatmap_freq]] = pd.Categorical(data[heatmap_column[heatmap_freq]], categories=categorie, ordered=True)


    return data.pivot_table(
        index='hours',
        columns=heatmap_column[heatmap_freq],
        values='counts',
        aggfunc='mean',
        fill_value=0,
    )

def add_time_columns(df):
    data = df.copy()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data["date"] = data.index
    data["day_name"] = data.date.dt.day_name()
    data['day_name'] = pd.Categorical(data['day_name'], categories=day_order, ordered=True) 
    data["hour"] = data.date.dt.hour
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.strftime('%b-%Y')
    return data


def prepare_bar_data(df, counter_names: List, start_date=None, end_date=None, period=None, frequency_column='jours'):
    
    def get_data_by_counter(name):
        data = df.loc[date_range]
        data = data.loc[data.name==name]

        data = add_time_columns(data)
        #data = data.loc[data.name==name, ["counts", "name"]].resample(frequencies[frequency]).sum(numeric_only=True)
        data = data[["counts", frequencies_to_column[frequency_column]]].groupby(frequencies_to_column[frequency_column]).mean()
        data["name"] = name
        data[frequencies_to_column[frequency_column]] = data.index
        return data

    date_range = get_date_range(df, start_date, end_date)

    return pd.concat([get_data_by_counter(name) for name in counter_names])
    

def resample_data(df, counter_names: List, start_date=None, end_date=None, period=None, frequency='journaliere'):

    
    def get_data_by_counter(name):
        data = df.loc[date_range]
        data = data.loc[data.name==name, ["counts", "name"]].resample(frequencies[frequency]).sum(numeric_only=True)
        data["name"] = name
        data["date"] = data.index
        return data

    date_range = get_date_range(df, start_date, end_date)

    data  = pd.concat([get_data_by_counter(name) for name in counter_names])
    return data

def prepare_map_data(df : pd.DataFrame):
    df = df.copy()
    df = add_time_columns(df)

    # L'URL de l'API pour localisation des sites de comptage
    df =  add_counter_location(df)

    # Création du DataFrame à partir de la liste de dictionnaires
    return df




if __name__ == '__main__':
    from data_loading import load_dataset
    import os
    from datetime import timedelta



    df = load_dataset(f"{os.getcwd()}/dataset/", update=False)

    print(prepare_heatmap_data(df, heatmap_freq="journaliere"))