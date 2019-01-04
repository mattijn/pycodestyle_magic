"""
Run under IPython with `ipython tests/test_flake8_magic.py`.

The unittest discovery with `python -m unittest discover -s tests`, or what I
imagine to be the IPython version `ipython -m unittest discover -s tests` is
not working, for some reason, and is complaining about `get_ipython()` not
being in the context.
"""
import os
import unittest
import logging
from pycodestyle_magic import flake8


class TestFlake8CellMagic(unittest.TestCase):
    """Setup the tests, we want a logger."""
    def setUp(self):
        self.logger = logging.getLogger('pycodestyle')
        self.logger.setLevel(logging.INFO)
        self.level = 'INFO'
        self.cellmagic = "%%flake8"

    def test_flake8_project_configuration(self):
        """Test a flake8 project level configuration file."""
        cell = '''a=1\n'''
        path = os.path.join(os.getcwd(), '.flake8')
        with open(path, "w") as fp:
            fp.write('[flake8]\nignore = E225\n')
            fp.flush()
            self.assertFalse(flake8(None, cell))  # expect no output
        os.remove(path)

    def test_flake8_missing_whitespace_around_operator(self):
        """Test an expected error, missing whitespace around operator."""
        cell = '''a=1\n'''
        expect_msg = (f"{self.level}:{self.logger.name}:2:2: " +
                      "E225 missing whitespace around operator")
        with self.assertLogs(self.logger, self.level) as cm:
            flake8(None, cell)
            self.assertEqual(cm.output, [expect_msg])

    def test_flake8_defaults(self):
        """Test flake8 defaults: F401, F821, W292, W391"""
        cell = ('''import collections.namedtuple\n\n\n''' +
                '''def get_name():\n''' +
                '''    return name\n\n''' +
                '''    #''')
        self.assertFalse(flake8(None, cell))  # expect no output


if __name__ == '__main__':
    unittest.main()
