import networkx as nx


def calculate_hamming_distance(og_graph: nx.Graph, recovered_graph: nx.Graph):
    # Cache total node counts
    n_og = og_graph.number_of_nodes()
    n_rec = recovered_graph.number_of_nodes()

    # Construct adjacency matrices
    og_adj = [[0 for _ in range(n_og)] for _ in range(n_og)]
    for u, v in og_graph.edges:
        og_adj[u][v] = 1
        og_adj[v][u] = 1

    rec_adj = [[0 for _ in range(n_rec)] for _ in range(n_rec)]
    for u, v in recovered_graph.edges:
        rec_adj[u][v] = 1
        rec_adj[v][u] = 1

    # PRINT ADJACENCY MATRICES
    # for row in og_adj: print(row)
    # print()
    # for row in rec_adj: print(row)

    # Calculate hamming distance (total differences from two adjacency matrices)
    hamming_distance = 0
    for i in range(n_og):
        for j in range(i, n_og):
            if og_adj[i][j] != rec_adj[i][j]:
                hamming_distance += 1

    # return hamming distance
    return hamming_distance
