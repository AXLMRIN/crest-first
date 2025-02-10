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
    make_a_bar
)
# Functions


# Settings =====================================================================
filenames = {
    "open_per_revue" : "auteurice.csv",
    "save" : "auteurice.html"
}

middle_gap : float = 30
height_gap : float = 0.05
bin_size : float = 0.05

# TODO Think of a better way to manage the settings
theme = GeneralTheme(**{
    "yaxis" : {"title" : ""}
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
    margin=dict(l=200, r=200),
)

# Create abstract axis =========================================================
theme.xaxis.config["zeroline"] = False
theme.xaxis.config["tickvals"] = [ 
    int(- middle_gap - 50), int(- middle_gap - 25),
    int(  middle_gap + 50), int(  middle_gap + 25)
    ]
theme.xaxis.config["showticklabels"] = False

theme.yaxis.config["showgrid"] = False
theme.yaxis.config["zeroline"] = False
theme.yaxis.config["showticklabels"] = False
theme.yaxis.config["tickvals"] = []

fig.update_layout(
    xaxis = theme.xaxis.config, 
    yaxis = theme.yaxis.config
)

# Create Rectangles ============================================================
idx = np.argsort(df_plot["r_w"])
disc_sorted = np.array(df_plot["discipline"])[idx]


n_disciplines = len(df_plot)
y_tick_value = 0.9 / n_disciplines

grouped = df_plot.groupby("discipline")

for i, discipline in enumerate(disc_sorted):
    discipline_df = grouped.get_group(discipline)
    # Add women rates
    fig.add_trace(
        make_a_bar( - middle_gap, y_tick_value * i + 0.05,
                -1 * discipline_df["r_w"].item(), bin_size,
                name = discipline, fillcolor = "pink",
                line = {"color" : "pink"},
                showlegend = False)
    )
    
    # Add women rates specialised in gender
    fig.add_trace(
        make_a_bar( - middle_gap, y_tick_value * i + 0.05,
                -1 * discipline_df["r_w_g"].item(), bin_size,
                name = discipline, fillcolor = "red",
                line = {"color" : "red"},
                showlegend = False)
    )
    
    # Add men rates
    fig.add_trace(
        make_a_bar( middle_gap, y_tick_value * i + 0.05,
                discipline_df["r_m"].item(), bin_size,
                name = discipline, fillcolor = "blue",
                line = {"color" : "blue"},
                showlegend = False)
    )
    
    # Add women rates specialised in gender
    fig.add_trace(
        make_a_bar( middle_gap, y_tick_value * i + 0.05,
                discipline_df["r_m_g"].item(), bin_size,
                name = discipline, fillcolor = "green",
                line = {"color" : "green"},
                showlegend = False)
    )

    # Add the discipline name 
    fig.add_trace(
        go.Scatter(
            x = [0], y = [y_tick_value * i + 0.05],
            mode="text",
            text=[discipline],
            textposition="middle center",
            textfont=dict(
                family="sans serif",
                size=18
        ),
        showlegend = False
    ))


    
# Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SAVEPATH = "views/"
# NOTE change 'include_plotlyjs' for lighter files
fig.write_html(SAVEPATH + filenames["save"],
               auto_play = False,
               include_plotlyjs = True, include_mathjax = False)

