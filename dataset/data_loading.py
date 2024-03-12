import os
import json
import requests
import numpy as np
import pandas as pd


datacount_base_url = f"https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records"
add_counter_location_base_url = f"https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-sites/records"

def update_local_data(local_data_df : pd.DataFrame, update_data_dict : dict, json_file_path, csv_file_path):
    list_local_data =local_data_df.to_dict(orient='records')
    update_data_dict.extend(list_local_data)
    # Utilisez json.dump() pour sauvegarder le dictionnaire dans le fichier JSON
    df=pd.DataFrame(update_data_dict)
    with open(json_file_path, 'w') as fichier_json:
        json.dump(update_data_dict, fichier_json)

    df.to_csv(csv_file_path, index=False)

def update_dataset(path):
    # L'URL de l'API pour donné de compteur 
    limit_datacount = 100 # télécharger 100 données mais ne pas saugarder localement 
    offset_datacount = 0
    #api avec un filtre "order by" dans l'ordre décroissant de dates dans datacount
    api_url_datacount = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?order_by=date%20DESC&limit=" + str(limit_datacount) +"&offset=" + str(offset_datacount)

    #L'URL de l'API pour localisation des sites de comptage
    api_url_localisation = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-sites/records?limit=29"

    #L'URL de l'API pour télécharger toutes les données 
    api_url_export = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/exports/json?lang=fr&timezone=Europe%2FBerlin"

    json_file_path = os.path.join(path, 'local_data.json')
    csv_file_path = os.path.join(path, 'local_data.csv')

 

    # #local_data telecharge depuis serveur
    local_data = pd.read_json(json_file_path)

    update_data = [] # initialise update_data par une liste

    dateEtHeure = local_data.iloc[0]['date'][:-12] # pour avoir la forme de variable dateEtHeure identique que celle declarée dessus

    #L'URL de l'API pour la mise à jour de données (where date > dateEtHeure le plus récent indiqué dans local_data, order by date descendant, timezone Europe/Berlin)
    api_url_update_data ="https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?where=date%3Edate'"+dateEtHeure+"%3A00%3A00%2B01%3A00'&order_by=date%20DESC&limit="+str(limit_datacount)+"&offset="+str(offset_datacount)+"&timezone=Europe%2FBerlin"


    # Effectuer une requête GET pour obtenir les données
    response_updateData = requests.get(api_url_update_data) # dictionnaire (indice total_count, indice results)
    response_localisation = requests.get(api_url_localisation)

    if (response_updateData.status_code != 200):
    
        print(f'Échec de la requête HTTP, code de statut {response_updateData.status_code}')

    if (response_localisation.status_code != 200):
    
        print(f'Échec de la requête HTTP, code de statut {response_localisation.status_code}')



    # Si la requête a réussi (code de statut HTTP 200), vous pouvez accéder aux données
    data_localisation = response_localisation.json()

    total_count = response_updateData.json()['total_count']

    print(total_count)

    if (total_count != 0) : # le nombre de données mises à jour 
        while (total_count >= 100) : # data limit is 100
            incomming_data = requests.get(api_url_update_data).json()
            if "results" not in incomming_data:
                print("resultat inatendu ", incomming_data)
                update_local_data(local_data, update_data, json_file_path, csv_file_path)

                update_dataset(path) 
            update_data.extend(incomming_data["results"])
            total_count -= 100
            offset_datacount +=  100
            api_url_update_data ="https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?where=date%3Edate'"+dateEtHeure+"%3A00%3A00%2B01%3A00'&order_by=date%20DESC&limit="+str(limit_datacount)+"&offset="+str(offset_datacount)+"&timezone=Europe%2FBerlin"

        limit_datacount = total_count
        api_url_update_data ="https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?where=date%3Edate'"+dateEtHeure+"%3A00%3A00%2B01%3A00'&order_by=date%20DESC&limit="+str(limit_datacount)+"&offset="+str(offset_datacount)+"&timezone=Europe%2FBerlin"
        
        

        incomming_data = requests.get(api_url_update_data).json()
        if "results" not in incomming_data:
            print("resultat inatendu ", incomming_data)
            update_local_data(local_data, update_data, json_file_path, csv_file_path)
            update_dataset(path) 
             
        update_data.extend(incomming_data['results'])
        update_local_data(local_data, update_data, json_file_path, csv_file_path)

def update_csv_dataset(path):
    # L'URL de l'API pour donné de compteur 
    limit_datacount = 100 # télécharger 100 données mais ne pas saugarder localement 
    offset_datacount = 0
    dateEtHeure ='2023-12-24T23'
    #api avec un filtre "order by" dans l'ordre décroissant de dates dans datacount
    api_url_datacount = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?order_by=date%20DESC&limit=" + str(limit_datacount) +"&offset=" + str(offset_datacount)

    #L'URL de l'API pour localisation des sites de comptage
    api_url_localisation = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-sites/records?limit=29"

    #L'URL de l'API pour télécharger toutes les données 
    api_url_export = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/exports/json?lang=fr&timezone=Europe%2FBerlin"

    json_file_path = os.path.join(path, 'local_data.json')
    csv_file_path = os.path.join(path, 'local_data.csv')

 

    # #local_data telecharge depuis serveur
    local_data = pd.read_csv(csv_file_path)

    update_data = [] # initialise update_data par une liste

    dateEtHeure = local_data.iloc[0]['date'][:-12] # pour avoir la forme de variable dateEtHeure identique que celle declarée dessus

    #L'URL de l'API pour la mise à jour de données (where date > dateEtHeure le plus récent indiqué dans local_data, order by date descendant, timezone Europe/Berlin)
    api_url_update_data ="https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?where=date%3Edate'"+dateEtHeure+"%3A00%3A00%2B01%3A00'&order_by=date%20DESC&limit="+str(limit_datacount)+"&offset="+str(offset_datacount)+"&timezone=Europe%2FBerlin"


    # Effectuer une requête GET pour obtenir les données
    response_updateData = requests.get(api_url_update_data) # dictionnaire (indice total_count, indice results)
    response_localisation = requests.get(api_url_localisation)

    if (response_updateData.status_code != 200):
    
        print(f'Échec de la requête HTTP, code de statut {response_updateData.status_code}')

    if (response_localisation.status_code != 200):
    
        print(f'Échec de la requête HTTP, code de statut {response_localisation.status_code}')



    # Si la requête a réussi (code de statut HTTP 200), vous pouvez accéder aux données
    data_localisation = response_localisation.json()

    total_count = response_updateData.json()['total_count']

    print(total_count)

    if (total_count != 0) : # le nombre de données mises à jour 
        while (total_count >= 100) : # data limit is 100
            update_data.extend(requests.get(api_url_update_data).json()['results'])
            total_count -= 100
            offset_datacount +=  100
            api_url_update_data ="https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?where=date%3Edate'"+dateEtHeure+"%3A00%3A00%2B01%3A00'&order_by=date%20DESC&limit="+str(limit_datacount)+"&offset="+str(offset_datacount)+"&timezone=Europe%2FBerlin"

        limit_datacount = total_count
        api_url_update_data ="https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-data/records?where=date%3Edate'"+dateEtHeure+"%3A00%3A00%2B01%3A00'&order_by=date%20DESC&limit="+str(limit_datacount)+"&offset="+str(offset_datacount)+"&timezone=Europe%2FBerlin"
        update_data.extend(requests.get(api_url_update_data).json()['results'])
        list_local_data =local_data.to_dict(orient='records')
        update_data.extend(list_local_data)
        # Utilisez json.dump() pour sauvegarder le dictionnaire dans le fichier JSON
        df.drop_duplicates(subset='id', inplace=True)
        df=pd.DataFrame(update_data)
        df.to_csv(csv_file_path, index=False)
        
        
cwd = os.getcwd()

def load_dataset(path, parse_dates=False, index_col="id", update=True):
    if update:
        update_dataset(path)
    csv_file_path = os.path.join(path, "local_data.csv")

    df = pd.read_csv(csv_file_path, parse_dates=True, index_col="date")
    df.index = pd.to_datetime(df.index, utc=True)
    return df


def get_localisation_data():
       
    api_url_localisation = "https://data.metropole-rouen-normandie.fr/api/explore/v2.1/catalog/datasets/eco-counter-sites/records?limit=29"
    response_localisation = requests.get(api_url_localisation)

    if response_localisation.status_code != 200:
        print(f'Échec de la requête HTTP, code de statut {response_localisation.status_code}')
        data_localisation = None
    else:
        data_localisation = response_localisation.json()
    return data_localisation



def add_counter_location(df):

    
    data_localisation = get_localisation_data()

    # Création d'un DataFrame à partir des données de localisation
    data_localisation_df = pd.DataFrame(data_localisation['results'])

    # Fusion des DataFrames df et data_localisation_df sur la colonne 'name'
    df_merged = pd.merge(df, data_localisation_df[['name', 'coordinates']], how='left', on='name')

    months = df_merged['Month-Year'].unique()

    # Création de la liste de dictionnaires
    result_data = []
    for mois in months:
        for nom in df_merged['name'].unique():
            # Filtrage des données pour le mois et le nom
            filtered_data = df_merged[(df_merged['name'] == nom) & (df_merged['Month-Year'] == mois)]
            # Calcul de la somme des valeurs de la colonne 'counts' pour ces données filtrées
            sum_count = filtered_data['counts'].sum()
            # Ajout des données à la liste de dictionnaires
            result_data.append({'mois': mois, 'name': nom, 'volume_month': sum_count})

    # Création du DataFrame à partir de la liste
    return pd.DataFrame(result_data)


if __name__ == '__main__':
    #load_dataset(os.getcwd() + "/data_toolset")
    print("Done")