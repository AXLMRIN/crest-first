# Third Parties
from typing import Any
import plotly.graph_objects as go
import pandas as pd

# Native

# Custom 

# Classes

# Functions

# ==============================================================================

def title_on_the_side(fig : go.Figure, text : str, x : float,
                      orientation : float) -> None :
    fig.add_annotation(
        text = text, textangle= orientation, x = x, y = 0.5,
        xref = "paper", yref = "paper",
        showarrow = False, 
        xanchor = "center", align = "center"
    )

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

def label_transform(x : float, dx1 : float, dx2 : float) -> float: 
    """
    even with xref, yref being "paper", the (0,0) point points to the 
    bottom left corner of the plot area and (1,1) to the top right corner
    """
    return (x + dx1) / (dx1 + dx2)
class yScale : 
    def __init__(self, factor, offset, order : dict[str:int]) : 
        self.factor = factor
        self.offset = offset
        self.order = order # dictionnary discipline -> i

    def __call__(self,discipline):
        return self.factor * self.order[discipline] + self.offset



class customHistogram:
    def __init__(self, 
                middle_gap : float = 30.0, bin_size :float = 0.05,
                color_1_1 : str = "#F6B656", color_1_2 : str = "#BA5F06",
                color_2_1 : str = "#B396AD", color_2_2 : str = "#684664"):
        self.middle_gap : float = middle_gap
        self.bin_size : float = bin_size
        self.color_1_1 : str = color_1_1
        self.color_1_2 : str = color_1_2
        self.color_2_1 : str = color_2_1
        self.color_2_2 : str = color_2_2

        self.line_style = {
            "color" : "white",
            "width" : 0.5
        }

    def set_axis_labels(self, fig : go.Figure, 
                        x_axis_range : tuple[float, float]) -> None: 
        tickvals : list[float] = [ 
            - self.middle_gap - 50, - self.middle_gap - 25,
              self.middle_gap + 50,   self.middle_gap + 25,
            - self.middle_gap - 75,   self.middle_gap + 75
        ]
        
        fig.update_layout({
            "xaxis" : {"tickvals" : tickvals}
        })

        dx1, dx2 = (abs(el) for el in x_axis_range)

        alias = {
            value : f'{int(abs(value) - self.middle_gap)} %'
            for value in tickvals
        }

        for x in alias : 
            fig.add_annotation(
                text = alias[x],
                x = label_transform(x, dx1, dx2), y = -0.05,
                xref = "paper", yref = "paper",
                xanchor = "center", align = "center",
                showarrow = False
            )

    def display_for_a_category(self, fig : go.Figure, y_scale : yScale,
                               discipline : str, discipline_df : pd.DataFrame
                               ) -> None: 
        args = {
            'line' : self.line_style,
            'showlegend' : False
        }

        # Add rates for people that didnt mention gender - - - - - - - - - - - -
        args["name"] = "ne mentionne pas le genre"
        # Add women rates
        args["fillcolor"] = self.color_1_1
        args["legendgroup"] = "Femme"
        fig.add_trace(
            make_a_bar( - self.middle_gap, y_scale(discipline),
                    -1 * discipline_df["r_w"].item(), self.bin_size,
                    **args)
        )
        
        # Add men rates
        args["fillcolor"] = self.color_2_1
        args["legendgroup"] = "Homme"
        fig.add_trace(
            make_a_bar(self.middle_gap, y_scale(discipline),
                    discipline_df["r_m"].item(), self.bin_size,
                    **args)
        )

        # Add rates for people that DID mention gender - - - - - - - - - - - - - 
        args["name"] = "mentionne le genre"
        # Add women rates
        args["fillcolor"] = self.color_1_2
        args["legendgroup"] = "Femme"
        fig.add_trace(
            make_a_bar( - self.middle_gap, y_scale(discipline),
                    -1 * discipline_df["r_w_g"].item(), self.bin_size,
                    **args)
        )
        
        
        # Add men rates specialised in gender
        args["legendgroup"] = "Homme"
        args["fillcolor"] = self.color_2_2
        fig.add_trace(
            make_a_bar( self.middle_gap, y_scale(discipline),
                    discipline_df["r_m_g"].item(), self.bin_size,
                    **args)
        )

        # Add the discipline name - - - - - - - - - - - - - - - - - - - - - - - 
        fig.add_trace(
            go.Scatter(
                x = [0], y = [y_scale(discipline)],
                mode="text",
                text=[discipline],
                textposition="middle center",
                textfont=dict(
                    family="sans serif",
                    size=18
            ),
            showlegend = False, name = "",
            hovertemplate = (
                f"<b>{discipline}</b><br>"
                f"Homme : {discipline_df["r_m"].item():.1f} % ont publié, "
                f"{discipline_df["r_m_g"].item():.1f} % ont parlé de genre <br>"
                f"Femme : {discipline_df["r_w"].item():.1f} % ont publié, "
                f"{discipline_df["r_w_g"].item():.1f} % ont parlé de genre<br>"
                )
            )
        )
    
    def add_custom_legend(self, fig : go.Scatter) -> None : 

        # With colors ==========================================================
        # fig.add_trace(
        #     go.Scatter(
        #         x = [None], y = [None],
        #         fill = "toself", fillcolor = self.color_1_1,
        #         name = "ne mentionne pas le genre", legendgroup = "Femme",
        #         mode = "lines", showlegend = True,
        #         line = self.line_style
        #     )
        # )
        
        # fig.add_trace(
        #     go.Scatter(
        #         x = [None], y = [None],
        #         fill = "toself", fillcolor = self.color_1_2,
        #         name = "mentionne le genre", legendgroup = "Femme",
        #         mode = "lines", showlegend = True,
        #         line = self.line_style
        #     )
        # )
        
        # fig.add_trace(
        #     go.Scatter(
        #         x = [None], y = [None],
        #         fill = "toself", fillcolor = self.color_2_1,
        #         name = "ne mentionne pas le genre", legendgroup = "Homme",
        #         mode = "lines", showlegend = True,
        #         line = self.line_style
        #     )
        # )
        
        # fig.add_trace(
        #     go.Scatter(
        #         x = [None], y = [None],
        #         fill = "toself", fillcolor = self.color_2_2,
        #         name = "mentionne le genre", legendgroup = "Homme",
        #         mode = "lines", showlegend = True,
        #         line = self.line_style
        #     )
        # )

        # Grey shades ==========================================================
        
        fig.add_trace(
            go.Scatter(
                x = [None], y = [None],
                fill = "toself", fillcolor = "rgb(169,169,169)",
                name = "ne mentionne pas le genre",
                mode = "lines", showlegend = True,
                line = self.line_style
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x = [None], y = [None],
                fill = "toself", fillcolor = "rgb(93,93,93)",
                name = "mentionne le genre",
                mode = "lines", showlegend = True,
                line = self.line_style
            )
        )
        