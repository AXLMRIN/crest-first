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
    "y" :  1.05, "yanchor" : "middle",

    "orientation":'h',
    "thickness" : 20, "len" : 1,

    "ticks" : "inside", "ticklen" : 20, "tickcolor" : "white",
    "tickvals" : [0,10, 25,50,75,100],
    "ticksuffix" : " %",
    "labelalias" : {10 : "Moyenne"}
}

COLORSCALE = [
    [0, "rgb(255,255,255)"],
    [0.5, "rgb(255,0,0)"],
    [1.0, "rgb(0,0,0)"],
]


# Export functions =============================================================
def add_heatmap(fig : go.Figure, x : np.ndarray, y : np.ndarray,
                z : np.ndarray) -> None:
    """takes in the figure and the 3 necessary vectors : 
    x, y (1D) and z (2D) as well as the kwargs and turn it into a go.Heatmap
    object. 
    the function returns a dictionnary mapping the name of the Heatmap to 
    the index of in the fig.data

    The kwargs must only refer to the add_trace function, no customisation 
    yet"""
    
    fig.add_trace(
        go.Heatmap(x = x, y = y, z = z, 
               colorbar = COLORAR, colorscale = COLORSCALE,
               xaxis = "x", yaxis = "y2",
               visible = False, xgap = 5, ygap = 5, 
               zauto = False, zmin = 0, zmax = 100, zmid = 50)
    )
