# Third Parties
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
from plotlyThemes.general_theme import GeneralTheme
from package.auteurice import(
    make_a_bar,
    title_on_the_side,
    yScale,
    customHistogram
)
# Functions


# Settings =====================================================================
filenames = {
    "open_per_revue" : "auteurice.csv",
    "save" : "auteurice.html"
}

custom_hist = customHistogram()

theme = GeneralTheme(**{
    "xaxis" : {"title" : "", "grid_opacity" : 0.7},
    "yaxis" : {"title" : ""},
    "legend" : {"position" : (0.5, 1.05)}
})

# Open Files ===================================================================
selected_columns = ["discipline", "r_w", "r_m", "r_w_g", "r_m_g"]

OPENPATH  = "data/preprocessed/"
df_plot = pd.read_csv(OPENPATH + filenames["open_per_revue"])
df_plot = df_plot.loc[:, selected_columns]
df_plot.index = range(len(df_plot))

# Create the figure =============================================================
fig = go.Figure()

# Customise figure general parameters - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(
    paper_bgcolor = theme.primary_color,
    plot_bgcolor = theme.primary_color, 
    height = 800, width = 1200,
    margin=dict(l=20, r=20),
)

# Create abstract axis =========================================================
theme.xaxis.config["showline"] = False
theme.xaxis.config["range"] = [-125, 125]
theme.xaxis.config["zeroline"] = False
theme.xaxis.config["showticklabels"] = False

theme.yaxis.config["showgrid"] = False
theme.yaxis.config["zeroline"] = False
theme.yaxis.config["showticklabels"] = False
theme.yaxis.config["tickvals"] = []

theme.legend.config["itemclick"] = False
theme.legend.config["itemdoubleclick"] = False
# theme.legend.config["groupclick"] = False


fig.update_layout(
    xaxis = theme.xaxis.config, 
    yaxis = theme.yaxis.config,
    legend = theme.legend.config
)

custom_hist.set_axis_labels(fig, theme.xaxis.config["range"])
# Add anotation on the left and right for men and women - - - - - - - - - - - - 
title_on_the_side(fig, "Femme (présumé)", x = 0, orientation =-90)
title_on_the_side(fig, "Homme (présumé)", x = 1, orientation = 90)

# Create Rectangles ============================================================
idx = np.argsort(df_plot["r_w"])
discipline_list = np.array(df_plot["discipline"])

y_scale = yScale(factor = 1 / len(df_plot),
                 offset = 0.05, 
                 order  = {
                     discipline : i
                     for i,discipline in enumerate(discipline_list[idx])
                 })

for discipline, discipline_df in df_plot.groupby("discipline") : 
    custom_hist.display_for_a_category(fig, y_scale, discipline, discipline_df)

# Add a custom legend
custom_hist.add_custom_legend(fig)


# Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SAVEPATH = "views/"
# NOTE change 'include_plotlyjs' for lighter files
fig.write_html(SAVEPATH + filenames["save"],
               auto_play = False,
               include_plotlyjs = True, include_mathjax = False)