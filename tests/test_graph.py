__author__ = 'maksymmarkov'

import unittest
import pygraphviz
import os
# from unittest.mock import patch


class GraphTestCase(unittest.TestCase):

    def tearDown(self):
        if os.path.isfile('test_diagram.svg'):
            os.remove('test_diagram.svg')

    def test_graph(self):
        digraph = """
            digraph G {
                node [shape=plaintext]
                [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                <TR><TD></TD></TR></TABLE>>];
            }
        """
        d = pygraphviz.AGraph(string=digraph)
        data = d.draw(prog='dot', format='svg')
        self.assertTrue(data.startswith(b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1'))

    def test_graph_arrows(self):
        digraph="""
            digraph G {
                graph [
                    rankdir="RL"
                    labeljust="l"
                    nodesep="0.18"
                    ranksep="0.46"
                ];
                node [
                    shape=plaintext
                ];
                edge [
                    arrowsize="0.8"
                ];
                table_a [label=<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR>
                        <TD COLSPAN="2">table_a</TD>
                    </TR>
                    <TR>
                        <TD PORT="col_a1">col_a1</TD>
                        <TD>type_col_a1</TD>
                    </TR>
                    <TR>
                        <TD PORT="col_a2">col_a2</TD>
                        <TD>type_col_a2</TD>
                    </TR>
                </TABLE>
                >];
                table_b [label=<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR>
                        <TD COLSPAN="2">table_b</TD>
                    </TR>
                    <TR>
                        <TD PORT="col_b1">col_b1</TD>
                        <TD>type_col_b1</TD>
                    </TR>
                </TABLE>
                >];

                "table_b":"col_b1"->"table_a":"col_a1"[arrowhead=normal dir=forward arrowtail=none];
            }
        """
        d = pygraphviz.AGraph(string=digraph)
        data = d.draw(prog='dot', format='svg')
        with open('test_diagram.svg', 'wb') as f:
            f.write(data)

if __name__ == '__main__':
    unittest.main()
