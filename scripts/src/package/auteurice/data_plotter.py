# Third Parties
import plotly.graph_objects as go
import pandas as pd

# Native

# Custom 

# Classes

# Functions

# ==============================================================================


def make_a_bar(x : float, y : float, dx : float, dy : float,
               **scatter_kwargs) -> go.Scatter:
    return go.Scatter(
        x = [
            x,
            x + dx,
            x + dx, 
            x,
            x
        ],
        y = [
            y - dy / 2,
            y - dy / 2,
            y + dy / 2,
            y + dy / 2,
            y - dy / 2
        ],
        fill = "toself",
        mode = "lines",
        text = f"{abs(dx):.1f} %",
        hoverinfo="text",
        **scatter_kwargs
    )