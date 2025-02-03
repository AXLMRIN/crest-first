# Third Parties
import pandas as pd
import numpy as np

# Native

# Custom 

# Classes

# Functions


# Export functions =============================================================

def make_xyz(df : pd.DataFrame, x_col : str, y_col : str, z_col : str
             ) -> tuple[np.ndarray, np.ndarray, np.ndarray] : 
    """Takes a dataframe and 3 columns. Makes it into a 2d array
    Both axis must be sorted
    """

    x_set = set(df[x_col])
    y_set = set(df[y_col])
    
    z_output = np.zeros([len(x_set), len(y_set)])
    for i, x in enumerate(x_set) :
        for j,y in enumerate(y_set) : 
            try : 
                item = df.loc[
                    (df[x_col] == x) & (df[y_col] == y),
                    z_col].item()
            except : 
                item = np.nan
            z_output[i,j] = item
    return np.array(x), np.array(y), z_output