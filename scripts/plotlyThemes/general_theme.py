import re
from copy import deepcopy
from mergedeep import merge

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

def merge_dictionnaries(internal : dict, external : dict) -> dict: 
    # internal = deepcopy(internal) # NOTE might be removed
    # # https://www.geeksforgeeks.org/recursively-merge-dictionaries-in-python/
    # for key, value in external.items():
    #     if key in internal and\
    #        isinstance(internal[key], dict) and\
    #        isinstance(value, dict):
    #         # Recursively merge nested dictionaries
    #         merge_dictionnaries(internal[key], value)
    #     else:
    #         # Merge non-dictionary values
    #         internal[key] = value 
    # return internal
    internal = deepcopy(internal)
    return merge(internal, external)

class XAxis :
    def __init__(self, secondary_colour : str, fontsize : int = 15, 
                 fontfamily : str = "New York", title : str = "X Label",
                 grid_opacity : float = 1.0):
        # FIXME grid_opacity is not linked to anything

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
            "gridcolor" : secondary_colour,
            "zerolinecolor" : secondary_colour,
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
    def set_config(self, external_config : dict): 
        self.config = merge_dictionnaries(self.config, external_config)
       

class YAxis :
    def __init__(self, secondary_colour : str, fontsize : int = 15, 
                 fontfamily : str = "New York", title : str = "Y Label",
                 grid_opacity : float = 1.0):
        # FIXME grid_opacity is not linked to anything

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
            "gridcolor" : secondary_colour,
            "zerolinecolor" : secondary_colour,
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
    def set_config(self, external_config : dict): 
        self.config = merge_dictionnaries(self.config, external_config)

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
    def set_config(self, external_config : dict): 
        self.config = merge_dictionnaries(self.config, external_config)

class TracesColours : 
    def __init__(self) : 
        # TODO Clean that up
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
            "10-2" : "#95A17E",
            'Anthropologie'             : "#F2DA57",
            'Aréale'                    : "#8E8E8E",
            'Autre interdisciplinaire'  : "#AFAFAF",
            'Démographie'               : "#E6842A",
            'Économie'                  : "#137B80",
            'Genre'                     : "#8E6C8A",
            'Géographie'                : "#5C8100",
            'Histoire'                  : "#BD2D28",
            'SIC'                       : "#3A3A3A",
            'Science politique'         : "#E6842A",
            'Sociologie'                : "#BD8F22"
        }
    def __getitem__(self, key):
        return self.config[key]
    
    def get_with_opacity(self, key, opacity) : 
        return apply_opacity(self.config[key], opacity)
    
    def set_config(self, external_config : dict): 
        self.config = merge_dictionnaries(self.config, external_config)

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

    def set_config(self, external_config : dict): 
        self.config = merge_dictionnaries(self.config, external_config)

class GeneralTheme : 
    def __init__(self,
                primary_color : str     = "white", 
                secondary_colour : str  = "rgb(34,34,34)",
                tertiary_colour : str   = "rgba(200,200,200, 0.4)",
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
        
    def change_config(self, external_config_hub): 
        if "xaxis" in external_config_hub : 
            self.xaxis.set_config(external_config_hub["xaxis"])
        
        if "yaxis" in external_config_hub : 
            self.yaxis.set_config(external_config_hub["yaxis"])
        
        if "hover" in external_config_hub : 
            self.hover.set_config(external_config_hub["hover"])
        
        if "traces_color" in external_config_hub : 
            self.traces_color.set_config(external_config_hub["traces_color"])
        
        if "legend" in external_config_hub : 
            self.legend.set_config(external_config_hub["legend"])
        
            