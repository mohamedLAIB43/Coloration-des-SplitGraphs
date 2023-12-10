import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def scinde(graphe):
    n = len(graphe)
    degres = np.sum(graphe, axis=0) - 1
    sommets_tries = np.argsort(-degres)

    clique = set()
    ensemble_independant = set(range(n))

    for sommet in sommets_tries:
        if all(graphe[sommet, voisin] == 1 for voisin in clique):
            clique.add(sommet)
            ensemble_independant.remove(sommet)

    for u in ensemble_independant:
        for v in ensemble_independant:
            if u != v and graphe[u, v] == 1:
                return False

    return True

def welsh_powell(graphe):
    n = len(graphe)
    couleurs = [-1] * n
    degres = [sum(ligne) for ligne in graphe]
    sommets = sorted(range(n), key=lambda x: degres[x], reverse=True)

    for sommet in sommets:
        if couleurs[sommet] == -1:
            # Obtenir les couleurs des voisins
            couleurs_voisins = set(couleurs[j] for j in range(n) if graphe[sommet][j] == 1 and couleurs[j] != -1)

            # Trouver la première couleur disponible
            nouvelle_couleur = 0
            while nouvelle_couleur in couleurs_voisins:
                nouvelle_couleur += 1

            couleurs[sommet] = nouvelle_couleur

    return couleurs


def trouve_clique_et_stable_max(graphe):
    n = len(graphe)

    clique = set()
    ensemble_independant = set(range(n))

    for sommet in range(n):
        if all(graphe[sommet, voisin] == 1 for voisin in clique):
            clique.add(sommet)
            ensemble_independant.remove(sommet)

    max_clique = list(clique)
    print("Clique maximale du graphe :")
    print(max_clique)

    stable = set(range(n)) - clique

    max_stable = list(stable)
    print("Ensemble stable maximal du graphe :")
    print(max_stable)

    return max_clique, max_stable

def plot_graph_with_colors(graphe, couleurs, title):
    n = len(graphe)
    G = nx.Graph()

    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(i + 1, n):
            if graphe[i, j] == 1:
                G.add_edge(i, j)

    pos = nx.spring_layout(G)

    # Convertir les couleurs en valeurs numériques pour l'affichage
    color_map = [couleurs[i] for i in range(n)]

    edge_colors = "black"

    nx.draw(G, pos, with_labels=True, font_weight="bold", node_size=700, node_color=color_map, edge_color=edge_colors, cmap=plt.cm.rainbow)
    plt.title(title)
    plt.show()

# Exemple d'utilisation
n = int(input("Entrez le nombre des sommets : n= "))
graphe = np.zeros((n, n), dtype=int)

for j in range(n):
    for i in range(j + 1):
        if i == j:
            graphe[i][j] = 1
        else:
            graphe[i][j] = int(input(f"si il y a une arette ({i + 1},{j + 1}) tapez 1 sinon tapez 0   : "))
            graphe[j][i] = graphe[i][j]

print('La matrice d\'adjacence est :')
print(graphe)

if scinde(graphe):
    print("Le graphe est scindé.")
    couleurs = welsh_powell(graphe)
    print("Coloration des sommets du graphe (Welsh-Powell) : ")
    for i in range(n):
        print(f"Sommet {i + 1} : Couleur {couleurs[i]}")
    
    max_clique, max_stable = trouve_clique_et_stable_max(graphe)
    
    # Tracer le graphe avec la coloration Welsh-Powell
    plot_graph_with_colors(graphe, couleurs, "Coloration Welsh-Powell")
else:
    print("Le graphe n'est pas scindé.")
