import G_graph as nx 
import matplotlib.pyplot as plt

def V__i(i,G):
    
    t=0
    V=[j for j in G.nodes()] # liste des noeuds du graphe G 
    for j in range(len(V)):
         if V[j]==i:
             t=j
             break
         
    return V[j:] # retourne la liste des noeuds du graphe G à partir du noeud i


def N_k_v(i, k, G):
    
    V_i=V__i(i,G) 
    N=[]
    for j in G.nodes():
        if G.shortest_path_length(source=i,target=j) == k:
            N.append(j)
    return list(set(N).intersection(V_i)) # retourne la liste des noeuds du graphe G à distance k du noeud i appartir de i

def G__i(G,i):
    
    G_i=nx.Graph()
    N1,N2=N_k_v(i,1,G),N_k_v(i,2,G)
    for j in [i] + N1 + N2:
        G_i.add_node(j)
    
        
    for j in G.edges():
        
        if j[0] in N1 and j[1] in N1:
            G_i.add_edge(j[0],j[1])
        elif j[0] in N2 and j[1] in N2:
            G_i.add_edge(j[0],j[1])
        else:
            pass
    for k in N1:  # au pire des cas c"est de delta iterations
        
        for j in N2: # au pire des cas c"est de m-delta iterations
            
            if (k,j) not in G.edges() :
                G_i.add_edge(k,j)
    
    return G_i


# Test the function G__i  ||| executer le code suivant dans un terminal pour voir les resultats        

G=nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 5), (4, 5), (1, 5), (2, 5)])
G.draw()


for i in G.nodes():
    Gs=G__i(G,i)

                    # Generate and draw the subgraph G_i for node 1
    G_sub = G__i(G, i)
    G_sub.draw()
    











