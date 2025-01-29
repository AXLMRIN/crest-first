# Third Parties
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np 

# Native
# NOTE might be worth finding a cleaner way to do that
import sys
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts/src"))

# Custom 
from package.temp import (
    add_traces_to_subplot, 
    add_traces_to_subplot_bi_colours_filling
)

# Classes
from plotly.graph_objs._figure import Figure as goFigure

# Functions

# Settings =====================================================================
filename_open = "2025-01-07-2024-10-29-quinquadef4-neat-abstract-bert.csv"
filename_save = "figure_2.csv"
# Groups - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
ARSS = [
    'Actes de la recherche en sciences sociales'
]

revues_generales = [
    'Actes de la recherche en sciences sociales',
    "L'Année sociologique",
    'Revue française de sociologie',
    'Sociologie',
    'Sociétés contemporaines',
    'Sociologie du travail'
]

revues_types = [
    'Actes de la recherche en sciences sociales',
    'Revue française de sociologie',
    'Revue française de science politique',
    'Archives de sciences sociales des religions',
    'Ethnologie française',
    'Population',
    'Annales de démographie historique',
    'Revue d\'histoire moderne & contemporaine',
    'Réseaux',
    "Revue française d'économie",
    'Espaces et sociétés'
]

# Open Files ===================================================================
filepath = "data/"
# >>> Only keep "bert_genre", "annee", "revue" 
original_df : pd.DataFrame = pd.read_csv(
    filepath + filename_open
    ).loc[:,["annee", "revue", "bert_genre", "bert_genre_stat"]].dropna()

# >>> Remove the years 2023 
original_df.drop(
    original_df[
        original_df["annee"] == 2023
    ].index, inplace = True)

# >>> create the groups
original_df["ARSS"] = original_df["revue"].apply(
    lambda revue : revue in ARSS)
original_df["TYPE"] = original_df["revue"].apply(
    lambda revue : revue in revues_types)
original_df["GENE"] = original_df["revue"].apply(
    lambda revue : revue in revues_generales)

# Evaluate the proportion - - - - - - - - - - - - - - - - - - - - - - - - - - - 
year_set = set(original_df["annee"]) # is sorted
new_df = []

for year in year_set:
    # Def extensive -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    new_df.append({
        "annee" : year,
        "group_by" : "Toutes  Définition extensive",
        "proportion" : original_df.loc[
            original_df["annee"] == year,
            "bert_genre"].mean() * 100
    })

    new_df.append({
        "annee" : year,
        "group_by" : "ARSS Définition extensive",
        "proportion" : original_df.loc[
            (original_df["annee"] == year) & original_df["ARSS"],
            "bert_genre"].mean() * 100
    })
    new_df.append({
        "annee" : year,
        "group_by" : "Revues GENERALES Définition extensive",
        "proportion" : original_df.loc[
            (original_df["annee"] == year) & original_df["TYPE"],
            "bert_genre"].mean() * 100
    })
    new_df.append({
        "annee" : year,
        "group_by" : "Revues TYPE Définition extensive",
        "proportion" : original_df.loc[
            (original_df["annee"] == year) & original_df["GENE"],
            "bert_genre"].mean() * 100
    })

    # Def statistique -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    new_df.append({
        "annee" : year,
        "group_by" : "Toutes  Définition statistique",
        "proportion" : original_df.loc[
            original_df["annee"] == year,
            "bert_genre_stat"].mean() * 100
    })

    new_df.append({
        "annee" : year,
        "group_by" : "ARSS Définition statistique",
        "proportion" : original_df.loc[
            (original_df["annee"] == year) & original_df["ARSS"],
            "bert_genre_stat"].mean() * 100
    })
    new_df.append({
        "annee" : year,
        "group_by" : "Revues GENERALES Définition statistique",
        "proportion" : original_df.loc[
            (original_df["annee"] == year) & original_df["TYPE"],
            "bert_genre_stat"].mean() * 100
    })
    new_df.append({
        "annee" : year,
        "group_by" : "Revues TYPE Définition statistique",
        "proportion" : original_df.loc[
            (original_df["annee"] == year) & original_df["GENE"],
            "bert_genre_stat"].mean() * 100
    })



# Save File ====================================================================
FOLDERNAME_SAVE = "data/preprocessed/"
pd.DataFrame(new_df).to_csv(
    FOLDERNAME_SAVE + filename_save, index = False
)