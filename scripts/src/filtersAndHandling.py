# -------------------------------
# Every function has been verified
# -------------------------------
import pandas   as pd
import numpy    as np


def filter( df : pd.DataFrame, label : str, value,
           returnBool : bool = False                ) -> pd.DataFrame | np.ndarray:
    # VERIFIED
    """
        Takes in a dataframe, a label and the accepted values. 
        
        Warning : the type of the df[label] and value must match

        returns
            - if returnBool = False : the dataframe filtered -> pd.DataFrame
            - if returnBool = True  : the boolean array to filter the dataframe manually
    """

    # we are using the logical operator _in_, thus we make the value a list of values if it wasn't
    if not isinstance(value, list) :
         value = [value]
    
    # Create a boolean array used to filter
    boolArray : np.ndarray = np.array(
        [item in value for item in df[label]],
        dtype = bool)
    
    if returnBool : return boolArray

    return df[boolArray]

def getPerYear(df : pd.DataFrame, label : str = "bert_genre", func = np.mean, filters : list[dict] = []) -> tuple[list, list]:
    # VERIFIED
    """
        takes a dataframe (non filtered) and read the table given the column label (label). it applies the 
        function func (usually np.means).
        It is possible to apply a filter thanks to the function filter.
        the _filters_ parameter is a list of dictionnaries {label, value} to apply to the dataframe

        returns the data retrieved and the years (dataRetrieved, years)
    """
    
    # Prepare output
    out = []
    years = list(set(df['annee']))  # select the years

    # filter data
    for f in filters:
        df = filter(df, f['label'], f['value'])
    
    # Retrieve data
    for y in years : 
        out.append(
            func(
                filter(df, 'annee',y)[label]
            ))
        
    return out, years
