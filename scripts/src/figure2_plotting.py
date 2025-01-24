# Third Parties
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np 

# Native
import json

# Custom 

# Classes
from plotly.graph_objects import Figure as goFigure

# Functions
from package import load_JSON_parameters, add_trace
# Parameters ===================================================================
# Data display - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
x_column = "annee"
y_column = "pourcentage"
group_by_column : str = "group_by"

# Ticks and axis - Local changes - - - - - - - - - - - - - - - - - - - - - - - -
x_axis_ticks : dict = {
    "tickvals" : [2004,2008,2012,2016,2020,2024]   
}
y_axis_ticks : dict = {
    "autorange" : False,
    "tickvals" : [0,10,20,30],
    "range" : [-1e-3, 31]
}
# Files to open - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
filename_open       : str = "figure_2_preprocessed.csv"
filename_save       : str = "figure_2.html"
json_filenames : dict = {
    "xaxis" : "xaxis.json",
    "yaxis" : "yaxis.json",
    "legend": "legend.json",
    "hover" : "hover.json",
    "traces_args" : "figure2_traces.json",
    "other" : "other_figure2.json",
}

# Open files ====================================================================
# The file is already preprocessed

# NOTE Because I run the file from the terminal the path is not '../../data ...'
FOLDERNAME = "data/checkpoints/"
df : pd.DataFrame = pd.read_csv(FOLDERNAME + filename_open)

# Loading the parameters - - - - - - - - - - - - - - - - - - - - - - - - - - - -
parameters = load_JSON_parameters(json_filenames)

# Creating the plot ============================================================
fig : goFigure = go.Figure()

# Axis Customisation 
fig.update_layout({
    "xaxis" : {
        **parameters["xaxis"],  # theme
        **x_axis_ticks          # local changes
        },
    "yaxis" : {
        **parameters["yaxis"],  #theme
        **y_axis_ticks          # local changes
    }
})  


# Legend Customisation
fig.update_layout({
    "legend" : parameters["legend"]
})

# Hover Customisation
fig.update_layout(
    parameters["hover"]
)

# Other parameters configuration
fig.update_layout(
    parameters["other"]
)

# Add the traces ===============================================================
grouped_df = df.groupby(group_by_column)

for name, sub_dataframe in grouped_df : 
    add_trace(fig, name, sub_dataframe,
              x_column = x_column, y_column = y_column,
              parameters = parameters["traces_args"])

# customise all the traces
fig.update_traces(parameters["traces_args"]["ALL"])

# Saving the plot ==============================================================
SAVINGFOLDER = "views/"
fig.write_html(SAVINGFOLDER + filename_save)
