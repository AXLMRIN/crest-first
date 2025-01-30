# Third Parties
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np 

# Native
# NOTE might be worth finding a cleaner way to do that
import sys
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts/src"))

# Custom 

# Classes

# Functions

# Settings =====================================================================
filepath : str = "data/preprocessed/"
filename : str = "figure_scatter_plot_fige.csv"

filepath_save : str = "views/"
filename_save : str = "figure_scatter_plot_animated.html"

x_axis = "prop_race"
y_axis = "prop_gender"
colour_axis = "discipline"

# Openning file ----=============================================================
df_plot : pd.DataFrame = pd.read_csv(filepath + filename)

# Creating the plot ============================================================
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x = df_plot[x_axis], y = df_plot[y_axis],
        # color = df_plot[colour_axis]
        mode = "markers"
    )
)
# Save figure ===================================================================
fig.write_html(
    filepath_save + filename_save
)