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

# Parameters ===================================================================

# Files to open - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
filename_open : str = 'figure_2_preprocessed.csv'
filename_save : str = 'figure_2.html'
xaxis_theme_file : str = 'xaxis.json'
yaxis_theme_file : str = 'yaxis.json'
legend_theme_file : str = 'legend.json'
other_theme_file : str = 'other_figure2.json'
# Open files ====================================================================
# The file is already preprocessed
FOLDERNAME : str = 'data/checkpoints/'
# NOTE Because I run the file from the terminal the path is not '../../data ...'
df : pd.DataFrame = pd.read_csv(FOLDERNAME + filename_open)

# Loading the parameters - - - - - - - - - - - - - - - - - - - - - - - - - - - -
PARAMETERSFOLDER : str = 'scripts/plotlyThemes/'
parameters = {}
with open(PARAMETERSFOLDER + xaxis_theme_file) as file :
    parameters['xaxis'] = json.load(file)

with open(PARAMETERSFOLDER + yaxis_theme_file) as file :
    parameters['yaxis'] = json.load(file)

with open(PARAMETERSFOLDER + other_theme_file, 'r') as file:
    parameters['other'] = json.load(file)

with open(PARAMETERSFOLDER + legend_theme_file) as file:
    parameters['legend'] = json.load(file)


# Creating the plot ============================================================
# UPGRADE This could be nice to make it better
fig : goFigure = px.line(
    df, x = 'annee', y = 'pourcentage',
    color = 'colour_style', line_dash= 'line_dash_style',
    labels = {
        'colour_style' : "Groupe de revues",
        'line_dash_style' : 'Definition du genre'
    }
)
# Axis Customisation 
fig.update_layout({
    'xaxis' : parameters['xaxis'],
    'yaxis' : parameters['yaxis']
})

# Legend Customisation
fig.update_layout({
    'legend' : parameters["legend"]
})

# Other parameters configuration
fig.update_layout(
    parameters["other"]
)

# Saving the plot ==============================================================
SAVINGFOLDER = 'views/'
fig.write_html(SAVINGFOLDER + filename_save)
