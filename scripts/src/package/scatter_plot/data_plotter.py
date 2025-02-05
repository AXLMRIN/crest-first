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
from plotlyThemes.general_theme import TracesColours
# Functions

# Settings =====================================================================

def create_data(fig : go.Figure, df : pd.DataFrame,
                traces_color : TracesColours) -> None : 
    fig.update(data = [
            go.Scatter(
                x = discipline_df["proportion_classe"], 
                y = discipline_df["proportion_genre"],
                mode = "markers", name = discipline, 
                marker = {
                    "size" : discipline_df["n_articles"],
                    "color" : traces_color[f'{i}-1'],
                    "sizemin" : 0, "sizemode" : "area", 'sizeref' : 1/2
                    },
                opacity = 0.8, 
                text = df["text"]
            )
            for i, (discipline, discipline_df) in enumerate(
                df.groupby("discipline"))
    ])

def create_frame(df : pd.DataFrame, annee : float, 
                 traces_color : TracesColours) -> go.Frame:
    return go.Frame(data = [
            go.Scatter(
                x = discipline_df["proportion_classe"], 
                y = discipline_df["proportion_genre"],
                mode = "markers", name = discipline, 
                marker = {
                    "size" : discipline_df["n_articles"],
                    "color" : traces_color[f'{i}-1'],
                    "sizemin" : 0, "sizemode" : "area",
                    },
                opacity = 0.8,
                text = df["text"]
            )
            for i, (discipline, discipline_df) in enumerate(
                df.groupby("discipline"))
        ], name = annee
    )



def create_control_buttons(fig : go.Figure) : 
    fig.update_layout(updatemenus =  [
        {
            "type": "buttons",
            "buttons": [{
                "label": "Play",
                "method": "animate",
                "args": [None]
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }]
        }
    ])
