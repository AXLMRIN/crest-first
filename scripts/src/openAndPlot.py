# ------------------------------------------------------------------------------
# Third parties
import pandas as pd
import plotly.express as px

# Native 
import json

# Custom
from .constants import DATADIRPATH

# Objects and classes
from plotly.graph_objs._figure import Figure as pxFigure

# Functions and methods
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------

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

def cleanMetadata(metadata : dict) -> tuple[str,str,dict]:
    '''
    this function is meant to take out the 'xlabel' and 'ylabel' off of metadata
    and return the labels and the metadata.
    '''
    xlabel, ylabel = metadata['xlabel'], metadata['ylabel']
    metadataOUT = {
        key : metadata[key] for key in metadata \
                if key not in ['xlabel','ylabel']
    }
    return xlabel, ylabel, metadataOUT

def openFilesCSVJSON(filename : str) -> tuple[pd.DataFrame, dict]:
    '''
    this function is meant to open the given file with respect to the fileformat
    '''
    filename = filename_format(filename)
    # Open the files
    dfToPlot =  pd.read_csv(DATADIRPATH + filename + '.csv' )
    metadata = loadJSONFILE(DATADIRPATH + filename + '.json')
    return dfToPlot, metadata

def loadJSONFILE(filename : str) -> dict:
    """
    Extract data from a .json file
    """
    with open(filename, 'r') as file:
        out : dict = json.load(file)
    return out
    

def open_and_plot(filename : str, 
                  axis_theme : dict = {
                      'xaxis' : 'xaxis.json',
                      'yaxis' : 'yaxis.json'
                      }) -> pxFigure:
    """
    this function is meant to open the csv file created with the 
    save_data_frame_for_plotting function as well as the json file and plot 
    the whole thing.
    
    # No customization in this function, pure plotting and apply theme.

    FYI :
        - The filename can be either 'xxxx' or 'xxxx.csv' of 'xxxx.json'
    """
    # Open data
    dfToPlot, metadata = openFilesCSVJSON(filename)

    # Create the figure
    xlabel, ylabel, metadata = cleanMetadata(metadata)

    fig = px.line(dfToPlot, x = xlabel, y = ylabel,
                **metadata
                )
    
    # TODO Make apply theme function
    # Load themes : 
    # FIXME no axis is showing up
    axis_themes_loaded = {
        axisName : loadJSONFILE(axis_theme[axisName]) for axisName in axis_theme
    }
    fig = fig.update_layout(
        axis_themes_loaded
    )

    return fig
    
def string_to_coordinates(chain : str) -> tuple[int,int]:
    '''
    Receive a string of the format 'x_y' and returns a tuple (x,y)
    '''
    x,y = [int(coordinate) for coordinate in chain.split("_")]
    return x,y

def s2c(chain : str) -> tuple[int, int]:
    '''
    Alias of string_to_coordinates
    '''
    return string_to_coordinates(chain)

def coordinates_to_string(x : int, y : int) -> str:
    '''
    Receive a a tuple (x,y) and returns string of the format 'x_y'  
    '''
    return f'{x}_{y}'

def c2s(x : int, y : int) -> str:
    '''
    Alias of coordinates_to_string
    '''
    return coordinates_to_string(x, y)

def add_figure_to_wrapper(wrapper_fig   : pxFigure,
                         figure_to_add : pxFigure,
                         coordinates  : tuple[int, int]) -> pxFigure : 
    '''
    Takes in a wrapper figure (plotly.subplots.make_subplot) and a plotly figure
    (data, layout, frames) and append the data to the wrapper at the given 
    coordinates
    # TODO what about layout and frames ? 
    '''

    for data in figure_to_add.data:
        wrapper_fig = wrapper_fig.add_trace(
            data,row = coordinates[0], col = coordinates[1]
        )
    
    return wrapper_fig

def merge_plots(dict_of_plots : dict) -> pxFigure : 
    '''
    Receives a dictionnary of figs (pxFigure) as values and coordinates ('x_y') 
    as keys then organise the 2 figs inside 1 bigger figure.
    No customization (for now)
    # FIXME can't have a weird tiling for now |:
    '''

    coordinates = [s2c(chain) for chain in dict_of_plots.keys()]
    n_rows = max([c[0] for c in coordinates])
    n_cols = max([c[1] for c in coordinates])
    # Create the wrapper fig
    wrapper_fig = make_subplots(rows = n_rows, cols = n_cols)

    for coordinate in dict_of_plots:
        wrapper_fig = add_figure_to_wrapper(
                        wrapper_fig,
                        dict_of_plots[coordinate],
                        s2c(coordinate)
                        )
        
    return wrapper_fig


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