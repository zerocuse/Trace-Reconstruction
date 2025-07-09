import networkx as nx
from scipy.optimize import linprog
import numpy as np

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

def recover_graph(cascade_set):
    # Get the set of all nodes that appear in any cascade
    all_nodes = set()
    for cascade in cascade_set:
        all_nodes.update(cascade.keys())

    # Total number of nodes
    n = max(all_nodes) + 1

    # Create candidate edges
    edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    edges_idx = {edge: i for i, edge in enumerate(edges)}
    total_edges = len(edges)

    # NP Array of cost
    c = np.ones(total_edges)

    # Construct lin prog arrays
    A = []
    b = []
    bounds = [(0, 1) for _ in range(total_edges)]

    # Constructing A's constraint matrix
    for cascade in cascade_set:
        sorted_nodes = sorted(cascade.items(), key=lambda x: x[1])
        for node_v, time_step_v in sorted_nodes:
            if time_step_v == 0:  # skip source node
                continue

            node_constraint = np.zeros(total_edges)   # initialize constraint with no candidates
            for node_u, time_step_u in cascade.items():
                if (time_step_u < time_step_v) and ((node_u, node_v) in edges_idx):
                    node_constraint[edges_idx[(node_u, node_v)]] = -1

            A.append(node_constraint)
            b.append(-1)

    A = np.array(A)
    b = np.array(b)

    res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='interior-point')

    x_lp = res.x
    x_binary = (np.random.rand(len(x_lp)) < x_lp).astype(int)

    recovered_edges = [edges[i] for i, val in enumerate(x_binary) if val == 1]
    rec_graph = nx.Graph()
    rec_graph.add_edges_from(recovered_edges)

    return rec_graph


x = recover_graph(cascade_set=cascades)
print(x.edges)
