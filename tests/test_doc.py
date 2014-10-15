__author__ = 'maksymmarkov'

import unittest
import schemadoc
from unittest.mock import patch



class ParametersTestCase(unittest.TestCase):

    @patch('optparse.OptionParser.print_help')
    @patch('builtins.print')
    @patch('schemadoc.doc._doc')
    def test_empty_parameters(self, mock__doc, mock_print, mock_print_help):
        exit_code = schemadoc.doc.main([])
        self.assertEqual(exit_code, 1, 'Calling without parameters should return exit code 1')

    @patch('optparse.OptionParser.print_help')
    @patch('builtins.print')
    @patch('schemadoc.doc._doc')
    def test_no_folder_parameters(self, mock__doc, mock_print, mock_print_help):
        exit_code = schemadoc.doc.main(['-slocalhost'])
        mock_print_help.asser_called()
        self.assertEqual(exit_code, 1, 'output older is required parameter')


    @patch('os.makedirs')
    @patch('optparse.OptionParser.print_help')
    @patch('builtins.print')
    @patch('schemadoc.doc._doc')
    def test_valid_folder_parameters(self, mock__doc, mock_print, mock_print_help, mock_makedirs):
        exit_code = schemadoc.doc.main(['-o/test_test_test_folder'])
        mock_makedirs.assert_called_with('/test_test_test_folder')
        self.assertEqual(exit_code, 0, 'If valid folder provided exit code expected 0')


if __name__ == '__main__':
    unittest.main()
