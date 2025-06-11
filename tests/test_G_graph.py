import unittest
import sys
import os

# Add the src directory to the Python path to allow importing G_graph
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from G_graph import Graph

class TestGraph(unittest.TestCase):

    def test_add_node(self):
        g = Graph()
        g.add_node('A')
        self.assertIn('A', g.nodes())
        g.add_nodes_from(['B', 'C'])
        self.assertIn('B', g.nodes())
        self.assertIn('C', g.nodes())
        self.assertEqual(len(g.nodes()), 3)

    def test_add_edge(self):
        g = Graph()
        g.add_edge('A', 'B')
        self.assertIn('A', g.nodes())
        self.assertIn('B', g.nodes())
        self.assertTrue(('A', 'B') in g.edges() or ('B', 'A') in g.edges())                                          # and order might matter or be consistent
        self.assertTrue(g.has_edge('A', 'B'))
        self.assertTrue(g.has_edge('B', 'A')) # For undirected graph

    def test_remove_edge(self):
        g = Graph()
        g.add_edges_from([('A', 'B'), ('B', 'C')])
        g.remove_edge('A', 'B')
        self.assertNotIn(('A', 'B'), g.edges())
        self.assertFalse(g.has_edge('A', 'B'))
        self.assertIn(('B', 'C'), g.edges())
        g.remove_edge_from([('B','C')])
        self.assertFalse(g.has_edge('B', 'C'))


    def test_nodes(self):
        g = Graph()
        nodes_to_add = ['X', 'Y', 'Z']
        g.add_nodes_from(nodes_to_add)
        self.assertCountEqual(g.nodes(), nodes_to_add) # Use assertCountEqual for lists where order doesn't matter

    def test_edges(self):
        g = Graph()
        edges_to_add = [('A', 'B'), ('B', 'C'), ('C', 'A')]
        g.add_edges_from(edges_to_add)
        # Normalize edges to compare (e.g., sort tuples) because order in tuple might vary
        normalized_added_edges = [tuple(sorted(edge)) for edge in edges_to_add]
        normalized_graph_edges = [tuple(sorted(edge)) for edge in g.edges()]
        self.assertCountEqual(normalized_graph_edges, normalized_added_edges)

    def test_neighbors(self):
        g = Graph()
        g.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D')])
        self.assertCountEqual(g.neighbors('A'), ['B', 'C'])
        self.assertCountEqual(g.neighbors('B'), ['A', 'D'])
        self.assertCountEqual(g.neighbors('C'), ['A'])
        self.assertCountEqual(g.neighbors('D'), ['B'])

    def test_has_edge(self):
        g = Graph()
        g.add_edge('P', 'Q')
        self.assertTrue(g.has_edge('P', 'Q'))
        self.assertTrue(g.has_edge('Q', 'P')) # Assuming undirected
        self.assertFalse(g.has_edge('P', 'R'))

    def test_degree(self):
        g = Graph()
        g.add_edges_from([('N1', 'N2'), ('N1', 'N3'), ('N1', 'N4')])
        degrees = dict(g.degree())
        self.assertEqual(degrees.get('N1'), 3)
        self.assertEqual(degrees.get('N2'), 1)
        self.assertEqual(degrees.get('N3'), 1)
        self.assertEqual(degrees.get('N4'), 1)
        g.add_edge('N2','N3')
        degrees_updated = dict(g.degree())
        self.assertEqual(degrees_updated.get('N1'), 3)
        self.assertEqual(degrees_updated.get('N2'), 2)
        self.assertEqual(degrees_updated.get('N3'), 2)


    def test_shortest_path_length(self):
        # This test requires networkx to be installed and G_graph.py to handle it
        g = Graph()
        g.add_edges_from([('A', 'B'), ('B', 'C'), ('A', 'D'), ('D', 'C'), ('C','E')])
        # A-B-C (length 2) vs A-D-C (length 2)
        self.assertEqual(g.shortest_path_length('A', 'C'), 2)
        # A-B-C-E (length 3) vs A-D-C-E (length 3)
        self.assertEqual(g.shortest_path_length('A', 'E'), 3)
        # B-C-E (length 2)
        self.assertEqual(g.shortest_path_length('B', 'E'), 2)
        # Test for non-existent path, assuming it raises an exception or returns a specific value
        # For now, let's assume networkx.NetworkXNoPath is raised or similar.
        # The current G_graph.py implementation of shortest_path_length doesn't specify error handling for no path.
        # If networkx is not found or a path doesn't exist, it might raise an error.
        # This part might need adjustment based on actual behavior of G_graph.py or networkx.
        with self.assertRaises(Exception): # Generic exception, refine if specific one is known (e.g., nx.NetworkXNoPath)
            g.shortest_path_length('A', 'F') # F is not in the graph

if __name__ == '__main__':
    unittest.main()
