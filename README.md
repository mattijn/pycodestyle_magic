# pycodestyle_magic
Magic function for pycodestyle and flake8 module in Jupyter-Lab or Notebook

# installation
Make sure you've the Python package `pycodestyle`, `flake8` and this `pycodestyle_magic`.

```
pip install flake8 pycodestyle pycodestyle_magic
```

# configuration

Flake8 and pycodestyle will discover and manage user configuration files
(stored in a user's home directory or in the XDG directory inside their home
directory) or project configuration files (stored in the current directory).
See their respective docs for specific details on configuration file naming,
syntax, and location.

Additionally, Flake8 cell magic ignores four codes by default:
  * W292 - *no newline at end of file*; not relevant in an iPython cell
  * W391 - *blank line at end of file*; not relevant in an iPython cell
  * F401 - *module imported but unused*; a module may be imported in one cell and used in another
  * F821 - *undefined name name*; a variable may be defined in one cell and used in another

# usage
Enable the magic function by using the pycodestyle_magic module in a cell

`%load_ext pycodestyle_magic`

## to check a cell once:
use the function as first line in your cell to check compliance with `pycodestyle` or `flake8` as such:

`%%pycodestyle`

or for `flake8`

`%%flake8`

## to auto check each cell (version >= 0.3):
If you want this compliance checking turned on by default for each cell then run this magic line function in an empty cell:

`%pycodestyle_on`

or for `flake8`

`%flake8_on`

You only need to call this once (observe the single `%`).

To turn off the auto-checking for each cell use:

`%pycodestyle_off` or `%flake8_off`

If you have turned `on` the function multiple times you also will have to turn it `off` the same amount of times.

See notebooks in notebook directory for example use cases, as such:
### Pycodestyle ([notebook](https://github.com/mattijn/pycodestyle_magic/blob/master/notebook/example%20pycodestyle_magic.ipynb))
![alt text](img/pycodestyle.PNG)

### Flake8 ([notebook](https://github.com/mattijn/pycodestyle_magic/blob/master/notebook/example%20flake8_magic.ipynb))
![alt text](img/flake8.PNG)

Examples notebooks were slightly adapted from
https://github.com/SiggyF/notebooks/blob/master/styleguide.ipynb
