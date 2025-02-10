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
filename_save : str = "auteurice.csv"

# Open Files ===================================================================
# >>> Only keep "bert_genre", "annee", "revue" 
original_df : pd.DataFrame = pd.read_csv(
    filepath + filename
    ).loc[:,["bert_genre", "femme", "annee", "revue"]].dropna()

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
    el + '; ' for el in set(original_df.loc[
                                original_df["discipline"] == "<UNK>",
                                "revue"])]) + '\n',
    "- " * 50 + "\n")

original_df.drop(
    original_df.loc[
        original_df["discipline"] == "<UNK>",:].index,
    axis = 0, inplace = True)

# Evaluate the number of women - - - - - - - - - - - - - - - - - - - - - - - - -
new_df = []
for discipline, sub_df in original_df.groupby("discipline"):
    r_women = 100 * sub_df["femme"].mean()
    r_homme = 100 - r_women
    r_women_genre = 100 * (sub_df["femme"] * sub_df["bert_genre"]).mean()
    r_homme_genre = 100 * ((1 - sub_df["femme"]) * sub_df["bert_genre"]).mean()
    new_df.append({"discipline" : discipline,
        "r_w" : r_women, "r_m" : r_homme,
        "r_w_g" : r_women_genre, "r_m_g" : r_homme_genre
    })

# Save to csv - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
pd.DataFrame(new_df).to_csv(
    filepath_save + filename_save,
    index = False
)


 