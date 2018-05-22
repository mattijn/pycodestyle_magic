"""
Run under IPython with `ipython tests/test_.*py`.

The unittest discovery with `python -m unittest discover -s tests`, or what I imagine to be the IPython version `ipython -m unittest discover -s tests` is not working, for some reason, and is complaining about `get_ipython()` not being in the context.
"""
import unittest
import logging
from pycodestyle_magic import pycodestyle

class TestLinenumbers(unittest.TestCase):
    """Setup the tests, we want a logger."""
    def setUp(self):
        self.logger = logging.getLogger('pycodestyle')
        self.logger.setLevel(logging.INFO)
        self.level = 'INFO'
        self.cellmagic = "%%pycodestyle"
        
    def test_pycodestyle_reports_correct_linenumber(self):
        """Test that pycodestyle reports correct line numbers, and
        accommodates for the cell magic at the top of the cell which is takes
        one line.
        """
        cell = '''print( "oh look kittens!" )'''
        # with self.assertLogs('pycodestyle', level='INFO') as cm:
        with self.assertLogs(self.logger) as cm:
            pycodestyle(None, cell)
            self.assertEqual(cm.output,
                             [f"{self.level}:{self.logger.name}:2:7: E201 whitespace after '('",
                              f"{self.level}:{self.logger.name}:2:26: E202 whitespace before ')'"])

    def test_pycodestyle_reports_correct_linenumber_with_leading_empty_lines(self):
        """Test that pycodestyle reports the correct line numbers when there
        are empty lines at the top of the cell, after the cell magic
        but before the actual code.
        """
        cell = '''\nprint( "oh look kittens!" )'''
        with self.assertLogs(self.logger) as cm:
            pycodestyle(None, cell)
            self.assertEqual(cm.output,
                             [f"{self.level}:{self.logger.name}:3:7: E201 whitespace after '('",
                              f"{self.level}:{self.logger.name}:3:26: E202 whitespace before ')'"])

    def test_pycodestyle_reports_three_leading_empty_lines(self):
        """Test that pycodestyle still reports if there are too many empty
        lines at the beginning of the cell.
        """
        cell = '''\n\n\nprint("this is fine")'''
        with self.assertLogs(self.logger) as cm:
            pycodestyle(None, cell)
            self.assertEqual(cm.output,
                             [f"{self.level}:{self.logger.name}:5:1: E303 too many blank lines (3)"])

# def test_pycodestyle_leading_comments_skipped_when_everything_is_fine(self):
#        """Test that leading comment lines is skipped when pycodestyle doesn't
#        report style issues.
#        """
#        cell = '''# a comment line\nprint("this is fine")'''
#        raise NotImplementedError

    def test_pycodestyle_leading_comments_skipped_when_reporting(self):
        """Test that leading comments lines are skipped when pycodestyle does
report style issues.
        """
        cell = '''# a comment line\nprint( "oh look kittens!" )'''
        with self.assertLogs(self.logger) as cm:
            pycodestyle(None, cell)
            self.assertEqual(cm.output,
                             [f"{self.level}:{self.logger.name}:3:7: E201 whitespace after '('",
                              f"{self.level}:{self.logger.name}:3:26: E202 whitespace before ')'"])

if __name__ == '__main__':
    unittest.main()
