import cvxpy as cp
import numpy as np
import networkx as nx

n = 20  # number of nodes
edges = [(i, j) for i in range(n) for j in range(n) if i != j]
edge_indices = {e: k for k, e in enumerate(edges)}
x = cp.Variable(len(edges))

# Example cascade constraints: list of (source, target) pairs and times
cascades = [
    {
        0: 0,
        1: 1, 2: 1,
        3: 2, 4: 2, 5: 2, 6: 2,
        7: 3, 8: 3, 9: 3, 10: 3,
        11: 4, 12: 4, 13: 4, 14: 4,
        15: 5, 16: 5, 17: 5, 18: 5,
        19: 6
    },
    {
        9: 0,
        5: 1, 13: 1,
        2: 2, 14: 2,
        0: 3, 6: 3, 18: 3,
        10: 4, 17: 4, 19: 4,
        1: 5, 3: 5, 4: 5,
        7: 6, 8: 6,
        11: 7, 12: 7,
        15: 8, 16: 8
    },
    {
        12: 0,
        8: 1, 16: 1,
        4: 2, 17: 2,
        1: 3, 18: 3,
        0: 4, 19: 4,
        2: 5,
        5: 6,
        9: 7,
        13: 8,
        3: 6, 6: 6,
        7: 7,
        10: 7,
        11: 8,
        14: 8,
        15: 9
    }
]


def gpt_recover_graph(cascade_set):
    constraints = []
    for cascade in cascade_set:
        for v, t_v in cascade.items():
            if t_v == 0:    # is source node
                continue
            influencers = [u for u, t_u in cascade.items() if t_u < t_v]    # saves all previous nodes
            if influencers:
                infl_indices = [edge_indices[(u, v)] for u in influencers]
                constraints.append(cp.sum([x[i] for i in infl_indices]) >= 1)

    constraints += [x >= 0, x <= 1]

    # Objective: minimize number of edges
    objective = cp.Minimize(cp.sum(x))

    # Solve LP
    prob = cp.Problem(objective, constraints)
    prob.solve()

    # Randomized rounding
    x_vals = x.value
    graph_edges = [e for e, i in edge_indices.items() if np.random.rand() < x_vals[i]]

    rec_graph = nx.Graph()
    rec_graph.add_edges_from(graph_edges)

    return rec_graph
