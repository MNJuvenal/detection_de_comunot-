


class Graph:
    def __init__(self):
        self.graph = {}
    
    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
    
    def add_nodes_from(self, nodes):
        for node in nodes:
            self.add_node(node)
            
    def add_edges_from(self, edges):
        for edge in edges:
            self.add_edge(edge[0], edge[1])
            
    def degree(self):
        return {(node ,len(neighbors))for node, neighbors in self.graph.items()}
    
    
    
    def complete_graph(self, nodes):
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                self.add_edge(nodes[i], nodes[j])
        return self.graph
    
    def remove_edge(self, node1, node2):
        if node2 in self.graph[node1] and node1 in self.graph[node2]:
            self.graph[node1].remove(node2)
            self.graph[node2].remove(node1) 
                
    def remove_edge_from(self,edges):
        for edge in edges:
            self.remove_edge(edge[0], edge[1])
    def nodes(self):
        return list(self.graph.keys())
    
    def edges(self):
        edges = []
        for node in self.graph:
            for neighbor in self.graph[node]:
                if ((neighbor, node) or (node,neighbor) )not in edges:
                    edges.append((node, neighbor))
        return edges

    def add_edge(self, node1, node2):
        if node2 not in self.graph:
            self.add_node(node2)
        if node1 not in self.graph:
            self.add_node(node1)
            
        if (node2 not in self.graph[node1]) and (node1 not in self.graph[node2]):
            self.graph[node1].append(node2)
            self.graph[node2].append(node1)
        
     
    def neighbors(self, node):
        return self.graph[node]
    
    def has_edge(self, node1, node2):
        return node2 in self.graph[node1]
    
    def draw(self):
        import matplotlib.pyplot as plt
        import networkx as nx
        G = nx.Graph()
        G.add_nodes_from(self.nodes())
        G.add_edges_from(self.edges())
        nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=15)
        plt.show()
        
    def shortest_path_length(self, source, target):
        import networkx as nx
        G = nx.Graph()
        G.add_nodes_from(self.nodes())
        G.add_edges_from(self.edges())
        return nx.shortest_path_length(G, source, target)
    def from_pandas_edgelist(df,source='source',target='target'):
        import pandas as pd
        
        G = Graph()
        edges = df[[source, target]].values
        G.add_edges_from(edges)
        return G

    def __str__(self):
        return str(self.graph)