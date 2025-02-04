# Third Parties
import plotly.graph_objects as go
import pandas as pd

# Native
# NOTE might be worth finding a cleaner way to do that
import sys
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts/src"))

# Custom 

# Classes

# Functions
from package.heatmap import (
    make_xyz,
    add_heatmap,
    add_menu,
    sort_revue_and_matrix
)
from package.data_loader import (
    load_JSON_parameters
)

# Settings =====================================================================
filenames = {
    "open_per_revue" : "figure_1_per_revue.csv",
    "open_per_discipline" : "figure_1_per_discipline.csv",
    "save" : "heatmap.html"
}
# TODO Think of a better way to manage the settings 
jsonfiles = {
    "general" : "general_theme.json",
    "xaxis" : "xaxis.json",
    "yaxis" : "yaxis.json",
    "legend" : "legend.json"
}

# Open files ====================================================================
OPENPATH  = "data/preprocessed/"
df_plot_per_revue = pd.read_csv(OPENPATH + filenames["open_per_revue"])
df_plot_per_revue = df_plot_per_revue.loc[
    df_plot_per_revue["RA"] == False, ["annee","revue","discipline","proportion"]
]
df_plot_per_revue.index = range(len(df_plot_per_revue))

df_plot_per_discipline = pd.read_csv(OPENPATH + filenames["open_per_discipline"])
df_plot_per_discipline = df_plot_per_discipline.loc[
    df_plot_per_discipline["RA"] == True, ["annee", "discipline", "proportion"]
]
df_plot_per_discipline.index = range(len(df_plot_per_discipline))

parameters = load_JSON_parameters(jsonfiles)

# Create the figure =============================================================
fig = go.Figure(
    layout = {
        'xaxis':  {'anchor': 'x' , 'domain': [0.0, 1.0  ]},
        'yaxis':  {'anchor': 'y' , 'domain': [0.0, 0.25 ]},
        'yaxis2': {'anchor': 'y2', 'domain': [0.3, 1.0  ]},
    }
)


# Customise figure general parameters - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(
    paper_bgcolor = parameters["general"]["theme-colors"]["primary"],
    plot_bgcolor = parameters["general"]["theme-colors"]["primary"], 
    height = 800, width = 1200,
    margin=dict(l=200, r=200),
)

# Customise axis - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(
    xaxis = parameters["xaxis"],
    yaxis = parameters["yaxis"],
    yaxis2 = parameters["yaxis"]
)

# customise the legend - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(
    legend = parameters["legend"]
)
fig.update_layout(
    legend = dict(
        x = 0.5,
        y = -0.1
    )
)

# Create the heatmaps - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
trace_bind = {}
for discipline, sub_df in df_plot_per_revue.groupby("discipline") : 
    annee_vec, revue_vec, proportion_matrix = make_xyz(sub_df)
    revue_vec, proportion_matrix = sort_revue_and_matrix(revue_vec, proportion_matrix)
    add_heatmap(fig, x = annee_vec, y = revue_vec, z = proportion_matrix, discipline = discipline)
    trace_bind[discipline + "_heatmap"] = len(fig.data) - 1


# Create the curves - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
grouped_discipline = df_plot_per_discipline.groupby("discipline")

sub_df = grouped_discipline.get_group("Toutes")
fig.add_trace(
    go.Scatter( x = sub_df["annee"], y = sub_df["proportion"],
                xaxis = "x", yaxis = "y", mode = "lines",
                name = "Moyenne de toutes les disciplines", 
                line = dict(
                   color = "black", dash = "longdash"
                ),
                visible = True)
)
trace_bind["Toutes_trace"] = len(fig.data) - 1

for discipline, sub_df in df_plot_per_discipline.groupby("discipline") :
    if discipline == "Toutes" : continue
    fig.add_trace(
        go.Scatter(x = sub_df["annee"], y = sub_df["proportion"],
                xaxis = "x", yaxis = "y", mode = "lines", 
                name = discipline + ", moyenne des revues",
                line = dict(color = "black" ),
                visible = False)
    )
    trace_bind[discipline + "_trace"] = len(fig.data) - 1



# Display one discipline - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Create the menu - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
discipline_set = sorted(list(set(df_plot_per_revue["discipline"])))
domain_sizes = [0.7, 0.5875, 0.3, 0.925, 0.625, 0.8125, 0.7375, 0.4375, 0.7375, 0.5875, 0.3]

add_menu(fig, trace_bind, discipline_set, domain_sizes)

# Set one facet active - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SAVEPATH = "views/"
# NOTE change 'include_plotlyjs' for lighter files
fig.write_html(SAVEPATH + filenames["save"],
               include_plotlyjs = True, include_mathjax = False)