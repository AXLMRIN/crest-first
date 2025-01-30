# Third Parties
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np 

# Native
# NOTE might be worth finding a cleaner way to do that
import sys
sys.path.append(("/Users/axelmorin/Library/Mobile Documents/com~apple~CloudDocs"
                 "/Axel_tout/Professionnel/Stages/TFE/CREST/workdirectory/Genre"
                 "/dataVis/plotly-datavis-crest/scripts/src"))

# Custom 
from package.temp import (
    add_traces_to_subplot, 
    add_traces_to_subplot_bi_colours_filling
)

# Classes
from plotly.graph_objs._figure import Figure as goFigure

# Functions
from plotly.subplots import make_subplots
from itertools import product

# FIXME The whole structure is falling appart, urgent need to redo it all !! 

# Settings =====================================================================
all_disciplines = [
    'Science politique'         ,
    'Sociologie'	            ,
    'Anthropologie'	            ,
    'Histoire'	                ,
    # 'Autre interdisciplinaire'	,
    'Démographie'               ,
    'Economie'                  ,
    'SIC'	                    ,
    'Géographie'	            ,
    # 'Aréale'
    ]

tick_grid_colour = 'rgb(50,50,50)'

colour_main_traces = 'black'
colour_bg_traces = 'rgba(200,200,200,0.5)'
colour_toutes = 'black'
colour_toutes_sauf_genre = 'black'

linewidth_main_traces   = 3
linewidth_bg_traces     = 1

fill_colour = 'rgba(180,180,180,0.7)'

dash_main = 'solid'
dash_toutes = 'longdash'
dash_toutes_sauf_genre = 'dashdot'

# Traces customisation kwargs - - - - - - - - - - - - - - - - - - - - - - - - -
# HERE change legend and customisation of the main traces of part 1
part_1_traces_customisation = {
    'Toutes' : {
        'local' :
            [{
                'name' : "Revues spécialisées en études de genre",
                'line' : {
                    'color' : colour_main_traces,
                    'width' : linewidth_main_traces,
                    'dash' : dash_main
                    }
            }]
        },
        'Toutes sauf Genre' :{
            'local' : [{
                'name' : "Moyenne des revues",
                'line' : {
                    'color' : colour_toutes,
                    'width' : linewidth_main_traces,
                    'dash' : dash_toutes
                    }
            }]
        },
        'Genre' :{ 
            'local' : [{
                    'name' :  ("Moyenne des revues, sans revues de genre"),
                    'line' : {
                        'color' : colour_toutes_sauf_genre,
                        'width' : linewidth_main_traces,
                        'dash' : dash_toutes_sauf_genre
                        }
                }]
        }
}

# HERE to modify the traces that will be in the background of part 1
part_1_bg_traces_customisation = {
    'global' : {
        'line' : {
            'color' : colour_bg_traces,
            'width' : linewidth_bg_traces},
        'showlegend' : False,
        'hoverinfo' : 'skip'
    }
}

# HERE to modify the traces in the second part of the graph
part_2_customisation = {
    'local' : [
        {   
            'name' : "Moyenne des revues",
            'line' : {
                'color' : colour_toutes,
                'width' : linewidth_main_traces,
                'dash' : dash_toutes
            },
            'showlegend' : False
        },
        {
            'line' : {
                'color' : colour_main_traces,
                'width' : linewidth_main_traces,
                'dash' : dash_main,
            },
            'showlegend' : False
        }
    ],
    'bi-colouring-args' : [
        'rgba(255,255,255,0.2)',        # underneath
        'rgba(140,140,140,0.2)   '      # above
        ]
}
# ==============================================================================

# Variables derived from Settings ----------------------------------------------
n_rows = len(all_disciplines) + 1

# Reading files -----------------------------------------------------------------
# HERE Modify the path according to your configuration
dfPlot      = pd.read_csv("data/preprocessed/figure_1.csv").groupby("RA")
dfPlot_raw = dfPlot.get_group(False)
dfPlot_ra  = dfPlot.get_group(True)

# Creating subplot figure -------------------------------------------------------

# https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html
fig = make_subplots(
    rows = n_rows , cols = 1,
    specs = [[{}]] * n_rows,
    row_heights= [n_rows - 1] + [1] * (n_rows - 1),
    start_cell = "top-left", 
    subplot_titles=[""] + all_disciplines,

    shared_xaxes = True,
    print_grid = True,

    x_title = 'Année de publication',
    y_title = ''
)

# Setting title
fig.update_layout(dict(
    title = dict(), # No Title
    width = 1000, height = 1400,
    plot_bgcolor = 'white',
))

# Define graph 1 ----------------------------------------------------------------
# Set x and y axis

fig.update_layout(
    xaxis = dict(
        showline = True,
        linewidth = 1,
        linecolor = tick_grid_colour,

        ticks = 'outside',
        showticklabels = True,
        tickangle = 0,
        tickwidth = 1,
        tickfont = dict(),
        tickvals = [2000,2005,2010,2015,2020],
        
        showgrid = False
    ),
    yaxis = dict(
        showline = False,

        ticks = "outside",
        showticklabels = True,
        tickangle = 0,
        tickfont = dict(),
        tickvals = [10,50,92],
        ticksuffix = "%",
        tickwidth = 1,

        showgrid = True,
        gridcolor = tick_grid_colour,
        gridwidth = 1,

        autorange = True,
        # range = [1, 100],
    )
)

# Customise legend
fig.update_layout(dict(
    legend = dict(
        bgcolor = 'rgba(255,255,255,1)',
        itemsizing = 'trace',
        orientation = "h",
        xanchor = 'left',
        yanchor = 'top',
        x = .1, y = 1.05,
        traceorder = 'normal'
    )
))

# Add all the disciplines in the background
for discipline, discipline_df_raw in dfPlot_raw.groupby("discipline") : 
    if (discipline in all_disciplines) | (discipline == "Genre") : 
        add_traces_to_subplot(fig,discipline_df_raw,
                            x = "annee",columns=["proportion"],
                            row = 1, col = 1,
                            **part_1_bg_traces_customisation) # All categories except gender studies

# Add the colourful traces
for discipline, discipline_df_ra in dfPlot_ra.groupby("discipline") : 
    if discipline in ["Genre", "Toutes", "Toutes sauf Genre"] : 
        add_traces_to_subplot(  fig, discipline_df_ra,
                                x = "annee",
                                columns = ["proportion"],
                                row = 1, col = 1, **part_1_traces_customisation[discipline])

# Create the other subfigures ---------------------------------------------------
yaxis_theme = {
    'showline'  : False,
    'showgrid'  : False,
    'ticks'     : "",
    'showticklabels' : False,
}

xaxis_theme = {
    'showline'  : False,
    'showgrid'  : False,
    'ticks'     : "outside",
    'showticklabels' : True,
    'tickfont' : {
        'size' : 12
    }
}

# Add the traces for the categories in all_disciplines
for i, discipline in enumerate(all_disciplines):
    # FIXME Really need to think of a better way to do it 
    temp_df = pd.DataFrame({
        "annee" : dfPlot_ra.groupby("discipline").get_group(discipline)["annee"],
        "Toutes" : dfPlot_ra.groupby("discipline").get_group('Toutes')["proportion"].to_numpy(),
        discipline : dfPlot_ra.groupby("discipline").get_group(discipline)["proportion"].to_numpy()
    })
    
    add_traces_to_subplot_bi_colours_filling(fig, temp_df,
        x = "annee", columns = ['Toutes'] + [discipline],
        row = i + 2, col = 1, **part_2_customisation)

# Apply theme to axis
fig.update_layout({
    key : yaxis_theme for key in ['yaxis' + str(i) for i in range(2,n_rows + 1)]
})
fig.update_layout({
    key : xaxis_theme for key in ['xaxis' + str(i) for i in range(2,n_rows + 1)]
})

# Hover parameters
fig.update_layout(dict(
    hovermode="x unified",
    hoversubplots="axis",
    ))

# Save the fig ------------------------------------------------------------------
# fig.write_image('fig_test.png')
fig.write_html('views/figure_1.html')
