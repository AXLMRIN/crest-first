# TLDR
Working on datavisualisation with Plotly (v5.24.1) focusing _- for now -_ on static yet interactive graphs.
# What will you find ?
As you would expect with such a self explenatory repository name. This is the first repository working on the datavisualisation of En Mode Mineur article _- upcoming link -_.
**The notebooks** are used to explore data and on the fly operations. **src** scripts are cleaner, you will find short scripts creating beautiful _ish_ figures. The **scripts** rely on 2 folders : 
- **plotlyThemes** is where we store `.json` files used to customise the plots with general preset (`xaxis.json`) and customisations for one graph (`figure2_menus`). This means creatting many short files rather than one big file. 
- **package**, is a custom package used in the scripts. You will find data loaders, trace updaters and so on - the perfect toolbox.
For now there are no data manipulation scripts - upcoming ? - .
_data are not saved in the repository. All data should be placed in a **data** folder at the root._

# How to run the scripts
I am working from the terminal, this means thata  all the path look like `scripts/src/plotlyThemes/xxx` or `data/xxx` rather than `../plotlyThemes/xxx` or `../../data/xxx`.
Ultimately you want to run : `python scripts/src/figure2_plotting.py`

# Requirements : 
Big picture : 
- `plotly` (v5.24.1)
- `pandas` (v2.2.2)
- `numpy` (v1.26.4)
