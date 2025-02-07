import re

def hex_to_rgb(hex : str):
    ''' Source : https://www.30secondsofcode.org/python/s/hex-to-rgb/
    '''
    if hex.startswith("#") : hex = hex[1:]
    r,b,g = tuple(int(hex[i:i+2], 16) for i in (1, 2, 4))
    return f'rgb({r},{g},{b})'

def is_hex_color(color : str) : 
    '''
    '''
    return len(
       re.sub("^#(?:[0-9a-fA-F]{3}){1,2}$","", color)
       ) == 0

def apply_opacity(color, opacity) : 
    # UPGRADE Make cleaner
    if is_hex_color(color) : 
        color_rgb = hex_to_rgb(color)
    else : color_rgb = color
    return "rgba" + color_rgb[3:-1] +"," +  str(opacity) + ")"

class XAxis :
    def __init__(self, secondary_colour : str, fontsize : int = 15, 
                 fontfamily : str = "New York", title : str = "X Label",
                 grid_opacity : float = 1.0):

        self.config : dict = {
            "showline": True,
            "linewidth": 2,
            "linecolor": secondary_colour,

            "ticks": "outside",
            "tickwidth" : 1,
            "showticklabels": True,
            "tickangle" : 0,
            "tickfont": {
                "family": fontfamily,
                "size": fontsize,
                "color" : secondary_colour
            },

            "showgrid": True,
            "gridcolor" : apply_opacity(secondary_colour, grid_opacity),
            "zerolinecolor" : apply_opacity(secondary_colour, grid_opacity),
            "gridwidth" : 1,

            "title" : {
                "text" : title,
                "font" : {
                    "family" : fontfamily,
                    "size" : 1.2 * fontsize,
                    "color" : secondary_colour
                }
            }
            
        }

class YAxis :
    def __init__(self, secondary_colour : str, fontsize : int = 15, 
                 fontfamily : str = "New York", title : str = "Y Label",
                 grid_opacity : float = 1.0):
        self.config : dict = {
            "showline": False,
            "linewidth": 2,
            "linecolor": secondary_colour,

            "ticks": "outside",
            "tickwidth" : 1,
            "tickangle": 0,
            "showticklabels": True,
            "tickfont": {
                "family": fontfamily,
                "size": fontsize,
                "color" : secondary_colour
                },
            
            "showgrid": True,
            "gridcolor" : apply_opacity(secondary_colour, grid_opacity),
            "zerolinecolor" : apply_opacity(secondary_colour, grid_opacity),
            "gridwidth" : 1,

            "title" : {
                "text" : title,
                "font" : {
                    "family" : fontfamily,
                    "size" : 1.2 * fontsize,
                    "color" : secondary_colour
                }
            }
        }

class Hover : 
    def __init__(self, secondary_colour : str, tertiary_colour : str, 
                 fontfamily : str = "New York", fontsize : int = 12,
                 bg_opacity : float = 1.0):
        self.config : dict = {
            "hoverlabel" : {
                "namelength" : 0,
                "bgcolor" : apply_opacity(tertiary_colour, bg_opacity),
                "font" : {
                    "color" : secondary_colour,
                    "size" : fontsize,
                    "family" : fontfamily
                }
            },
            "hovermode" : "x unified"
        }

class TracesColours : 
    def __init__(self) : 
        self.config : dict = {
            "0-1"  : "#50BA69",
            "0-2"  : "#7DB88B",
            "1-1"  : "#E3BA22",
            "1-2"  : "#BD8F22",
            "2-1"  : "#E6842A",
            "2-2"  : "#BA5F06",
            "3-1"  : "#137B80",
            "3-2"  : "#005D6E",
            "4-1"  : "#8E6C8A",
            "4-2"  : "#684664",
            "5-1"  : "#978F80",
            "5-2"  : "#7C715E",
            "6-1"  : "#BD2D28",
            "6-2"  : "#E25A42",
            "7-1"  : "#0F8C79",
            "7-2"  : "#6BBBA1",
            "8-1"  : "#E6842A",
            "8-2"  : "#688BAB",
            "9-1"  : "#9A3E25",
            "9-2"  : "#B37055",
            "10-1" : "#708259",
            "10-2" : "#95A17E"
        }
    def __getitem__(self, key):
        return self.config[key]
    
    def get_with_opacity(self, key, opacity) : 
        return apply_opacity(self.config[key], opacity)

class Legend : 
    def __init__(self, secondary_colour : str, tertiary_colour : str,
                 fontfamily : str = "New York", fontsize : int = 15,
                 position : tuple = (0.5, 1),
                 anchor : tuple = ("center", "middle")) : 
        
        self.config : dict = {
            "bgcolor" : tertiary_colour,
            "title" : {
                "side" : "top center",
                "font" : {
                    "family" : fontfamily,
                    "size" : fontsize,
                    "color" : secondary_colour
                }
            },
            "groupclick" : "toggleitem",
            "itemdoubleclick" : "toggleothers",
            "itemclick" : "toggle",
            "orientation" : "h",
            "x" : position[0], "xanchor" : anchor[0],
            "y" : position[1], "yanchor" : anchor[1], 
            "entrywidth" : 0.45, "entrywidthmode" : "fraction",
        }

class GeneralTheme : 
    def __init__(self,
                primary_color : str     = "white", 
                secondary_colour : str  = "rgb(34,34,34)",
                tertiary_colour : str   = "rgba(245, 243, 242, 0.4)",
                **kwargs):
        
        for key in ["xaxis", "yaxis", "hover", "legend"] : 
            if key not in kwargs : 
                kwargs[key] = {}


        self.primary_color = primary_color
        self.secondary_colour = secondary_colour
        self.tertiary_colour = tertiary_colour

        self.xaxis = XAxis(secondary_colour = secondary_colour,
                            **kwargs["xaxis"])
        self.yaxis = YAxis(secondary_colour = secondary_colour,
                            **kwargs["yaxis"])
        self.hover = Hover(secondary_colour = secondary_colour,
                           tertiary_colour  = tertiary_colour,
                           **kwargs["hover"])
        self.traces_color = TracesColours()

        self.legend = Legend(secondary_colour = secondary_colour,
                            tertiary_colour  = tertiary_colour,
                            **kwargs["legend"])
            