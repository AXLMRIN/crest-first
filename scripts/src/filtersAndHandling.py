# ------------------------------------------------------------------------------
# Third parties
import pandas   as pd
import numpy    as np

# Native
import json

# Custom
from .constants import DATADIRPATH, SAVEPATH

# Object and classes
from datetime import date

# Functions and methods


# ------------------------------------------------------------------------------

def filter( df : pd.DataFrame, label : str, value,
           returnBool : bool = False             ) -> pd.DataFrame | np.ndarray:
    # VERIFIED
    """
        Takes in a dataframe, a label and the accepted values. 
        
        Warning : the type of the df[label] and value must match

        returns
            - if returnBool = False : the dataframe filtered -> pd.DataFrame
            - if returnBool = True  : the boolean array to filter the dataframe 
                                      manually
    """

    # we are using the logical operator _in_, thus we make the value a list of 
    # values if it wasn't
    if not isinstance(value, list) :
         value = [value]
    
    # Create a boolean array used to filter
    boolArray : np.ndarray = np.array(
        [item in value for item in df[label]],
        dtype = bool)
    
    if returnBool : return boolArray

    return df[boolArray]

def getPerYear(df : pd.DataFrame, label : str = "bert_genre", func = np.mean, 
               filters : list[dict] = []) -> tuple[list, list]:
    # VERIFIED
    """
        takes a dataframe (non filtered) and read the table given the column 
        label (label). it applies the 
        function func (usually np.means).
        It is possible to apply a filter thanks to the function filter.
        the _filters_ parameter is a list of dictionnaries {label, value} to
        apply to the dataframe

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


# NOTVERIFIED

PLOTLYARGS = ['color', 'line_dash', 'symbol', 'hover_name', 'hover_data',
              'facet_row', 'facet_col', 'error_x', 'error_y', 'error_x_minus',
              'error_y_minus', 'animation_frame', 'animation_group']

def xlabel_check(df : pd.DataFrame, xlabel : str) -> bool:
    if xlabel not in df.columns : 
        raise KeyError(f'{xlabel} is not a column in the dataframe')
    
    return True

def ylabel_check(df : pd.DataFrame, ylabel : str, xlabel : str) -> bool:
    if (ylabel not in df.columns):
        raise KeyError(f'{ylabel} is not a column in the dataframe.')
    if (ylabel == xlabel):
        raise ValueError(f'The xlabel and ylabel are the same ({xlabel}).')
    return True

def key_check(key : str, xlabel : str, ylabel : str) -> bool:
    # NOTE : PLOTLYARGS is expected to be defined elsewhere
    # NOTE Might be unnecessary 
    return (key in PLOTLYARGS)&(key != xlabel)&(key != ylabel)

def key_saving(
        df : pd.DataFrame,  metadata : dict,
        key : str, value ) -> tuple[pd.DataFrame, dict] : 
    """
        this function is meant to deal with 2 types of values (arraylike objects
        or strings) and save it in the metadata and the dataframe (if need be).
            -> arraylike :  adds it to the data frame, the object must be the
                            same length of the dataframe and adds it to the
                            metadata dict
            -> string    : adds it to the metadata dict
    """
    if isinstance(value,str):             # is a column name
        # Only adds information to the metadata file
        try:
            assert(value in df.columns)   # is a column of the dataframe
            metadata[key] = value
        except:
            print((f'WARNING : The kwargs[{key}] = {value} is not a column of '
                    'the data frame. Ignored.'))

    else :
        # Assume this is a column. #UPGRADE deal with other types of value
        # Add the data to the dataframe and save the information in the metadata
        # file

        # Verify the length of the serie
        try :
            assert(len(value) == len(df)) # make sure the length is correct
        except :
            print((f'WARNING : kwargs[{key}] is not of length {len(df)} '
                   f'({len(value)}). Ignored.'))
            pass
        
        # try to add it in the dataframe
        try :
            df.loc[:,key] = pd.DataFrame({
                                'temp' : value
                                }).set_index(df.index).loc[:,'temp']
            metadata[key] = key
        except:
            print((f'WARNING : kwargs[{key}] could not be added to the '
                    'dataframe. Ignored'))
            pass
    
    # NOTE .copy() might be unnecessary
    return df.copy(), metadata

def create_filename(**kwargs):
    if 'filename' in kwargs : filename = kwargs['filename']
    else :                   filename = 'someDataFrame'

    filename = filename_format(filename)

    # Add the date
    dateSTR : str = str(date.today())
    filename = dateSTR + "-" + filename
    
    return filename

def filename_format(filename : str) -> str:
    """
    this function is to make sure the filename has the right format.
    given 'xxxx' or 'xxxx.csv' of 'xxxx.json' it returns the 'xxxx' (root with 
    no extension)
    IT SPECIFICALLY DEALS WITH FILENAMES WITH .csv AND .json, NOT WITH ANY
    EXTENSION
    """
    csvExtension    : bool = filename.endswith('.csv')
    jsonExtension   : bool = filename.endswith('.json')

    if csvExtension  : return filename[:-4] # Remove '.csv'
    if jsonExtension : return filename[:-5] # Remove '.json'
    
    # assume it had the right format
    return filename

def save_data_frame_for_plotting(df, xlabel : str, ylabel : str,
                             **kwargs) -> None:
    """
    This function is meant to be the bridge between the filtered dataframe and 
    the actual plotting.
    In order to be as free as possible, the function will take kwargs to match
    the plotly arguments (defined elsewhere : PLOTLYARGS)
    # UPGRADE the list of accepted arguments
    """

    #NOTE tryout | seems to be working  
    df = df.copy()

    # Prepare metadata ouput --------------------------------------------------- 
    #   the metadata dictionnary will hold the parameters and the columns to 
    #   refer to 
    metadata : dict[str:str] = {}
    if xlabel_check(df, xlabel) :
        metadata['xlabel'] = xlabel
    
    if ylabel_check(df, ylabel, xlabel):
        metadata['ylabel'] = ylabel

    # loop through kwargs and find to find the plotly arguments : 
    for key in kwargs : 
        if  key_check(key, xlabel, ylabel) :
            # kwargs[key] is either a column name or a vector, the size of the 
            # plot that will be added to the dataframe
            df, metadata = key_saving(df, metadata,
                                      key = key, value = kwargs[key])
            
    # Saving zone --------------------------------------------------------------
    #UPGRADE for now the files are overwritten, think of a way to move the
    #        document we are about to delete somewhere else

    filename = create_filename(**kwargs)
    
    # save csv document
    df.to_csv(SAVEPATH + filename + ".csv")

    # save metadata in json
    with open(SAVEPATH + filename + ".json", "w") as outfile:
        json.dump(metadata, outfile)
    print(f'File ({filename}) saved here : {DATADIRPATH}')

    #TODELETE 
    print(metadata)
    
