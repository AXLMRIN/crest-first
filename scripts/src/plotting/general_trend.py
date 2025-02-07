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

discipline_to_NOT_show = set(["Toutes", "Aréale", "Autre interdisciplinaire"])

theme = GeneralTheme(**{
    "xaxis" : {"title" : ""},
    "yaxis" : {"title" : ""}
})
eps = 0.025
# Open Files ===================================================================
selected_columns = ["annee", "discipline", "proportion", "text"]

OPENPATH  = "data/preprocessed/"
df_plot = pd.read_csv(OPENPATH + filenames["open_per_revue"])
df_plot = df_plot.loc[df_plot["RA"] == True, selected_columns]
df_plot.index = range(len(df_plot))


DISCIPLINE_SET = sorted(list(
    set(df_plot["discipline"]) - discipline_to_NOT_show
))
n_disciplines : int  = len(DISCIPLINE_SET)
# Create the figure =============================================================
# TODO Refactor
fig = go.Figure( layout = {
    **{
        "xaxis" : {"anchor" : "y", "domain" : [0.0,1]},
        "yaxis" : {"anchor" : "y", "domain" : [0.8,1]}
    },
    **{
        f"yaxis{i+2}" : {
            'anchor': f'y{i+2}'  ,
            'domain': [i * (0.8 / n_disciplines) + eps, 
                       (i + 1) * (0.8 / n_disciplines) - eps]}
        for i in range(n_disciplines)
    },
    **{
        f"xaxis{i+2}" : {'anchor': f'y{i+2}'  , 'domain': [0.0, 1.0  ]}
        for i in range(n_disciplines)
    }
})

theme.xaxis.config["showgrid"] = False
theme.yaxis.config["showgrid"] = False

fig.update_layout({
    "xaxis" : theme.xaxis.config,
    "yaxis" : theme.xaxis.config,
    **{
        f"xaxis{i + 2}" : theme.xaxis.config for i in range(n_disciplines)
    },
    **{
        f"yaxis{i + 2}" : theme.yaxis.config for i in range(n_disciplines)
    }
})

fig.update_layout(
    paper_bgcolor = theme.primary_color,
    plot_bgcolor = theme.primary_color, 
    height = 1800, width = 1000,
    margin=dict(l=50, r=50),
)

fig.update_layout(
    legend = {"visible" : False},
    hoverlabel= {"bgcolor" : theme.tertiary_colour}
)

# Add the traces - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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