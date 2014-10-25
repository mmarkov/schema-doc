__author__ = 'maksymmarkov'

import unittest
import pygraphviz
# from unittest.mock import patch

class GraphTestCase(unittest.TestCase):

    def test_graph(self):
        str = """
            digraph G {
                node [shape=plaintext]
                [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                <TR><TD></TD></TR></TABLE>>];
            }
        """
        d = pygraphviz.AGraph(string=str)
        data = d.draw(prog='dot', format='svg')
        self.assertTrue(data.startswith(b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1'))




if __name__ == '__main__':
    unittest.main()
