# Third Parties
import pandas as pd
import numpy as np

# Native

# Custom 

# Classes

# Functions


# Export functions =============================================================

def sort_revue_and_matrix(revue_array : list[str], 
                          proportion_matrix : list[list[float]]
                          ) -> tuple[list[str], list[list[float]]]: 
    
    return revue_array, proportion_matrix

def make_xyz(df : pd.DataFrame) -> tuple[list, list, list] : 
    """Takes a dataframe and 3 columns. Makes it into a 2d array
    Both axis must be sorted
    """
    year_array = list(set(df["annee"]))
    revue_array = sorted(list(set(df["revue"])), reverse = True)

    z = [
        df.loc[df["revue"] == revue,"proportion"].to_list()
        for revue in revue_array
    ]
    
    return year_array, revue_array, z