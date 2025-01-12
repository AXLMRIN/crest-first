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
                  axis_theme : dict = {'xaxis' : 'xaxis.json', 'yaxis' : 'yaxis.json'}) -> pxFigure:
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
    