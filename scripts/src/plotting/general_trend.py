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

# Functions


# Settings =====================================================================
filenames = {
    "open_per_revue" : "general_trend.csv",
    "save" : "general_trend.html"
}

theme = GeneralTheme(**{})

# Open Files ===================================================================
selected_columns = ["annee", "discipline", "proportion", "text"]

OPENPATH  = "data/preprocessed/"
df_plot = pd.read_csv(OPENPATH + filenames["open_per_revue"])
df_plot = df_plot.loc[df_plot["RA"] == True, selected_columns]
df_plot.index = range(len(df_plot))

# Create the figure =============================================================
# TODO Refactor
eps = 0.01
fig = go.Figure(
    layout = {
        'xaxis'   :  {'anchor': 'y'   , 'domain': [0.0, 1.0  ]},
        'xaxis2'  :  {'anchor': 'y2'  , 'domain': [0.0, 1.0  ]},
        'xaxis3'  :  {'anchor': 'y3'  , 'domain': [0.0, 1.0  ]},
        'xaxis4'  :  {'anchor': 'y4'  , 'domain': [0.0, 1.0  ]},
        'xaxis5'  :  {'anchor': 'y5'  , 'domain': [0.0, 1.0  ]},
        'xaxis6'  :  {'anchor': 'y6'  , 'domain': [0.0, 1.0  ]},
        'xaxis7'  :  {'anchor': 'y7'  , 'domain': [0.0, 1.0  ]},
        'xaxis8'  :  {'anchor': 'y8'  , 'domain': [0.0, 1.0  ]},
        'xaxis9'  :  {'anchor': 'y9'  , 'domain': [0.0, 1.0  ]},
        'xaxis10' :  {'anchor': 'y10' , 'domain': [0.0, 1.0  ]},
        'xaxis11' :  {'anchor': 'y11' , 'domain': [0.0, 1.0  ]},
        'yaxis'  :  {'anchor': 'y' , 'domain': [0.80 + eps, 1.0 - eps ]},
        'yaxis2' : {'anchor': 'y2' , 'domain': [0.72 + eps, 0.80 - eps]},
        'yaxis3' : {'anchor': 'y3' , 'domain': [0.64 + eps, 0.72 - eps]},
        'yaxis4' : {'anchor': 'y4' , 'domain': [0.56 + eps, 0.64 - eps]},
        'yaxis5' : {'anchor': 'y5' , 'domain': [0.48 + eps, 0.56 - eps]},
        'yaxis6' : {'anchor': 'y6' , 'domain': [0.40 + eps, 0.48 - eps]},
        'yaxis7' : {'anchor': 'y7' , 'domain': [0.32 + eps, 0.40 - eps]},
        'yaxis8' : {'anchor': 'y8' , 'domain': [0.24 + eps, 0.32 - eps]},
        'yaxis9' : {'anchor': 'y9' , 'domain': [0.16 + eps, 0.24 - eps]},
        'yaxis10': {'anchor': 'y10', 'domain': [0.08 + eps, 0.16 - eps]},
        'yaxis11': {'anchor': 'y11', 'domain': [0.00 + eps, 0.08 - eps]},
        "hoversubplots" : "axis",
    }
)

fig.update_layout(
    paper_bgcolor = theme.primary_color,
    plot_bgcolor = theme.primary_color, 
    height = 1500, width = 1000,
    margin=dict(l=50, r=50),
)

fig.update_layout(
    legend = {"visible" : False},
    hoverlabel= {"bgcolor" : theme.primary_color}
)

# Add the traces - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
DISCIPLINE_SET = sorted(list(
                    set(df_plot["discipline"]) - set(["Toutes", "Autre interdisciplinaire"])
                ))
print(DISCIPLINE_SET)
df_grouped = df_plot.groupby("discipline")
for i, discipline in enumerate(DISCIPLINE_SET) : 

    fig.add_trace(go.Scatter(
        x = df_grouped.get_group(discipline)["annee"],
        y = df_grouped.get_group(discipline)["proportion"],
        customdata = df_grouped.get_group(discipline)["text"],
        name = discipline,
        hovertemplate = "%{customdata}",
        mode = "lines", line = {"color" : theme.traces_color[f'{i}-1']},
        xaxis = f'x{i+2}', yaxis = f'y{i+2}'
    ))

    fig.add_trace(go.Scatter(
        x = df_grouped.get_group("Toutes")["annee"],
        y = df_grouped.get_group("Toutes")["proportion"],
        mode = "lines", line = {
            "color" : "black",
            "width" : 1,
            "dash" : "longdash"
        },
        xaxis = f'x{i+2}', yaxis = f'y{i+2}',
        hovertemplate = None
    ))

# Save the figure ===============================================================
SAVEPATH = "views/"
fig.write_html(SAVEPATH + filenames["save"],
               include_plotlyjs = True, include_mathjax = False)