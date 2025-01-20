# Third Parties
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np 

# Native

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

#-------------------------------------------------------------------------------
# Settings =====================================================================
all_categories = [
    'Science politique',
    'Sociologie'	,
    'Anthropologie'	,
    'Histoire'	,
    'Autre interdisciplinaire'	,
    'Démographie',
    'Economie',
    'SIC'	,
    'Géographie'	,
    'Aréale']
# ==============================================================================


# Reading files -----------------------------------------------------------------
dfPlot      = pd.read_csv('data/checkpoints/dfPlot.csv')
dfPlotRA    = pd.read_csv('data/checkpoints/dfPlotRA.csv')

# Creating subplot figure -------------------------------------------------------

# https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html
fig = make_subplots(
    rows=11, cols=1,
    specs=[[{}]] * 11,
    row_heights= [0.5] + [0.05] * 10,
    subplot_titles=(
       "","Science Politique","Sociologie","Anthropologie",
       "Histoire", "Démographie", "Économie","SIC", "Géographie", "Aréales", 
       "Autre interdisciplinaire"),

       shared_xaxes = 'all',
       print_grid = True,

       x_title = 'Année de publication',
       y_title = ''
)

# Setting title and axis names
fig.update_layout(dict(
    title = dict(), # No Title
    width = 1150, height = 1400,
    plot_bgcolor = 'white',
    # showlegend = False
))






# Parameters -------------------------------------------------------------------
tick_grid_colour = 'rgb(50,50,50)'

colour_main = 'black'
colour_bg = 'rgba(200,200,200,0.5)'
colour_toutes = 'black'
colour_toutes_sauf_genre = 'black'

linewidth_main  = 3
linewidth_bg    = 1

fill_colour = 'rgba(180,180,180,0.7)'

dash_main = 'solid'
dash_toutes = 'longdash'
dash_toutes_sauf_genre = 'dashdot'

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

# Change legend 
fig.update_layout(dict(
    legend = dict(
        bgcolor = 'rgba(255,255,255,1)',
        itemsizing = 'trace',
        orientation = "h",
        xanchor = 'left',
        yanchor = 'top',
        x = .1, y = 1.05
    )
))

# Add all the categories in the background

kwargs = {
    'global' : {
        'line' : {
            'color' : colour_bg,
            'width' : linewidth_bg},
        'showlegend' : False
    }
}

add_traces_to_subplot(fig,dfPlot,
                      x = "annee",columns=all_categories,
                      row = 1, col = 1, **kwargs) # All categories except gender studies
add_traces_to_subplot(fig, dfPlot,
                      x = "annee", columns=["Genre"],
                      row = 1, col = 1, **kwargs)

# Add the colourful traces
kwargs = {
    'local' : [
        {
            'name' : "Moyenne de toutes les revues",
            'line' : {
                'color' : colour_toutes,
                'width' : linewidth_main,
                'dash' : dash_toutes
                }
        },
        {
            'name' :  ("Moyennes de toutes les revues qui ne sont pas"
                       " des revues spécialisées dans les études de genre"),
            'line' : {
                'color' : colour_toutes_sauf_genre,
                'width' : linewidth_main,
                'dash' : dash_toutes_sauf_genre
                }
        },
        {
            'name' : "Revues spécialisées dans les études de genre",
            'line' : {
                'color' : colour_main,
                'width' : linewidth_main,
                'dash' : dash_main
                }
        }
    ]
}
add_traces_to_subplot(  fig, dfPlotRA,
                        x = "annee",
                        columns = ["Toutes", "Toutes sauf Genre", "Genre"],
                        row = 1, col = 1, **kwargs)

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

kwargs_subplots = {
    'local' : [
        {
            'line' : {
                'color' : colour_toutes,
                'width' : linewidth_main,
                'dash' : dash_toutes
            },
            'showlegend' : False
        },
        {
            'line' : {
                'color' : colour_main,
                'width' : linewidth_main,
                'dash' : dash_main,
            },
            # 'fill' : 'tonexty',
            # 'fillcolor' : fill_colour, 
            'showlegend' : False
        }
    ],
    'bi-colouring-args' : ['red','blue']
}

# Science Politique - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig.update_layout(dict(
    yaxis2 = yaxis_theme,
    xaxis2 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Science politique"],
                      row = 2, col = 1, 
                      **kwargs_subplots)

# Sociologie - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig.update_layout(dict(
    yaxis3 = yaxis_theme,
    xaxis3 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Sociologie"],
                      row = 3, col = 1, 
                      **kwargs_subplots)

# Anthropologie -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig.update_layout(dict(
    yaxis4 = yaxis_theme,
    xaxis4 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Anthropologie"],
                      row = 4, col = 1, 
                      **kwargs_subplots)

# Histoire - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig.update_layout(dict(
    yaxis5 = yaxis_theme,
    xaxis5 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Histoire"],
                      row = 5, col = 1, 
                      **kwargs_subplots)

# Démographie - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(dict(
    yaxis6 = yaxis_theme,
    xaxis6 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Démographie"],
                      row = 6, col = 1, 
                      **kwargs_subplots)

# Economie - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - 
fig.update_layout(dict(
    yaxis7 = yaxis_theme,
    xaxis7 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Economie"],
                      row = 7, col = 1, 
                      **kwargs_subplots)

# SIC - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig.update_layout(dict(
    yaxis8 = yaxis_theme,
    xaxis8 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "SIC"],
                      row = 8, col = 1, 
                      **kwargs_subplots)

# Géographie - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig.update_layout(dict(
    yaxis9 = yaxis_theme,
    xaxis9 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Géographie"],
                      row = 9, col = 1, 
                      **kwargs_subplots)

# Aréales - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig.update_layout(dict(
    yaxis10 = yaxis_theme,
    xaxis10 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Aréale"],
                      row = 10, col = 1, 
                      **kwargs_subplots)

# Autre interdisciplinaire - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig.update_layout(dict(
    yaxis11 = yaxis_theme,
    xaxis11 = xaxis_theme
))

add_traces_to_subplot_bi_colours_filling(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Autre interdisciplinaire"],
                      row = 11, col = 1, 
                      **kwargs_subplots)

# Save the fig ------------------------------------------------------------------
fig.write_image('fig_test.png')
