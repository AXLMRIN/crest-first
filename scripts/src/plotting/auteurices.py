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
theme = GeneralTheme(**{
    "xaxis" : {"title" : "Proportion des articles mentionnant la classe"},
    "yaxis" : {"title" : "Proportion des articles mentionnant le genre"}
})

# Open Files ===================================================================
selected_columns = ["revue", "discipline", "annee","proportion_genre",
                    "proportion_classe", "n_articles", "text"]

OPENPATH  = "data/preprocessed/"
df_plot = pd.read_csv(OPENPATH + filenames["open_per_revue"])
df_plot = df_plot.loc[df_plot["RA"] == True, selected_columns]
df_plot.index = range(len(df_plot))

# Create the figure =============================================================
fig = go.Figure()

# Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SAVEPATH = "views/"
# NOTE change 'include_plotlyjs' for lighter files
fig.write_html(SAVEPATH + filenames["save"],
               auto_play = False,
               include_plotlyjs = True, include_mathjax = False)

