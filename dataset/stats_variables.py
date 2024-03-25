import calendar
import pandas as pd
from datetime import timedelta


def get_stats(df):
    # Calculer la date d'hier

    df = df.copy()
    df.date_j = pd.to_datetime(df.date_j)
    hier = pd.Timestamp.now().normalize() - timedelta(days=1)

    # Filtrer les données pour obtenir les vélos comptabilisés hier
    velos_hier = df[df['date_j'] == hier]['counts'].sum()

    # Calculer la date de 1 semaine avant hier
    une_semaine_avant_hier = hier - timedelta(days=7)

    # Filtrer les données pour obtenir les vélos comptabilisés sur cette date
    velos_une_semaine_avant_hier = df[df['date_j'] == une_semaine_avant_hier]['counts'].sum()


    # Calculer l'évolution par rapport à la semaine précédente
    evol_semaine_prec = ((velos_hier - velos_une_semaine_avant_hier) / velos_une_semaine_avant_hier) * 100

    # Filtrer les données pour obtenir les vélos comptabilisés sur une semaine (jusqu'à hier) sur 7 jours
    semaine_prec = hier - timedelta(days=7)
    velos_semaine_prec = df[(df['date_j'] > semaine_prec) & (df['date_j'] <= hier)]['counts'].sum()

    # Calculer la date d'hie, une semaine avant hier, et 2 semaines avant hier
    hier = pd.Timestamp.now().normalize() - timedelta(days=1)
    semaine_avant_hier = hier - timedelta(days=7)
    semaine_a_a_hier = semaine_avant_hier - timedelta(days=7)

    # Filtrer les données pour obtenir les vélos comptabilisés sur une période de 7 jours jusqu'à deux semaines avant hier
    velos_2_semaine_avant_hier = df[(df['date_j'] > semaine_a_a_hier) & (df['date_j'] <= semaine_avant_hier)]['counts'].sum()

    # Calculer l'évolution par rapport à la semaine précédente
    evol_2_semaine_prec = ((velos_semaine_prec - velos_2_semaine_avant_hier) / velos_2_semaine_avant_hier) * 100

    # Vérifier si l'année précédente est bissextile
    annee_bissextile = calendar.isleap(hier.year - 1)

    # Calculer la date d'un an avant hier en fonction de l'année bissextile
    if annee_bissextile:
        un_an_avant_hier = hier - timedelta(days=365)
    else:
        un_an_avant_hier = hier - timedelta(days=366)

    # Filtrer les données pour obtenir les vélos comptabilisés sur une période de 7 jours jusqu'à un an avant hier
    periode_un_an_avant_hier = un_an_avant_hier - timedelta(days=7)
    velos_un_an_avant_hier = df[(df['date_j'] > periode_un_an_avant_hier) & (df['date_j'] <= un_an_avant_hier)]['counts'].sum()

    # Calculer l'évolution par rapport à la même semaine de l'année dernière
    evol_semaine_annee_derniere = ((velos_semaine_prec - velos_un_an_avant_hier) / velos_un_an_avant_hier) * 100

    return (velos_hier, velos_une_semaine_avant_hier, evol_semaine_prec ), \
            (velos_semaine_prec, velos_2_semaine_avant_hier, evol_2_semaine_prec ), \
            (velos_un_an_avant_hier, evol_semaine_annee_derniere)
