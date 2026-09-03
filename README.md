# ml-prediction-salaire

Projet de Machine Learning visant à prédire le salaire d'un individu à partir de variables telles que l'expérience, le niveau d'étude, le secteur d'activité ou la localisation. Le projet suit un pipeline Data Scientist complet : collecte, nettoyage, EDA, modélisation, évaluation et déploiement.

## Données

- **Source** : annonces Glassdoor scrapées (dataset Kaggle), marché US, salaires en USD.
- **Fichier** : `glassdoor_jobs.csv`

## Structure du projet

- `audit_salaires.py` — audit exploratoire du dataset (dimensions, valeurs manquantes, types, doublons, valeurs aberrantes).
- `glassdoor_jobs.csv` — données brutes.

## Installation

1. Créer et activer l'environnement virtuel :

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Installer les dépendances :

   ```powershell
   pip install pandas numpy matplotlib scikit-learn streamlit
   ```

## Utilisation

```powershell
python audit_salaires.py
```

## État d'avancement : audit exploratoire (EDA)

Étape actuelle du pipeline : audit des données brutes, avant nettoyage.

### Constats

- `isnull().sum()` affiche **0 valeur manquante** sur toutes les colonnes. Ce résultat est trompeur : deux colonnes affichent 0 mais méritent un second regard, car l'absence de `NaN` ne garantit pas l'absence de valeurs manquantes déguisées (encodées par exemple en `-1` plutôt qu'en `NaN`).
- `describe()` sur les colonnes numériques montrait un **minimum à -1**, alors que la boucle de vérification (comparaison `== '-1'` sur chaque colonne) ne l'avait pas détecté.
  - ⚠️ `describe()` **ignore les `NaN`** dans son calcul (count, min, max, mean, etc. ne portent que sur les valeurs non nulles) : un minimum de -1 renvoyé par `describe()` est donc bien une valeur réelle présente dans les données, pas un artefact lié aux `NaN`.
- Vérification ciblée des valeurs négatives sur la colonne `Rating` :
  - `data['Rating'] == -1` → ne détecte rien.
  - `data['Rating'] < 0` → **34 valeurs négatives trouvées !**

> **Note au passage** : `Founded` révèle **97 manquants** qui n'apparaissaient pas dans la boucle texte. Même raison que `Rating` — c'est une colonne numérique.

### Leçon retenue

> L'égalité les ratait, l'infériorité les révèle.

Sur des nombres décimaux (`float`), une comparaison d'**égalité stricte** (`== -1`) est fragile : elle rate toute valeur qui n'est pas *exactement* -1 (ex. -1.0 stocké différemment, arrondis, autres valeurs négatives sentinelles). Une comparaison d'**intervalle** (`< 0`, `<= -1`, etc.) est plus robuste pour détecter des valeurs aberrantes ou des données manquantes déguisées sur des colonnes numériques.

**Bonne pratique** : préférer systématiquement les comparaisons d'intervalle aux égalités strictes lorsqu'on travaille sur des `float`.

> **Note entretien** : « j'ai traité les cas particuliers plutôt que de les jeter » est une meilleure phrase que « j'ai supprimé ce qui posait problème ».

> **Note entretien** : « 24 annonces exprimaient un taux horaire, incompatible avec une cible annuelle. Je les ai écartées plutôt que d'appliquer une conversion reposant sur des hypothèses non vérifiables. »

> **Note entretien** : « Sur des données scrapées, j'ai rencontré quatre formats de salaire différents. J'ai traité chaque cas successivement, en mesurant d'abord son ampleur avant de décider de le corriger ou de l'écarter. »
