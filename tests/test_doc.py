__author__ = 'maksymmarkov'

import os
import shutil
import unittest
import schemadoc
from unittest.mock import patch



class ParametersTestCase(unittest.TestCase):


    @patch('sys.argv')
    @patch('optparse.OptionParser.print_help')
    @patch('builtins.print')
    @patch('schemadoc.doc._doc')
    def test_empty_parameters(self, mock__doc, mock_print, mock_print_help, mock_argv):
        def getitem(a, b, **kwargs):
            return []
        mock_argv.__getitem__ = getitem
        exit_code = schemadoc.doc.main()
        self.assertEqual(exit_code, 1, 'Calling without parameters should return exit code 1')

    @patch('sys.argv')
    @patch('optparse.OptionParser.print_help')
    @patch('builtins.print')
    @patch('schemadoc.doc._doc')
    def test_no_folder_parameters(self, mock__doc, mock_print, mock_print_help, mock_argv):
        def getitem(a,b, **kwargs):
            return ['-u sqllite://']
        mock_argv.__getitem__ = getitem
        exit_code = schemadoc.doc.main()
        mock_print_help.asser_called()
        self.assertEqual(exit_code, 1, 'output folder is required parameter')


    @patch('sys.argv')
    @patch('os.makedirs')
    @patch('optparse.OptionParser.print_help')
    @patch('builtins.print')
    @patch('schemadoc.doc._doc')
    def test_valid_folder_parameters(self, mock__doc, mock_print, mock_print_help, mock_makedirs, mock_argv):
        def getitem(a, b, **kwargs):
            return ['-o /test_test_test_folder', '-u sqllite://']
        mock_argv.__getitem__ = getitem
        # ['-o/test_test_test_folder']
        exit_code = schemadoc.doc.main()
        mock_makedirs.assert_called_with('/test_test_test_folder')
        self.assertEqual(exit_code, 0, 'If valid folder provided exit code expected 0')


if __name__ == '__main__':
    unittest.main()
