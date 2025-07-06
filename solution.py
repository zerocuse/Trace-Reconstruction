import networkx as nx
from scipy.optimize import linprog
import numpy as np


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

    res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    x_lp = res.x
    x_binary = np.random.binomial(1, x_lp)

    recovered_edges = [edges[i] for i, val in enumerate(x_binary) if val == 1]
    rec_graph = nx.Graph()
    rec_graph.add_edges_from(recovered_edges)

    return rec_graph
