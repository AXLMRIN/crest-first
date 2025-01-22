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

# Parameters ===================================================================
gap : float = 1 # gap between traces

# Reading Data -----------------------------------------------------------------
FOLDERNAME = 'data/checkpoints/'
filename = 'kernel_for_plotly.csv'

df = pd.read_csv(FOLDERNAME + filename)
del df['Unnamed: 0']
year_set = set(df['year'])

# Create a cascade - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
2001 -> 23 * gap -->
2023 -> 0  * gap -->  -23 / (2023 - 2001) * (Y - 2023)
'''
year_max, year_min = max(year_set), min(year_set)
factor = gap * -1 * (year_max - year_min + 1) / (year_max - year_min)
df['density'] = df['density'] * (df['year'] - year_max) * factor + 1

# Creating goFigure


fig = px.line(df, x = 'x', y = 'density', color = 'year', log_y= True)

# Save Figure

fig.write_image('violin_test.png')
fig.write_html('violin_test.html')