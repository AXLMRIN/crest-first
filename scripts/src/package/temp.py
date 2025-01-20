# Third Parties
import pandas as pd
import plotly.graph_objs as go

# Native

# Custom 


# Classes
from plotly.graph_objs._figure import Figure as goFigure

# Functions


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