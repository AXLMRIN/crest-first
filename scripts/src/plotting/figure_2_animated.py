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
from plotly.graph_objects import Figure as goFigure

# Functions
from package import (
    load_JSON_parameters, add_trace,
    create_update_menus_buttons, bool_out_of_list
    )

# Parameters ===================================================================
# Data display - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
x_column = {
    "column" : "annee",
    "name" : "Année de publication"
}
y_column = {
    "column" : "proportion",
    "name" : "Part des articles qui convoquent le concept du genre"
}
group_by_column : str = "group_by"

# Ticks and axis - Local changes - - - - - - - - - - - - - - - - - - - - - - - -
x_axis_ticks : dict = {
    "autorange" : False,
    "tickvals" : [2004,2008,2012,2016,2020,2024],
    "range" : [2000,2028]
}
y_axis_ticks : dict = {
    "autorange" : False,
    "tickvals" : [0,10,20,30],
    "range" : [-1e-3, 31]
}
# Files to open - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
filename_open       : str = "figure_2.csv"
filename_save       : str = "figure_2_animated.html"
json_filenames : dict = {
    "xaxis" : "xaxis.json",
    "yaxis" : "yaxis.json",
    "legend": "legend.json",
    "hover" : "hover.json",
    "traces_args" : "figure2/traces.json",
    "menus" : "figure2/menus.json",
    "other" : "figure2/other.json",
}

# Loading the parameters - - - - - - - - - - - - - - - - - - - - - - - - - - - -
parameters = load_JSON_parameters(json_filenames)

# Buttons - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
number_of_traces = len(parameters["traces_args"]) - 1 # contains "ALL"
buttons_dict = {
    "Toutes les courbes" : {
        "visible" : bool_out_of_list(
            [i for i in range(number_of_traces)],
            number_of_traces
            ),
        "other_args" : {}
    },
    "Moyenne de toutes les revues" : {
        "visible" : bool_out_of_list(
            [6,7],
            number_of_traces
            ),
        "other_args" : {}
    }
}

# Open files ====================================================================
# The file is already preprocessed

# NOTE Because I run the file from the terminal the path is not '../../data ...'
FOLDERNAME = "data/preprocessed/"
df : pd.DataFrame = pd.read_csv(FOLDERNAME + filename_open)


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
    },
    "xaxis_title" : x_column["name"],
    "yaxis_title" : y_column["name"]
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

# Add one trace animated =======================================================
grouped = df.groupby("group_by")

color = {
    'Revues TYPE Définition extensive'          : "blue",
    'Revues TYPE Définition statistique'        : "blue",
    'Revues GENERALES Définition statistique'   : "red",
    'Revues GENERALES Définition extensive'     : "red",
    'ARSS Définition extensive'                 : "green", 
    'ARSS Définition statistique'               : "green", 
    'Toutes  Définition extensive'              : "orange", 
    'Toutes  Définition statistique'            : "orange"
    }

fig.update(frames=[
    go.Frame(data = [ 
                    go.Scatter(
                        x = list(discipline_df["annee"].to_numpy()[0:k]),
                        y = list(discipline_df["proportion"].to_numpy()[0:k]),
                        mode = "lines", 
                        line = dict(
                            color = color[discipline],
                            width = 2
                        ))
                for discipline, discipline_df in grouped
                ],
                traces = [1])
            for k in range(len(set(df["annee"])))
    ])

print(fig.frames)

fig.update_layout(
    updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
)

# Saving the plot ==============================================================
SAVINGFOLDER = "views/"
fig.write_html(SAVINGFOLDER + filename_save)
