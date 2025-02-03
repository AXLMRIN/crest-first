'''
What it does : 
this file is meant to preprocess a data frame for the figure 1 : 
graph : 
    x : years
    y : proportion (with or without rolling average)

input : raw dataframe from EOLLION mail from the 2 week of January (mail) 
    name : 2025-01-07-2024-10-29-quinquadef4-neat-abstract-bert.csv

output : 
    dataframe : 
        columns :  
            RA : bool
            revue : str
            discipline : str
            annee : int
            proportion : float

    
!! expected to change !! 
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

RA_window_size : int = 3

filepath_save : str = "data/preprocessed/"
filename_save : str = "figure_1_per_discipline.csv"

# Open Files ===================================================================
# >>> Only keep "bert_genre", "annee", "revue" 
original_df : pd.DataFrame = pd.read_csv(
    filepath + filename
    ).loc[:,["annee", "revue", "bert_genre"]].dropna()

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

# Evaluate the proportion - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# >>> Group the dataframe by revue
grouped_df = original_df.groupby("discipline")

# >>> Evaluate the mean of bert_genre for the given revue and year
# NOTE there might be a cleanier way of doing it 

year_set = set(original_df["annee"]) # is sorted

new_df = []
for discipline, discipline_df in grouped_df : 
    for year in year_set:
        new_df.append({
            "RA" : False,
            "annee" : year,
            "discipline" : discipline,
            "proportion" : discipline_df.loc[
                discipline_df["annee"] == year,
                "bert_genre"].mean() * 100
        })


# Proceed to the Rolling Average - - - - - - - - - - - - - - - - - - - - - - - -
# >>> Define a new pandas.Dataframe to evaluate the rolling average
new_df_grouped = pd.DataFrame(new_df).groupby("discipline")

window : np.ndarray = np.ones(RA_window_size) / RA_window_size

years : list = list(year_set)
years_RA : list = years[RA_window_size // 2 :
                         len(years) - (RA_window_size - RA_window_size // 2)]

for discipline, discipline_df in new_df_grouped :
    proportion_RA : np.ndarray = np.convolve(
        discipline_df["proportion"], window,
        mode = "valid")

    for proportion, year in zip(proportion_RA, years_RA): 
        new_df.append({
            "RA" : True, 
            "annee" : year,
            "discipline" : discipline,
            "proportion" : proportion
        })

# Save to csv - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
pd.DataFrame(new_df).to_csv(
    filepath_save + filename_save,
    index = False
)


