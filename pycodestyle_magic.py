"""
magic function that checks a cell for pep8 compliance, using pycodestyle
%pycodestyle_on
or flake8
%flake8_on
a=1
should give an error about missing spaces
"""

__version__ = '0.5'

import sys
import tempfile
import io
import os
import logging
import copy
import pycodestyle as pycodestyle_module
from flake8.api import legacy as flake8_module
from contextlib import redirect_stdout

from IPython.core.magic import register_cell_magic
from IPython.core.magic import register_line_magic
from IPython.core import magic_arguments

vw = None
init_pycodestyle = False
init_flake8 = False
ignore_codes = ['W292', 'W391', 'F401', 'F821']
ignore_codes_bak = copy.deepcopy(ignore_codes)
max_line_length = 79
max_line_length_bak = copy.deepcopy(max_line_length)


class VarWatcher(object):
    def __init__(self, ip):
        self.shell = ip
        self.last_x = None

    def auto_run_flake8(self, result):
        flake8(1, result.info.raw_cell, auto=True)
        if result.error_before_exec:
            print('Error before execution: %s' % result.error_before_exec)

    def auto_run_pycodestyle(self, result):
        pycodestyle(1, result.info.raw_cell, auto=True)
        if result.error_before_exec:
            print('Error before execution: %s' % result.error_before_exec)


logger = logging.getLogger('pycodestyle')
if not logging.root.hasHandlers():
    handler = logging.StreamHandler(stream=sys.stderr)
    # format = '%(lineno)d: %(msg)s'
    # handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)


def load_ipython_extension(ip, pck=False):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    if pck == False:
        global vw
        vw = VarWatcher(ip)
    if pck == 'flake8':
        ip.events.register('post_run_cell', vw.auto_run_flake8) 
    if pck == 'pycodestyle':
        ip.events.register('post_run_cell', vw.auto_run_pycodestyle)         
    pass


def unload_ipython_extension(ip, pck=False):
    # If you want your extension to be unloadable, put that logic here.
    if pck == 'flake8':
        ip.events.unregister('post_run_cell', vw.auto_run_flake8)
        global init_flake8
        init_flake8 = False
    if pck == 'pycodestyle':
        ip.events.unregister('post_run_cell', vw.auto_run_pycodestyle)
        global init_pycodestyle
        init_pycodestyle = False
    pass

@magic_arguments.magic_arguments()
@magic_arguments.argument('--ignore','-i', help='ignore option, comma separated errors')
@magic_arguments.argument('--max_line_length','-m', help='set the max line length')
@register_line_magic
def flake8_on(line):
    """
    Flake8 magic function

    Parameters
    ----------
    --ignore, -i: errors
        Single error to ignore or comma separeted for multiple (no spaces)
        Example:  %flake8_on --ignore E265,E255
    --max_line_length, -m: int
        Maximal line length (default to 79)
        Example: %flake8_on --max_line_length 119
    """

    # validate for any options
    args = magic_arguments.parse_argstring(flake8_on, line)
    # check ignore codes
    global ignore_codes
    global ignore_codes_bak  
    ignore_codes = ignore_codes_bak  
    if args.ignore:
        ignore_codes = list(set(ignore_codes + args.ignore.split(',')))

    # check max-line-length
    global max_line_length
    global max_line_length_bak  
    max_line_length = max_line_length_bak
    if args.max_line_length:
        max_line_length = int(args.max_line_length)

    # validate if function is already active, if so, do not register new `post_run_cell`
    global init_flake8
    if init_flake8 == False:
        init_flake8 = True
    else:
        return          
    
    load_ipython_extension(vw.shell, pck='flake8')
    
@register_line_magic
def pycodestyle_on(line):
    load_ipython_extension(vw.shell, pck='pycodestyle')    
    
@register_line_magic
def flake8_off(line):
    unload_ipython_extension(vw.shell, pck='flake8')
    
@register_line_magic
def pycodestyle_off(line):
    unload_ipython_extension(vw.shell, pck='pycodestyle') 
    
@register_cell_magic
def pycodestyle(line, cell, auto=False):
    """pycodestyle cell magic for pep8"""
    global init_pycodestyle
    if init_pycodestyle == False:
        init_pycodestyle = True
        return    
        
    logger.setLevel(logging.INFO)
    # output is written to stdout
    # remember and replace
    old_stdout = sys.stdout
    # temporary replace
    sys.stdout = io.StringIO()
    # store code in a file, todo unicode
    if cell.startswith(('!', '%%', '%')):
        return    
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
        #logger.info(line)     
        # on windows drive path also contains :
        line, col, error = line.split(':')[-4:] 
        # do not subtract 1 for line for %%pycodestyle, inc pre py3.6 string
        if auto:
            add = -1
        else:
            add = 0
        logger.info('{}:{}:{}'.format(int(line) + add, col, error))         
    # restore
    sys.stdout = old_stdout
    try:
        os.remove(f.name)
    except OSError as e:  ## if failed, report it back to the user ##
        logger.error("Error: %s - %s." % (e.filename,e.strerror))
    return

@register_cell_magic
def flake8(line, cell, auto=False):
    """flake8 cell magic"""

    global init_flake8
    if init_flake8 == False:
        init_flake8 = True
        return

    logger.setLevel(logging.INFO)
    if cell.startswith(('!', '%%', '%')):
        return
    with tempfile.NamedTemporaryFile(mode='r+', delete=False) as f:
        # save to file
        f.write(cell)
        # make sure it's written
        f.flush()
        f.close()
   
    global ignore_codes    
    global max_line_length
    flake = flake8_module.get_style_guide(
        extend_ignore=ignore_codes, 
        max_line_length=max_line_length
    )
  
    
    with io.StringIO() as buf, redirect_stdout(buf):
        _ = flake.check_files([f.name])
        for line in buf.getvalue().splitlines():
            # on windows drive path also contains :
            temp_file, line, col, error = line.split(':')[-4:] 
            # only add + 1 for line for %%flake8, inc pre py3.6 string
            if auto:
                add = 0
            else:
                add = 1
            logger.info('{}:{}:{}'.format(int(line) + add, col, error))  

    return

