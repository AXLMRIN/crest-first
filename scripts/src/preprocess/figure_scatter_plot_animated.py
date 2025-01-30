'''
What it does : 
this file is meant to preprocess a data frame for the a scatter plot considering 
3 dimensions : 
    % of article about race
    % of article about genre
    % of article about classe

input : raw dataframe from EOLLION mail from the 2 week of January (mail) 
    name : 2025-01-07-2024-10-29-quinquadef4-neat-abstract-bert.csv

output : 
    dataframe : 
        columns :  
| prop race | prop genre | prop classe | revue | discipline | number_of_article | year
| float      | float       | float        | str   | str        | int               | int

'''
# Third Parties
import pandas as pd
import numpy as np

# Native

# Custom 

# Classes

# Functions

# Settings =====================================================================
filepath : str = "data/"
filename : str = "2025-01-07-2024-10-29-quinquadef4-neat-abstract-bert.csv"

filepath_save : str = "data/preprocessed/"
filename_save : str = "figure_scatter_plot_animated.csv"

# Open Files ===================================================================
# >>> Only keep "bert_genre", "annee", "revue" 
original_df : pd.DataFrame = pd.read_csv(
    filepath + filename
    ).loc[
        :,["annee", "revue", "bert_genre", "tag_race", "bert_classe_large"]
          ].dropna().rename(
              columns = {
                  "bert_genre" : "gender",
                  "tag_race" : "race",
                  "bert_classe_large" : "class"
              }
          )

# >>> Remove the years 2023 
original_df.drop(
    original_df[
        original_df["annee"] == 2023
    ].index, inplace = True)

# Add the "discipline" column - - - - - - - - - - - - - - - - - - - - - - - - - 
# >>> Open and clean discipline_per_revue
discipline_per_revue : pd.DataFrame = pd.read_csv(
    filepath + "2025-01-14-Classification revues - Feuille 1.csv"
    ).loc[:,["revue", "Dominante"]].dropna()
 
discipline_per_revue["Dominante"] = discipline_per_revue["Dominante"].replace(
    "Économie", "Economie")

def what_discipline(revue : str):

    try : 
        to_return : str =  discipline_per_revue.loc[
            discipline_per_revue["revue"] == revue,
            "Dominante"
        ].item()
    except : 
        to_return :str =  "<UNK>"
    return to_return

# >>> Add the column "discipline"
original_df["discipline"] = original_df["revue"].apply(what_discipline)

# >>> Remove the rows where the discipline was not found
print("- " * 50 + "\n",
      "Discipline not found for : \n\n",
      ''.join([
    el + ', ' for el in set(original_df.loc[
                                original_df["discipline"] == "<UNK>",
                                "revue"])]) + '\n',
    "- " * 50 + "\n")

original_df.drop(
    original_df.loc[
        original_df["discipline"] == "<UNK>",:].index,
    axis = 0, inplace = True)


# Evaluate the proportion of article mentionning race, class or gender
# per revue---------------------------------------------------------------------
grouped = original_df.groupby("revue")
years_set = set(original_df["annee"]) # sorted

new_df = []
for year in years_set : 
    for revue, revue_df in grouped : 
        new_df.append(
            {
                "prop_race" : revue_df.loc[
                    revue_df["annee"] == year, "race"].mean(),
                "prop_gender" : revue_df.loc[
                    revue_df["annee"] == year, "gender"].mean(),
                "prop_class" : revue_df.loc[
                    revue_df["annee"] == year, "class"].mean(),
                "revue" : revue,
                "discipline" : what_discipline(revue),
                "number_of_article" : len(revue_df.loc[
                    revue_df["annee"] == year, :]),
                "annee" : year
            }
        )

# Save the df ------------------------------------------------------------------

pd.DataFrame(new_df).to_csv(
    filepath_save + filename_save, index = False)