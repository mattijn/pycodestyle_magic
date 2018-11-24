# pycodestyle_magic
magic function for pycodestyle module in jupyter notebook

Make sure you've the module pycodestyle and flake8 (`pip install pycodestyle flake8`) Then enable the magic function by using the pycodestyle_magic module

`pip install pycodestyle_magic`

first load the magic in a cell:

`%load_ext pycodestyle_magic`


and then use the function in your cell to check compliance with `pycodestyle`

`%%pycodestyle`

or  with `flake8`

`%%flake8`


Examples notebooks originate and slightly adaptad from
https://github.com/SiggyF/notebooks/blob/master/styleguide.ipynb