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
    add_heatmap
)

# Settings =====================================================================
filenames = {
    "open" : "figure_1_per_revue.csv",
    "save" : "heatmap.html"
}

jsonfiles = {}

# Open files ====================================================================
OPENPATH  = "data/preprocessed/"
df_plot = pd.read_csv(OPENPATH + filenames["open"])
df_plot = df_plot.loc[
    df_plot["RA"] == False, ["annee","revue","discipline","proportion"]
]
df_plot.index = range(len(df_plot))

# Create the figure =============================================================
fig = go.Figure(
    layout = {
        'xaxis':  {'anchor': 'y', 'domain': [0.0, 1.0]},
        'yaxis':  {'anchor': 'x', 'domain': [0, 1.0]}
    }
)
# 'xaxis2': {'anchor': 'y2', 'domain': [0.0, 1.0]},
# 'yaxis2': {'anchor': 'x2', 'domain': [0.0, 0.425]}

# Create the heatmap - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# TODO Create for all disciplines
year_array = list(set(df_plot["annee"]))
grouped = df_plot.groupby("discipline")
sub_df = grouped.get_group("Sociologie")
revue_array = sorted(list(set(sub_df["revue"])), reverse = True)

z = [
    sub_df.loc[sub_df["revue"] == revue,"proportion"].to_list()
    for revue in revue_array
]
# --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --

colorscale=[
        [0, "rgb(255,255,255)"],
        [0.5, "rgb(255,0,0)"],
        [1.0, "rgb(0,0,0)"],
    ]
colorbar={
    "tickvals" : [0,50,100,1500],
    "ticksuffix" : " %"
}

fig.add_trace(
    go.Heatmap(x = year_array, y = revue_array, z = z,
               zmid = 50, colorbar = colorbar, colorscale = colorscale,
               visible = True)
)

print(fig.data[0])

# Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SAVEPATH = "views/"
# NOTE change 'include_plotlyjs' for lighter files
fig.write_html(SAVEPATH + filenames["save"],
               include_plotlyjs = True, include_mathjax = False)