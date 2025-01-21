# Third Parties
import pandas as pd
import plotly.graph_objs as go

# Native

# Custom 


# Classes
from plotly.graph_objs._figure import Figure as goFigure

# Functions
from numpy import where

def add_traces_to_subplot(fig : goFigure, df : pd.DataFrame,
                          x : str, columns : list[str],
                          row : int, col : int, **kwargs) -> None:
    '''takes a dataframe and addit to the figure. 
    the kwargs can contain : 
        {
        # will be applied to the traces one at a time
         'local' : {
                        [kwargs, kwargs, ]
                    }, 
        # will be applied to all the traces
         'global' : kwargs 
        }
    all customisation must be in the kwargs
    '''

    for i, column  in zip( range(len(columns)), columns):
        fig.add_trace(
            go.Scatter(
                x = df[x], y = df[column],
                mode = 'lines'
            ), row = row, col = col
        )
        if 'global' in kwargs:
            fig.data[-1].update(kwargs['global'])
        if 'local' in kwargs: 
            fig.data[-1].update(**kwargs['local'][i])

def extend_index(df : pd.DataFrame, data : pd.DataFrame) -> list:
    '''
    This function is used to add the previous and following number to an index
    if possible
    '''
    idx = list(data.index)      # Get the index
    if idx[0] - 1 in df.index : # add the previous number
        idx = [idx[0] - 1] + idx

    if idx[-1] + 1 in df.index: # add the following number
        idx = idx + [idx[-1] + 1]

    return idx

def add_traces_to_subplot_bi_colours_filling(fig : goFigure, df : pd.DataFrame,
                          x : str, columns : list[str],
                          row : int, col : int, **kwargs) -> None:
    '''
    https://stackoverflow.com/questions/64741015/plotly-how-to-color-the-fill-between-two-lines-based-on-a-condition
    This function does the same as add_traces_to_subplot except that it fills 
    the gap between 2 TRACES by 2 different colours (depending on which one is 
    greater than the other). 
    The kwargs are the same as add_traces_to_subplot, except that if it contains
    any filling argument it will overwrite the filling this function sets.
    The kwargs MUST contain a 'bi-colouring-args' key that refers to a list of 2
    colours.
    '''

    # Assertions - Making sure we have everything we need ----------------------
    # This function is designed to receive only 2 traces
    try:
        assert(len(columns) == 2)
    except:
        raise ValueError((f'2 columns were needed but {len(columns)} were '
                          f'passed on {columns}'))
    
    # This function is designed to receive a kwarg that contains a 
    # 'bi-colouring-args' refering to a list of 2 colours : 
    #   kwargs['bi-colouring-args'] = [COLOUR1, COLOUR2]
    try : 
        assert('bi-colouring-args' in kwargs)
        def fill_colour(label):
            if label == 1 : 
                return kwargs['bi-colouring-args'][0]
            return kwargs['bi-colouring-args'][1]
        
    except:
        raise ValueError("Didn't specify the bi-colouring-args or did it wrong") 
    # --------------------------------------------------------------------------

    # First we need to proceed to few adjustments on the dataframe : 
    # - labelling and grouping
    df = df.loc[:,[x] + columns].copy() # only keeping relevant columns

    df['label'] = where(df[columns[0]] > df[columns[1]], 1, 0)
    df['group'] = df['label'].ne(df['label'].shift()).cumsum()
    # NOTE Explaining this weird line : 
    # the ne(df[].shift) detects changes, meaning 'are we part of the same group
    # or not ?' Then the cumsum creates groups, everytime it changes we create a 
    # new group 

    # create a grouped df so we can trace portions of the trace one at a time
    df_grouped = df.groupby('group')


    for _,data in df_grouped:

        # extending the index to prevent from finding holes in the trace
        idx = extend_index(df,data)

        fig.add_trace(go.Scatter(
            x = df.loc[idx,x], 
            y = df.loc[idx,columns[0]],
            mode = 'lines'
        ), row = row, col = col)

        # Adding customisation kwargs - - - - - - - - - - - - - - - - - - - - - 
        if 'global' in kwargs:
            fig.data[-1].update(kwargs['global'])
        if 'local' in kwargs: 
            fig.data[-1].update(**kwargs['local'][0])
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        fig.add_trace(go.Scatter(
            x = df.loc[idx,x],
            y = df.loc[idx,columns[1]],
            mode = 'lines',
            fill = 'tonexty',
            fillcolor = fill_colour(data['label'].iloc[0])
        ), row = row, col = col)

            # Adding customisation kwargs - - - - - - - - - - - - - - - - - - - - - 
        if 'global' in kwargs:
            fig.data[-1].update(kwargs['global'])
        if 'local' in kwargs: 
            fig.data[-1].update(**kwargs['local'][1])
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


def add_to_dict(dictionnary : dict, key : str , value):
    '''allows the user to add a value to a dictionnary
    The dictionnary is copied so that teh output is independant from
    the input. 
    use '/' in the key to specify sub-dictionnary keys
    '''
    dictionnary = dictionnary.copy()
    keys = key.split('/')
    # TODELETE
    print(keys)
    while len(keys) > 0:
        current_key = keys.pop(0)

        if not current_key in dictionnary :
            raise KeyError(f"{current_key} not in dictionnary")
            return
        