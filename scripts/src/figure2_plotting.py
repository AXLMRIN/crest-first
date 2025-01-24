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
from package import load_JSON_parameters
# Parameters ===================================================================

# Files to open - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
filename_open       : str = "figure_2_preprocessed.csv"
filename_save       : str = "figure_2.html"
json_filenames : dict = {
    "xaxis" : "xaxis.json",
    "yaxis" : "yaxis.json",
    "legend": "legend.json",
    "hover" : "hover.json",
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
# UPGRADE This could be nice to make it better
fig : goFigure = px.line(
    df, x = "annee", y = "pourcentage",
    color = "colour_style", line_dash= "line_dash_style",
    labels = {
        "colour_style" : "Groupe de revues",
        "line_dash_style" : "Definition du genre"
    }
)
# Axis Customisation 
fig.update_layout({
    "xaxis" : parameters["xaxis"],
    "yaxis" : parameters["yaxis"]
})

# Legend Customisation
fig.update_layout({
    "legend" : parameters["legend"]
})

# Hover Customisation
fig.update_layout(
    parameters["hover"]
)

# FIXME Add hovertemplate

# Other parameters configuration
fig.update_layout(
    parameters["other"]
)

# Add the traces ===============================================================


# Saving the plot ==============================================================
SAVINGFOLDER = "views/"
fig.write_html(SAVINGFOLDER + filename_save)
