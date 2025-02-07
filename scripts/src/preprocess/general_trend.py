'''
The point is to add the text column to the per_discipline
'''
# Third Parties
import pandas as pd
import numpy as np

# Native

# Custom 

# Classes

# Functions

# Settings =====================================================================
filepath : str = "data/preprocessed/"
filename : str = "prop_per_discipline.csv"


filepath_save : str = "data/preprocessed/"
filename_save : str = "general_trend.csv"

# Open Files ===================================================================
df = pd.read_csv(filepath + filename)

# Add the text - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
DISCIPLINE_SET = sorted(list(set(df["discipline"])))

def b_start(discipline1, discipline2) : 
    if discipline1 == discipline2: return "<b>"
    return ''

def b_end(discipline1, discipline2) : 
    if discipline1 == discipline2: return "</b>"
    return ''

def create_text(localisation,df : pd.DataFrame) : 
    '''
    data : 
        - annee
        - discipline
        - RA
    '''
    sub_df = df.groupby(["RA", "annee", "discipline"])

    text_out = f'{localisation["annee"]} :<br>'
    for discipline in DISCIPLINE_SET : 
        text_out += b_start(discipline, localisation["discipline"])
        text_out += (f'{discipline} :'
                     f'{sub_df.get_group(
                         (localisation["RA"], localisation["annee"], discipline)
                        )["proportion"].item():.2f} %')
        text_out += b_end(discipline, localisation["discipline"])
        text_out += "<br>"
    return text_out
    

df["text"] = [create_text(df.loc[i, ["annee", "RA", "discipline"]], df) 
             for i in range(len(df))]
# Save to csv - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
df.to_csv(
    filepath_save + filename_save,
    index = False
)

