'''
output : 
    dataframe : 
        columns :  
            RA : bool
            revue : str
            discipline : str
            annee : int
            proportion : float
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
filename : str = "2025-01-21-quinquadef5-abstracts.csv"

RA_window_size : int = 3

filepath_save : str = "data/preprocessed/"
filename_save : str = "prop_per_discipline.csv"

# Open Files ===================================================================
# >>> Only keep "bert_genre", "annee", "revue" 
original_df : pd.DataFrame = pd.read_csv(
    filepath + filename
    ).loc[:,["annee", "revue", "bert_genre", "bert_genre_stat"]].dropna()

# >>> Remove the years 2023 
original_df.drop(
    original_df[
        original_df["annee"] == 2023
    ].index, inplace = True)

# Add the "discipline" column - - - - - - - - - - - - - - - - - - - - - - - - - 
# NOTE Fixing the names to match the revue csv. 

original_df["revue"] = original_df["revue"].replace({
    "Géographie, économie, société" : "Géographie, économie et société",
    "L’Espace géographique" : "L'espace géographique",
    "Économie rurale" : "Economie rurale",
    "Natures Sciences Sociétés" : "Nature science et sociétés"

})

# >>> Open and clean discipline_per_revue
discipline_per_revue : pd.DataFrame = pd.read_csv(
    filepath + "2025-01-14-Classification revues - Feuille 1.csv"
    ).loc[:,["revue", "Dominante"]].dropna()
 
discipline_per_revue["Dominante"] = discipline_per_revue["Dominante"].replace(
    "Economie", "Économie")

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
    el + '; ' for el in set(original_df.loc[
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

def eval_restr(df, year):
    return 100 * ( df.loc[
        df["annee"] == year, "bert_genre"
    ].mean() - df.loc[
        df["annee"] == year, "bert_genre_stat"
    ].mean() ) 

def eval_ext(df, year):
    return 100 * df.loc[
        df["annee"] == year, "bert_genre"
    ].mean()

# >>> Evalutation 'restrainte'
for discipline, discipline_df in grouped_df : 
    for year in year_set:
        new_df.append({
            "RA" : False,
            "annee" : year,
            "discipline" : discipline,
            "proportion" : eval_restr(discipline_df, year),
            "definition" : "restr"
        })

# >>> Evalutation 'extensive'
for discipline, discipline_df in grouped_df : 
    for year in year_set:
        new_df.append({
            "RA" : False,
            "annee" : year,
            "discipline" : discipline,
            "proportion" : eval_ext(discipline_df, year),
            "definition" : "ext"
        })

    

# Estimate the average of all categories
for year in year_set:
    new_df.append({
        "RA" : False,
        "annee" : year,
        "discipline" : "Toutes",
        "proportion" : eval_restr(original_df, year),
        "definition" : "restr"
    })

for year in year_set:
    new_df.append({
        "RA" : False,
        "annee" : year,
        "discipline" : "Toutes",
        "proportion" : eval_ext(original_df, year),
        "definition" : "ext"
    })

# Proceed to the Rolling Average - - - - - - - - - - - - - - - - - - - - - - - -
# >>> Define a new pandas.Dataframe to evaluate the rolling average
new_df_grouped = pd.DataFrame(new_df).groupby("definition")

window : np.ndarray = np.ones(RA_window_size) / RA_window_size

years : list = list(year_set)
years_RA : list = years[RA_window_size // 2 :
                         len(years) - (RA_window_size - RA_window_size // 2)]

for definition, definition_df in new_df_grouped : 
    for discipline, discipline_df in definition_df.groupby("discipline") :
        proportion_RA : np.ndarray = np.convolve(
            discipline_df["proportion"], window,
            mode = "valid")

        for proportion, year in zip(proportion_RA, years_RA): 
            new_df.append({
                "RA" : True, 
                "annee" : year,
                "discipline" : discipline,
                "proportion" : proportion,
                "definition" : definition
            })

# Save to csv - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
pd.DataFrame(new_df).to_csv(
    filepath_save + filename_save,
    index = False
)


