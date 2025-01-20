# Third Parties
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np 

# Native

# Custom 
# /

# Classes
from plotly.graph_objs._figure import Figure as goFigure
# Functions
from plotly.subplots import make_subplots
from itertools import product

#-------------------------------------------------------------------------------

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
fig = fig.update_layout(dict(
    title = dict(
            text = ("Insightful title"),
             automargin = True,  # TODO Check the margins and pads again
             pad = dict(t = 10, b = 10 , r = 10, l = 10)),
    width = 1150, height = 1400,
    plot_bgcolor = 'white',
    showlegend = False
))

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

def add_traces_to_subplot(fig : goFigure, df : pd.DataFrame,
                          x : str, columns : list[str],
                          row : int, col : int, **kwargs) -> None:
    '''takes a dataframe and addit to the figure. 
    the kwargs can contain : 
        {
        # will be applied to the traces one at a time
         'local' : {
                        [kwargs, kwargs, ]
                    }, 
        # will be applied to all the traces
         'global' : kwargs 
        }
    all customisation must be in the kwargs
    '''

    for i, column  in zip( range(len(columns)), columns):
        fig.add_trace(
            go.Scatter(
                x = df[x], y = df[column],
                mode = 'lines'
            ), row = row, col = col
        )
        if 'global' in kwargs:
            fig.data[-1].update(kwargs['global'])
        if 'local' in kwargs: 
            fig.data[-1].update(**kwargs['local'][i])


# Parameters -------------------------------------------------------------------
tick_grid_colour = 'rgb(50,50,50)'
colour_main = 'black'
colour_bg = 'rgba(200,200,200,0.5)'
colour_toutes = 'red'
colour_toutes_sauf_genre = 'green'
linewidth_main  = 3
linewidth_bg    = 1
fill_colour = 'rgba(180,180,180,0.7)'

# Define graph 1 ----------------------------------------------------------------
# Set x and y axis

fig = fig.update_layout(
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

# Add all the categories in the background

kwargs = {
    'global' : {
        'line' : {
            'color' : colour_bg,
            'width' : linewidth_bg}
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
            'line' : {'color' : colour_toutes, 'width' : linewidth_main}
        },
        {
            'name' :  ("Moyennes de toutes les revues qui ne sont pas"
                       " des revues spécialisées dans les études de genre"),
            'line' : {'color' : colour_toutes_sauf_genre,
                      'width' : linewidth_main}
        },
        {
            'name' : "Revues spécialisées dans les études de genre",
            'line' : {'color' : colour_main, 'width' : linewidth_main}
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
                'width' : linewidth_main
            }
        },
        {
            'line' : {
                'color' : colour_main,
                'width' : linewidth_main
            },
            'fill' : 'tonexty',
            'fillcolor' : dfPlotRA['testing_fill']
        }

    ]
}

# Science Politique - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig = fig.update_layout(dict(
    yaxis2 = yaxis_theme,
    xaxis2 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Science politique"],
                      row = 2, col = 1, 
                      **kwargs_subplots)

# Sociologie - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig = fig.update_layout(dict(
    yaxis2 = yaxis_theme,
    xaxis2 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Sociologie"],
                      row = 3, col = 1, 
                      **kwargs_subplots)

# Anthropologie -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig = fig.update_layout(dict(
    yaxis3 = yaxis_theme,
    xaxis3 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Anthropologie"],
                      row = 4, col = 1, 
                      **kwargs_subplots)

# Histoire - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig = fig.update_layout(dict(
    yaxis4 = yaxis_theme,
    xaxis4 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Histoire"],
                      row = 5, col = 1, 
                      **kwargs_subplots)

# Démographie - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig = fig.update_layout(dict(
    yaxis5 = yaxis_theme,
    xaxis5 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Démographie"],
                      row = 6, col = 1, 
                      **kwargs_subplots)

# Economie - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - 
fig = fig.update_layout(dict(
    yaxis6 = yaxis_theme,
    xaxis6 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Economie"],
                      row = 7, col = 1, 
                      **kwargs_subplots)

# SIC - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig = fig.update_layout(dict(
    yaxis7 = yaxis_theme,
    xaxis7 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "SIC"],
                      row = 8, col = 1, 
                      **kwargs_subplots)

# Géographie - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig = fig.update_layout(dict(
    yaxis9 = yaxis_theme,
    xaxis9 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Géographie"],
                      row = 9, col = 1, 
                      **kwargs_subplots)

# Aréales - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
fig = fig.update_layout(dict(
    yaxis10 = yaxis_theme,
    xaxis10 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Aréale"],
                      row = 10, col = 1, 
                      **kwargs_subplots)

# Autre interdisciplinaire - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig = fig.update_layout(dict(
    yaxis11 = yaxis_theme,
    xaxis11 = xaxis_theme
))

add_traces_to_subplot(fig, dfPlotRA, x = "annee",
                      columns = ["Toutes", "Autre interdisciplinaire"],
                      row = 11, col = 1, 
                      **kwargs_subplots)

# Save the fig ------------------------------------------------------------------
fig.write_image('fig_test.png')
