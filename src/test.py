import G_graph as nx2
import os
import random
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import multiprocessing
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time







def generer_random_G(n, p, nb_G):
    """
    Génère une liste de graphes aléatoires utilisant
    Parameters:
    n (int): Le nombre de nœuds dans chaque graphe.
    p (float): La probabilité pour chaque paire de nœuds d'être connectée par une arête.
    nb_G (int): Le nombre de graphes à générer.
    Returns:
    list: Une liste de graphes générés aléatoirement.
    """
    
    
    Gs = []
    for k in range(nb_G):
        G = nx2.Graph()     # initialise un graph en list d'adjence vide 
        G.add_nodes_from(range(n)) 
        for i in range(n):
            for j in range(i + 1, n):
             if random.random() < p:
                G.add_edge(i, j) 
            print(f"le noeud {i} a été généré")
        Gs.append(G)
    

    return Gs

def creer_graphe_depuis_csv(f):
    """
    Crée un graphe à partir d'un fichier CSV.

    Args:
        f (str): Le chemin vers le fichier CSV contenant les données du graphe.

    Returns:
        .Graph: Un graphe créé à partir des données du fichier.
    """
    
    df = pd.read_csv(f)
    G = nx2.Graph()
    G.add_edges_from(df.values)
    
    return G
   
    
    


def creer_graphe_depuis_fichier(fichier):
    """
    Crée un graphe à partir d'un fichier.

    Args:
        fichier (str): Le chemin vers le fichier contenant les données du graphe.

    Returns:
        .Graph: Un graphe  créé à partir des données du fichier a noter que le graphe est stocker en liste d'adjacence.
    """ 
    G = nx2.Graph()
    with open(fichier, 'r') as f:
        for line in f:
            source, target = line.strip().split(' ')  
            G.add_edge(source, target)
    return G 



def histo_G(Gs):
    """
    Trace des histogrammes des degrés des nœuds pour une liste de graphes.

    Paramètres:
    Gs (list): Une liste d'objets graphe NetworkX. Chaque graphe doit avoir un attribut 'name' dans son dictionnaire de graphes.

    La fonction effectue les étapes suivantes pour chaque graphe de la liste :
    1. Calcule le degré de chaque nœud dans le graphe.
    2. Trace un histogramme des degrés des nœuds.
    3. Étiquette l'axe des x comme "Degré" et l'axe des y comme "Nombre de nœuds".
    4. Ajoute une légende avec le nom du graphe.
    5. Annoter l'histogramme avec le degré maximum et le nombre de chemins induits.

    Remarque:
    - La fonction suppose que les objets graphe ont un attribut 'name' dans leur dictionnaire de graphes.
    - La fonction utilise matplotlib pour le traçage et NetworkX pour les opérations sur les graphes.
    - La fonction appelle une fonction externe `nb_chemins_induits_` pour calculer le nombre de chemins induits dans le graphe.

    """
    count=1
    for i in Gs :
        degrees =[d for n, d in i.degree()]
        plt.hist(degrees, label='Graphe '+str(count)) 
        count+=1
        plt.xlabel("Degré")
        plt.ylabel("Nombre de nœuds")
        plt.legend()
        d = max((dict(i.degree())).values())
        c = nb_chemins_induits(i)
        plt.annotate('Degré Max', xy=(d, 0.2), xytext=(d, 0.5),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 horizontalalignment='right', verticalalignment='top')
        plt.text( d/2,2 , 'Nb Chemins Induits: '+str(c), ha='center', va='bottom', fontsize=10, color='red')
        plt.show()
        
        
def histo_f(dossier):
    
        for i in nom_fichiers(dossier):
            G=creer_graphe_depuis_fichier(dossier+"/"+i)
            degrees = [d for n, d in G.degree()]
            plt.hist(degrees, label='Graphe ' + i) 
            plt.xlabel("Degré")
            plt.ylabel("Nombre de nœuds")
            plt.legend()
            d = max((dict(G.degree())).values())
            c = nb_chemins_induits(G)
            plt.annotate('Degré Max'+str(d), xy=(d,0.1), xytext=(d, 0.5),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 horizontalalignment='center', verticalalignment='bottom')
            plt.text( d/2,2 , 'Nb Chemins Induits: '+str(c), ha='center', va='bottom', fontsize=10, color='red')
            plt.show()
def histo_csv(f):
        
        G=creer_graphe_depuis_csv(f)
        degrees = [d for n, d in G.degree()]
        plt.hist(degrees, label='Graphe ' + f) 
        plt.xlabel("Degré")
        plt.ylabel("Nombre de nœuds")
        plt.legend()
        d = max((dict(G.degree())).values())
        c = nb_chemins_induits(G)
        plt.annotate('Degré Max'+str(d), xy=(d,0.1), xytext=(d, 0.5),
                    arrowprops=dict(facecolor='red', shrink=0.05),
                    horizontalalignment='center', verticalalignment='bottom')
        plt.text( d/2,2 , 'Nb Chemins Induits: '+str(c), ha='center', va='bottom', fontsize=10, color='red')
        plt.show()


def nom_fichiers(dossier):
    L_f = []
    for f in os.listdir(dossier):
        if os.path.isfile(os.path.join(dossier, f)):
             L_f.append(f)
    return L_f


def nb_chemins_induits(G):
    """
    Calcule le nombre de chemins induits de longueur 2 dans un graphe.

    Args:
        G (Graph): Un objet de type Graph représentant le graphe.

    Returns:
        int: Le nombre de chemins induits de longueur 2.
    """

    count = 0
    for node in G.nodes():
        neighbors = G.neighbors(node) # Récupérer les voisins du nœud
        for i in range(len(neighbors)):
            neighbor1 = list(neighbors)[i]
            for j in  G.neighbors(neighbor1):
                # Vérifier si le chemin n'a pas déjà été compt
                if not (G.has_edge(node, j) and  G.has_edge(j, node))  and (node < neighbor1) and (node!=j) and (node < j) :
                # On vérifie que le chemin n'a pas déjà été compté en partant de neighbor1
                    count += 1
                    print("chemin induit trouvé:", node, neighbor1, j)

    return count



def bron_kerbosch(R, P, X, graph, Liste_cliques_maximale=None):
    if Liste_cliques_maximale is None:
        Liste_cliques_maximale = []
    if not P and not X:
        print("clique maximale trouvée:", R)
        Liste_cliques_maximale.append(R)
    for v in list(P):
        bron_kerbosch(R.union([v]), P.intersection(set(graph.neighbors(v))), X.intersection(set(graph.neighbors(v))), graph, Liste_cliques_maximale)
        P.remove(v)
        X.add(v)
    return Liste_cliques_maximale





def bron_kerbosch_parallel(graph):
    # Partitionner les sommets
    num_processes=multiprocessing.cpu_count()   
    num_nodes = len(graph.nodes())
    nodes_list = list(graph.nodes())  # Convertir les nœuds en liste pour permettre l'indexation
    partitions = [set(nodes_list[i:i + num_nodes // num_processes]) for i in range(0, num_nodes, num_nodes // num_processes)]
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(bron_kerbosch, [(set(), partition, set(), graph) for partition in partitions])

    # Fusionner les résultats
    Liste_cliques_maximale = []
    for result in results:
        Liste_cliques_maximale.extend(result)

    return Liste_cliques_maximale


def enumération_cliques(Gs):
    
    for i, graph in enumerate(Gs):
        
        print(f"Graphe {i+1}: {graph}")
        res=bron_kerbosch(set(), set(graph.nodes()), set(), graph)
        res=bron_kerbosch_parallel(graph)
        
    print("les cliques maximales sont:", res)


def voir_les_sortie_dans_unfichier_txt():
    

    with open('output.txt', 'w') as f:
        subprocess.call(['/bin/python', '/home/juvenal/Téléchargements/prjt_OCA/prjt_oca/src/test.py'], stdout=f)


def complement_graph(G):
    nodes = G.nodes()
    C_G=nx2.Graph()
    C_G.complete_graph(nodes)
    C_G.remove_edge_from(G.edges())
    
    return C_G


def independant_maximal_G(G):
    
    cliiques_maximal_G=[]
    C_G = complement_graph(G)
    cliiques_maximal_G== bron_kerbosch(set(), set(C_G.nodes()), set(), C_G, cliiques_maximal_G)
    
    print("les indépendants  maximaux sont:", cliiques_maximal_G)



histo_f("data")    #decommenter cette ligne pour voir l'histogramme des graphes dans le dossier prjt_oca
#Gs=generer_random_G(100, 0.4, 1)

#histo_G(Gs)            #decommenter cette ligne pour voir l'histogramme des graphes générés aléatoirement
histo_csv("graphe_no_LASN.csv")  #decommenter cette ligne pour voir l'histogramme du graphe graphe_no_LASN.csv


