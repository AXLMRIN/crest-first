# Third Parties
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np 

# Native

# Custom 

# Classes
from plotly.graph_objects import Figure as goFigure
# Functions

# Parameters ===================================================================
filename_open : str = 'figure_2_preprocessed.csv'
filename_save : str = 'figure_2.html'
# Open files ====================================================================
# The file is already preprocessed
FOLDERNAME : str = 'data/checkpoints/'
# NOTE Because I run the file from the terminal the path is not '../../data ...'
df : pd.DataFrame = pd.read_csv(FOLDERNAME + filename_open)

# Creating the plot ============================================================
fig : goFigure = px.line(
    df, x = 'annee', y = 'pourcentage',
    color = 'colour_style', line_dash= 'line_dash_style',
    labels = {
        'colour_style' : "Groupe de revues",
        'line_dash_style' : 'Definition du genre'
    }
)



# Saving the plot ==============================================================
SAVINGFOLDER = 'views/'
fig.write_html(SAVINGFOLDER + filename_save)
