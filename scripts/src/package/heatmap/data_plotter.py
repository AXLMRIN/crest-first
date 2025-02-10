# Third Parties
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Native

# Custom 

# Classes

# Functions

# Constants ====================================================================
COLORAR ={
    "x" : 0.5, "xanchor" : "center",
    "y" :  1.01, "yanchor" : "bottom",

    "orientation":'h',
    "thickness" : 20, "len" : 1,

    "ticks" : "inside", "ticklen" : 20, "tickcolor" : "white",
    "tickvals" : [0,10, 25,50,75,100],
    "ticksuffix" : " %",
    "labelalias" : {10 : "Moyenne"}
}

# https://www.learnui.design/tools/data-color-picker.html#divergent
# COLORSCALE = [
#     [0,    "#488f31"],
#     [0.25, "#b7b66c"],
#     [0.5,  "#ffe4c3"],
#     [0.75, "#ec9974"],
#     [1.0,  "#de425b"]]

# https://github.com/ucarion/cielab.io?tab=readme-ov-file
COLORSCALE = [
    [0,    "rgb(199, 198, 197)"],
    [0.25, "rgb(196, 163, 167)"],
    [0.5,  "rgb(198, 124, 133)"],
    [0.75, "rgb(202, 75, 93)"],
    [1.0,  "rgb(192, 0, 25)"]]


# Export functions =============================================================
def set_max_length(ticks : list[str], n = 25):
    ticks = ticks.copy()
    for i in range(len(ticks)) : 
        if len(ticks[i]) > n :
            ticks[i] = ticks[i][:n-3] + "..." 
        else :
            while len(ticks[i]) < n :
                ticks[i] = " " + ticks[i]
    return ticks

def make_custom_data(revue_names : list[str], n : int) : 
    return [[revue] * n for revue in revue_names]

def add_heatmap(fig : go.Figure, annees : np.ndarray, revue_names : np.ndarray, 
                proportions : np.ndarray, discipline : str) -> None:
    """takes in the figure and the 3 necessary vectors : 
    x, y (1D) and z (2D) as well as the kwargs and turn it into a go.Heatmap
    object. 
    the function returns a dictionnary mapping the name of the Heatmap to 
    the index of in the fig.data

    The kwargs must only refer to the add_trace function, no customisation 
    yet"""
    
    fig.add_trace(
        go.Heatmap(x = annees, y = set_max_length(revue_names), z = proportions, 
            colorbar = COLORAR, colorscale = COLORSCALE,
            xaxis = "x2", yaxis = "y2", name = discipline,
            visible = False, xgap = 5, ygap = 5, 
            zauto = False, zmin = 0, zmax = 100, zmid = 50,
            customdata = make_custom_data(revue_names, len(annees)),
            hovertemplate = "<b>%{customdata}</b><br>%{z:.1f} %")
    )

def visible(discipline, binder) : 
    output = [False] * len(binder)
    output[binder[discipline + "_heatmap"]] = True
    output[binder[discipline + "_trace"]] = True
    output[binder["Toutes_trace"]] = True
    return output

def add_menu(fig : go.Figure, binder : dict, discipline_sizes : list[str],
             y_axis_theme) : 
    domain_sizes = [
        0.7,            # Anthropologie
        0.775,          # Aréale
        0.6625,         # Autre interdisciplinaire
        0.925,          # Démographie
        0.8125,         # Économie
        0.8125,         # Genre
        0.7375,         # Géographie
        0.7,            # Histoire
        0.7375,         # SIC
        0.775,          # Science Politique
        0.7375]         # Sociologie
    
    # Use .update_layout() method to add dropdown bar
    fig.update_layout(
        updatemenus=[dict(
            buttons= [
                {
                    "label" : discipline,
                    "method" : "update",
                    "args" : [
                        {"visible" : visible(discipline, binder)},
                        {
                            "yaxis2" : {
                                "domain" : [discipline_sizes[discipline],1.0],
                                **y_axis_theme.config
                            }
                        }
                    ]
                } for discipline in discipline_sizes
            ],
            x = 0.5, xanchor = "center",
            y = 1.15, yanchor = "bottom",
            type = "buttons",
            direction = "left", 
            showactive = True,
        )]
    )
