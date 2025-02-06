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
from plotlyThemes.general_theme import GeneralTheme
from package.scatter_plot import(
    create_data,
    create_frame,
    create_control_buttons
)
# Functions


# Settings =====================================================================
filenames = {
    "open_per_revue" : "prop_genre_classe_per_revue.csv",
    "save" : "scatter_plot.html"
}

# TODO Think of a better way to manage the settings
theme = GeneralTheme(**{})

# Open Files ===================================================================
selected_columns = ["revue", "discipline", "annee","proportion_genre",
                    "proportion_classe", "n_articles", "text"]

OPENPATH  = "data/preprocessed/"
df_plot = pd.read_csv(OPENPATH + filenames["open_per_revue"])
df_plot = df_plot.loc[df_plot["RA"] == True, selected_columns]
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

# Customise axis - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
theme.xaxis.config["range"] = [-5,35]
theme.yaxis.config["range"] = [-5,105]

theme.xaxis.config["showline"] = False

theme.xaxis.config["title"] = {"text" : "Proportion des articles mentionnant la classe"}
theme.yaxis.config["title"] = {"text" : "Proportion des articles mentionnant la genre"}

theme.legend.config["itemsizing"] = "constant"
theme.legend.config["itemwidth"] = 50
theme.legend.config["y"] = 1.1
theme.legend.config["entrywidth"] = 0.20


fig.update_layout(
    xaxis = theme.xaxis.config,
    yaxis = theme.yaxis.config,
    legend = theme.legend.config
)

# Create the dots - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

create_data(fig, 
            df_plot.groupby("annee").get_group(2020),
            theme.traces_color)

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
    }

frames = []
for annee, sub_df in df_plot.groupby("annee"): 
    frames += [
        create_frame(sub_df, annee, theme.traces_color)
    ]
    sliders_dict["steps"].append({
        "args": [
            [annee],
            {
                "frame": {"duration": 300, "redraw": False},
                "mode": "immediate",
                "transition": {"duration": 300}}
        ],
        "label": annee,
        "method": "animate"})
fig.frames = frames
fig.update_layout(sliders = [sliders_dict])
# Add the control buttons - - - - - - - - - - - - - - - - - - - - - - - - - - - 
create_control_buttons(fig)

# Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SAVEPATH = "views/"
# NOTE change 'include_plotlyjs' for lighter files
fig.write_html(SAVEPATH + filenames["save"],
               auto_play = False,
               include_plotlyjs = True, include_mathjax = False)

