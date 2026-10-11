# -------------------------------------------------------------
# PROJET Prediction de salaires : analyse et modélisation
# AUTEUR : Caleb
# DATE   : Août 2026
# SOURCE : Annonces Glassdoor scrapées (Kaggle) - marché US, salaires en USD
# --------------------------------------------------------------


# importation des bibliothèques nécessaires

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Lecture du fichier CSV contenant les données de salaires

data = pd.read_csv('glassdoor_jobs.csv')

print("la dimension du dataset est : ")
print(data.shape)

# L'audit des données : vérification des valeurs manquantes et des types de données

print("\nAperçu des premières lignes du dataset :")
print(data.head())

print("\nInformations sur les valeurs manquantes :")
print(data.isnull().sum())

print("\nTypes de données des colonnes :")
print(data.dtypes)

print("\ninformations sur les doublons :")
print(data.duplicated().sum())

# Recherce des valeurs précises dans les colonnes spécifiques

print("\nLignes où la colonne 'Competitors' a la valeur '-1' :")
print(data[data['Competitors'] == '-1'])

# méthode compte les True avec df.isnull().sum() pour chaque colonne et affiche le résultat

print("\nComptage des valeurs manquantes sur la colonne 'Competitors' :")

print((data['Competitors'] == '-1').sum())

# vérification des valeurs dans chaque colonne pour identifier les valeurs aberrantes ou incohérentes

for col in data.columns:
    print(f"\nValeurs manquantes dans la colonne '{col}':")
    print((data[col] == '-1' ).sum())

# vérification des valeurs dans la colonne  'rating'

print("\nVérification des valeurs dans la colonne 'Rating' :")
print((data['Rating'] == '-1').sum())


# vérification des valeurs négatives dans la colonne 'Rating'
print("\nVérification des valeurs négatives dans la colonne 'Rating' :")
print((data['Rating'] < 0).sum())

# -- Transformatio et nétoyage des données

data = data.replace(['-1', -1], np.nan)
print(data.isnull().sum())

# Nettoyage de la colonne "Salary Estimate" en supprimant les mentions "(Glassdoor est.)"
print("\nNettoyage de la colonne 'Salary Estimate' : suppression des mentions '(Glassdoor est.)'")
data["Salary Estimate"] = data["Salary Estimate"].str.replace('(Glassdoor est.)', '')

# Nettoyage de la colonne "Salary Estimate" en supprimant les mentions "(Employer est.)"
print("\nNettoyage de la colonne 'Salary Estimate' : suppression des mentions '(Employer est.)'")
data["Salary Estimate"] = data["Salary Estimate"].str.replace('(Employer est.)', '')


# Vérification de la présence de la mention "Employer Provided" dans la colonne "Salary Estimate"
print(data["Salary Estimate"].str.contains("Employer Provided").sum())

# ligne temporaire pour compter combien contiennent "Per Hour"
print(data["Salary Estimate"].str.contains("Per Hour").sum())


# Nettoyage de la colonne "Salary Estimate" en supprimant la mention "Employer Provided Salary:"
data['Salary Estimate'] = data['Salary Estimate'].str.replace('Employer Provided Salary:', '')


# Nettoyage de la colonne "Salary Estimate" en supprimant les lignes contenant "Per Hour"
data = data[ ~(data["Salary Estimate"].str.contains("Per Hour"))]


# Nettoyage de la colonne "Salary Estimate" en supprimant les symboles '$' et 'K'
data["Salary Estimate"] = data["Salary Estimate"].str.replace('$', '')
data["Salary Estimate"] = data["Salary Estimate"].str.replace('K', '')
data["Salary Estimate"] = data["Salary Estimate"].str.strip()

# Vérification des premières lignes de la colonne "Salary Estimate" après nettoyage
print(data["Salary Estimate"].head())

# Vérification des valeurs manquantes dans la colonne "Salary Estimate"
print((data["Salary Estimate"] == '').sum())


# Vérification de la présence de la mention "Employer Provided" dans la colonne "Salary Estimate" après nettoyage
print(data["Salary Estimate"].str.contains("Employer Provided").sum())


# ligne qui crée une nouvelle colonne salaire_max

data['Salaire_Max'] = data['Salary Estimate'].str.split('-', expand=True)[1].astype(float)


# ligne qui crée une nouvelle colonne salaire_min
data['Salaire_Min'] = data['Salary Estimate'].str.split('-', expand=True)[0].astype(float)

# Vérification des premières lignes des colonnes "Salary Estimate", "Salaire_Min" et "Salaire_Max"
print(data[['Salary Estimate', 'Salaire_Min', 'Salaire_Max']].head())
print(data.shape)

# ligne qui crée Salaire_Moyen

print("\nCréation de la ligne qui créé la colonne 'Salaire_Moyen' :")
data["Salaire_Moyen"] = (data["Salaire_Max"] + data["Salaire_Min"])/2
print(data[['Salaire_Moyen', 'Salaire_Min', 'Salaire_Max']].head())


# ligne qui crée une colonne Ville à partir du premier morceau de Location.

data["Ville"] = data["Location"].str.split(',', expand=True)[0]

# la ligne pour Etat, avec le second morceau.
data["Etat"] = data["Location"].str.split(',', expand=True)[1]
print(data[['Location', 'Ville', 'Etat']].head())

# la ligne qui crée une colonne Entreprise avec le nom seul.

data["Company Name"] = data["Company Name"].str.split('\n', expand=True)[0]
print(data[['Company Name', 'Ville', 'Etat']].head())

# Suppresion de la colonne Competitors qui contient trop de valeurs manquantes
print("\nSuppression de la colonne 'Competitors' qui contient trop de valeurs manquantes :")
data = data.drop(columns=['Competitors', 'Unnamed: 0'])
print(data.shape)

# la ligne qui remplace les NaN de Rating par la médiane.
data["Rating"] = data["Rating"].fillna(data["Rating"].median())
print("\nVérification des valeurs manquantes dans la colonne 'Rating' après remplacement par la médiane :")
print(data["Rating"].isnull().sum())

# la ligne pour Industry, puis celle pour Sector,en les passes simplement la chaîne "Inconnu".

data["Industry"] = data["Industry"].fillna("Inconnu")
data["Sector"] = data["Sector"].fillna("Inconnu")
print("\nVérification des valeurs manquantes dans les colonnes 'Industry' et 'Sector' après remplacement par 'Inconnu' :")

print(data["Sector"].isnull().sum())

# pour les les quatre lignes pour Headquarters, Size, Type of ownership et Revenue, sur le même modèle.
print("\nRemplacement des valeurs manquantes dans les colonnes 'Headquarters', 'Size', 'Type of ownership' et 'Revenue' par 'Inconnu' :")
data["Headquarters"] = data["Headquarters"].fillna("Inconnu")
data["Size"] = data["Size"].fillna("Inconnu")
data["Type of ownership"] = data["Type of ownership"].fillna("Inconnu")
data["Revenue"] = data["Revenue"].fillna("Inconnu") 

print(data["Industry"].isnull().sum())
print(data["Sector"].isnull().sum())
print(data["Headquarters"].isnull().sum())
print(data["Size"].isnull().sum())
print(data["Type of ownership"].isnull().sum())
print(data["Revenue"].isnull().sum())   




# Suppression des lignes où Salaire_Moyen est manquant
data = data.dropna(subset=['Salaire_Moyen'])
print("\nVérification de la suppression des lignes où Salaire_Moyen est manquant :")
print(data.shape)

# vérification globale

print("\nVérification globale des valeurs manquantes après nettoyage :")
print(data.isnull().sum())

# création de la colonne age_entreprise, puis imputation.

data["age_entreprise"] = 2020 - data["Founded"]
data["age_entreprise"] = data["age_entreprise"].fillna(data["age_entreprise"].median())
data = data.drop(columns=['Founded'])
print("\nVérification des valeurs manquantes dans la colonne 'age_entreprise' après imputation :")
print(data["age_entreprise"].isnull().sum())
print(data["age_entreprise"].describe())


# vérification des valeurs extrêmes dans la colonne "age_entreprise"

#print("\nVérification des valeurs extrêmes dans la colonne 'age_entreprise' :")
#print(data[data["age_entreprise"] > 150][["Company Name", "Founded", "age_entreprise"]].head(10))

# Regroupement des intitulés de poste en familles de métiers

print("\nLes 15 intitulés les plus fréquents :")
print(data["Job Title"].value_counts().head(15))

def classer_poste(titre):
    titre = titre.lower()
    if 'data scientist' in titre:
        return 'data scientist'
    elif 'data engineer' in titre:
        return 'data engineer'
    elif 'data analyst' in titre:
        return 'data analyst'
    elif 'machine learning' in titre:
        return 'machine learning engineer'
    elif 'business intelligence' in titre:
        return 'data analyst'
    elif  'artificial intelligence' in titre:
        return 'artificial intelligence'
    else:
        return 'autres'


# création de la fonction classer_poste pour regrouper les intitulés de poste en familles de métiers

def classer_niveau(titre):
    titre = titre.lower()
    if 'senior' in titre or 'sr.' in titre:
        return 'senior'
    elif 'junior' in titre or 'jr.' in titre:
        return 'junior'
    elif 'lead' in titre:
        return 'lead'
    elif 'principal' in titre:
        return 'principal'
    else:
        return 'standard'

# on applique la fonction classer_poste à la colonne "Job Title" pour créer une nouvelle colonne "poste_famille"
data["poste_famille"] = data["Job Title"].apply(classer_poste)

print("\nVérification de la nouvelle colonne 'poste_famille' :")
print(data[["Job Title", "poste_famille"]].head(10))

print(data["poste_famille"].value_counts())

print("\nLes 15 intitulés de poste les plus fréquents pour la catégorie 'autres' :")
print(data[data["poste_famille"] == "autres"]["Job Title"].value_counts().head(15))

# on applique la fonction classer_niveau à la colonne "Job Title" pour créer une nouvelle colonne "niveau"
data["niveau"] = data["Job Title"].apply(classer_niveau)
print("\nVérification de la nouvelle colonne 'niveau' :")
print(data["niveau"].value_counts())


# ligne de filtrage puis vérification des nouvelles dimensions

print("\nFiltrage des lignes où 'poste_famille' est différent de 'autres' :")
data= data[data["poste_famille"] != "autres"]
print(data.shape)
print(data["poste_famille"].value_counts())

# Suppression de la colonne "Job Title", devenue redondante avec "poste_famille"
print("\nSuppression de la colonne 'Job Title', devenue redondante :")
data = data.drop(columns=['Job Title'])
print(data.shape)

# Vérification 
print(data.shape)
print(data.isnull().sum().sum())

# sauverge et exportation du dataset nettoyé dans un nouveau fichier CSV
data.to_csv("dataset_nettoye.csv", index=False)
