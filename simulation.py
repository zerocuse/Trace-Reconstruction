from solution import recover_graph
from gptSolution import gpt_recover_graph
import networkx as nx

original_graph = nx.Graph()
edges = []
original_graph.add_edges_from(edges)


def simulate(graph, cascades):

    n = graph.number_of_nodes()
    recovered_edges = {(i, j): 0 for i in range(n) for j in range(n) if i != j}

    for _ in range(100):
        rec_graph = recover_graph(cascade_set=cascades)
        for edge in rec_graph.edges:
            recovered_edges[edge] += 1

    has_different_edges = False
    compare_value = None
    for edge, count in recovered_edges.items():
        if count != 0:
            if compare_value and count != compare_value:
                has_different_edges = True
                break
            elif not compare_value:
                compare_value = count

    print(recovered_edges)
    print(has_different_edges)


# Construct Graph
graph = nx.Graph()
graph_edges = [
    (0, 1), (0, 2),
    (1, 3), (1, 4),
    (2, 5),
    (3, 6),
    (4, 6), (4, 7),
    (5, 7), (5, 8),
    (6, 9),
    (7, 9), (7, 10),
    (8, 10),
    (9, 11),
    (10, 11)
]
graph.add_edges_from(graph_edges)

# Construct Cascades from Original Graph
cascades = [
    {
        0: 0,
        1: 1, 2: 1,
        3: 2, 4: 2, 5: 2,
        6: 3, 7: 3, 8: 3,
        9: 4, 10: 4,
        11: 5
    },
    {
        2: 0,
        5: 1,
        7: 2, 8: 2,
        9: 3, 10: 3,
        11: 4
    },
    {
        5: 0,
        7: 1, 8: 1,
        10: 2,
        11: 3
    },
    {
        1: 0,
        3: 1, 4: 1,
        6: 2, 7: 2,
        9: 3, 10: 3,
        11: 4
    },
    {
        4: 0,
        6: 1, 7: 1,
        9: 2, 10: 2,
        11: 3
    },
    {
        8: 0,
        10: 1,
        11: 2
    }
]

simulate(graph, cascades)
