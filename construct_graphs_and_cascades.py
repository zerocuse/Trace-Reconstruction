import networkx as nx
from testing import test
from simulation import simulate

# BIPARTITE GRAPH
bipartite_graph = nx.Graph()
bipartite_edges = [
    (0, 10), (0, 11),
    (1, 10), (1, 12),
    (2, 12), (2, 13),
    (3, 11), (3, 14),
    (4, 14), (4, 15),
    (5, 15), (5, 16),
    (6, 13), (6, 17),
    (7, 16), (7, 18),
    (8, 17), (8, 19),
    (9, 18), (9, 19)
]

bipartite_graph.add_edges_from(bipartite_edges)
bipartite_cascades = [
    {
        0: 0,
        10: 1, 11: 1,
        1: 2, 3: 2,
        12: 3, 14: 3,
        2: 4, 4: 4
    },
    {
        5: 0,
        15: 1, 16: 1,
        4: 2, 7: 2,
        14: 3, 18: 3,
        3: 4, 9: 4
    },
    {
        6: 0,
        13: 1, 17: 1,
        2: 2, 8: 2,
        12: 3, 19: 3,
        1: 4
    }
]

test(bipartite_graph, bipartite_cascades)
simulate(bipartite_graph, bipartite_cascades, 50)

# 100 NODE GRAPH


# CYCLE GRAPH
cycle_graph = nx.cycle_graph(20)
cycle_cascades = [
    {
        0: 0,
        1: 1, 19: 1,
        2: 2, 18: 2,
        3: 3, 17: 3,
        4: 4, 16: 4,
        5: 5, 15: 5,
        6: 6, 14: 6,
        7: 7, 13: 7,
        8: 8, 12: 8,
        9: 9, 11: 9,
        10: 10
    },
    {
        5: 0,
        4: 1, 6: 1,
        3: 2, 7: 2,
        2: 3, 8: 3,
        1: 4, 9: 4,
        0: 5, 10: 5,
        19: 6, 11: 6,
        18: 7, 12: 7,
        17: 8, 13: 8,
        16: 9, 14: 9,
        15: 10
    },
    {
        10: 0,
        9: 1, 11: 1,
        8: 2, 12: 2,
        7: 3, 13: 3,
        6: 4, 14: 4,
        5: 5, 15: 5,
        4: 6, 16: 6,
        3: 7, 17: 7,
        2: 8, 18: 8,
        1: 9, 19: 9,
        0: 10
    }
]

test(cycle_graph, cycle_cascades)
simulate(cycle_graph, cycle_cascades, 50)

# TREE
tree = nx.Graph()
tree_edges = [
    (0, 1), (0, 2),          # Root connects to two children
    (1, 3), (1, 4),          # Children of node 1
    (2, 5), (2, 6),          # Children of node 2
    (3, 7), (3, 8),          # Children of node 3
    (4, 9), (4, 10),         # Children of node 4
    (5, 11), (5, 12),        # Children of node 5
    (6, 13), (6, 14),        # Children of node 6
    (7, 15),                 # Child of node 7
    (9, 16), (9, 17),        # Children of node 9
    (14, 18), (14, 19)       # Children of node 14
]
tree.add_edges_from(tree_edges)
tree_cascades = [
    {
        0: 0,
        1: 1, 2: 1,
        3: 2, 4: 2, 5: 2, 6: 2,
        7: 3, 8: 3, 9: 3, 10: 3, 11: 3, 12: 3, 13: 3, 14: 3,
        15: 4, 16: 4, 17: 4, 18: 4, 19: 4
    },
    {
        9: 0,
        4: 1, 16: 1, 17: 1,
        1: 2, 10: 2,
        0: 3, 3: 3,
        7: 4, 8: 4,
        15: 5
    },
    {
        14: 0,
        6: 1, 18: 1, 19: 1,
        2: 2,
        0: 3,
        1: 4,
        3: 5,
        7: 6
    }
]

test(tree, tree_cascades)
simulate(tree, tree_cascades, 50)
