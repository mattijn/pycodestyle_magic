"""
magic function that checks a cell for pep8 compliance, using pycodestyle
%%pycodestyle
a=1
should give an error about missing spaces
"""

__version__ = '0.1'

import sys
import tempfile
import io
import os
import logging
import pycodestyle as pycodestyle_module


from IPython.core.magic import register_cell_magic


logger = logging.getLogger('pycodestyle')
if not logging.root.hasHandlers():
    handler = logging.StreamHandler(stream=sys.stderr)
    # format = '%(lineno)d: %(msg)s'
    # handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)


def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    pass


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass


@register_cell_magic
def pycodestyle(line, cell):
    """pycodestyle cell magic for pep8"""

    logger.setLevel(logging.INFO)
    # output is written to stdout
    # remember and replace
    old_stdout = sys.stdout
    # temporary replace
    sys.stdout = io.StringIO()
    # store code in a file, todo unicode
    with tempfile.NamedTemporaryFile(mode='r+',delete=False) as f:
        # save to file
        f.write('# The %%pycodestyle cell magic was here\n' + cell + '\n')
        # make sure it's written
        f.flush()
        f.close()
    # now we can check the file by name.
    # we might be able to use 'stdin', have to check implementation
    format = '%(row)d:%(col)d: %(code)s %(text)s'
    pycodestyle = pycodestyle_module.StyleGuide(format=format)
    # check the filename
    pcs_result = pycodestyle.check_files(paths=[f.name])
    # split lines
    stdout = sys.stdout.getvalue().splitlines()    
    for line in stdout:
        logger.info(line)
    # restore
    sys.stdout = old_stdout
    try:
        os.remove(f.name)
    except OSError as e:  ## if failed, report it back to the user ##
        logger.error("Error: %s - %s." % (e.filename,e.strerror))
    return
