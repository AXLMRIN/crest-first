# Third Parties
import plotly.graph_objects as go
import pandas as pd

# Native
# NOTE might be worth finding a cleaner way to do that
import sys
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts/src"))
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts"))

# Custom 

# Classes

# Functions
from package.heatmap import (
    make_xyz,
    add_heatmap,
    add_menu,
    sort_revue_and_matrix
)

from plotlyThemes.general_theme import GeneralTheme

# Settings =====================================================================
filenames = {
    "open_per_revue" : "figure_1_per_revue.csv",
    "open_per_discipline" : "figure_1_per_discipline.csv",
    "save" : "heatmap.html"
}
# TODO Think of a better way to manage the settings 
theme = GeneralTheme(**{
    "xaxis" : {"grid_opacity" : 0.3},
    "yaxis" : {"grid_opacity" : 0.3}
})

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

# Create the figure =============================================================
fig = go.Figure(
    layout = {
        'xaxis':  {'anchor': 'x' , 'domain': [0.0, 1.0  ]},
        'yaxis':  {'anchor': 'y' , 'domain': [0.0, 0.25 ]},
        'yaxis2': {'anchor': 'y2', 'domain': [0.7, 1.0  ]},
    }
)

# Customise figure general parameters - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(
    paper_bgcolor = theme.primary_color,
    plot_bgcolor = theme.primary_color, 
    height = 800, width = 1200,
    margin=dict(l=200, r=200),
)

# Customise axis - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(
    xaxis = theme.xaxis.config,
    yaxis = theme.yaxis.config,
    yaxis2 = theme.yaxis.config
)

# customise the legend - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
theme.legend.config["x"] =  0.5
theme.legend.config["y"] = -0.1
fig.update_layout(
    legend = theme.legend.config
)

# Create the heatmaps - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
trace_bind = {}
for discipline, sub_df in df_plot_per_revue.groupby("discipline") : 
    annee_vec, revue_vec, proportion_matrix = make_xyz(sub_df)
    revue_vec, proportion_matrix = sort_revue_and_matrix(revue_vec, proportion_matrix)
    add_heatmap(fig, annees = annee_vec, revue_names = revue_vec, 
                proportions = proportion_matrix, discipline = discipline)
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
# BUG The grid color changes for god know why CF data_plotter.add_menu

# Set one facet active - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig.data[trace_bind["Anthropologie_heatmap"]].visible = True
fig.data[trace_bind["Anthropologie_trace"]].visible = True
# Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SAVEPATH = "views/"
# NOTE change 'include_plotlyjs' for lighter files
fig.write_html(SAVEPATH + filenames["save"],
               include_plotlyjs = True, include_mathjax = False)

