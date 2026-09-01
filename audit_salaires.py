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