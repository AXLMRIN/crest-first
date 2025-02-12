import pandas as pd
import numpy as np
import plotly.graph_objects as go

from .. import GeneralTheme
from .data_plotter import (
    title_on_the_side,
    yScale, customHistogram
)

class Auteurice : 
    def __init__(self,
        filename_open : str,
        filename_save : str,
        alternative_config : dict = {}) :
        # Open files
        selected_columns = ["discipline", "r_w", "r_m", "r_w_g", "r_m_g"]

        OPENPATH  = "data/preprocessed/"
        df_plot = pd.read_csv(OPENPATH + filename_open)
        df_plot = df_plot.loc[:, selected_columns]
        df_plot.index = range(len(df_plot))

        # Load theme
        theme = GeneralTheme()
        theme.change_config(alternative_config)

        # Figure section
        fig = go.Figure(layout = {
            "paper_bgcolor" : theme.primary_color,
            "plot_bgcolor"  : theme.primary_color
        })
        
        if "general" in alternative_config : 
            fig.update_layout(alternative_config["general"])

        fig.update_layout(
            xaxis = theme.xaxis.config,
            yaxis = theme.yaxis.config,
            legend = theme.legend.config,
        )
        # Create the histogram
        custom_hist = customHistogram()
        custom_hist.set_axis_labels(fig, theme.xaxis.config["range"])

        # Add the labels on the side
        title_on_the_side(fig, "Femme (présumé)", x = 0, orientation = -90)
        title_on_the_side(fig, "Homme (présumé)", x = 1, orientation =  90)
        # ...
        # NOTE Might be refactored
        idx = np.argsort(df_plot["r_w"])
        discipline_list = np.array(df_plot["discipline"])

        y_scale = yScale(factor = 1 / len(df_plot),
                 offset = 0.05, 
                 order  = {
                     discipline : i
                     for i,discipline in enumerate(discipline_list[idx])
                 })
        for discipline, discipline_df in df_plot.groupby("discipline") : 
            custom_hist.display_for_a_category(fig, y_scale, discipline, discipline_df)

        # Add a custom legend
        custom_hist.add_custom_legend(fig)

        # Save section
        SAVEPATH = "views/"
        # NOTE change 'include_plotlyjs' for lighter files
        fig.write_html(SAVEPATH + filename_save,
                    auto_play = False,
                    include_plotlyjs = True, include_mathjax = False)

