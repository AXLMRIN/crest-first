import pandas as pd
import plotly.graph_objects as go

from .. import GeneralTheme
from .data_plotter import (
    create_data, create_frame
)
class ScatterPlot : 
    def __init__(self,
        filename_open : str,
        filename_save : str,
        alternative_config : dict = {}) :

        # Open Files ===================================================================
        selected_columns = ["revue", "discipline", "annee","proportion_genre",
                            "proportion_classe", "n_articles", "text"]

        OPENPATH  = "data/preprocessed/"
        df_plot = pd.read_csv(OPENPATH + filename_open)
        df_plot = df_plot.loc[df_plot["RA"] == True, selected_columns]
        df_plot.index = range(len(df_plot))

        # Load the theme
        theme = GeneralTheme()
        theme.change_config(alternative_config)

        # Create Figure
        fig = go.Figure(layout = {
            "paper_bgcolor" : theme.primary_color,
            "plot_bgcolor"  : theme.primary_color
        })

        if "general" in alternative_config : 
            fig.update_layout(alternative_config["general"])
        fig.update_layout(
            xaxis = theme.xaxis.config,
            yaxis = theme.yaxis.config,
            legend = theme.legend.config
        )
        # ...
        # FIXME 2020 is going to break
        create_data(fig, 
            df_plot.groupby("annee").get_group(2020),
            theme.traces_color)
        
        sliders_dict = {
            "active": 0,
            "currentvalue": {
                "font": {
                    "size": 20,
                    "family" : "New York"
                },
                "prefix": "Année : ",
                "visible": True,
                "xanchor": "left",
                "offset" : 20
            },
            "transition": {
                "duration": 30000,
                "easing": "cubic-in-out"
            },
            "pad": {"b": 10, "t": 50},
            "len": 0.9,

            "x": 0.5, "xanchor": "center",
            "y": -0.15, "yanchor": "middle",

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
        # create_control_buttons(fig)
        
        # Save the figure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        SAVEPATH = "views/"
        # NOTE change 'include_plotlyjs' for lighter files
        fig.write_html(SAVEPATH + filename_save,
                    auto_play = False,
                    include_plotlyjs = True, include_mathjax = False)