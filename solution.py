import networkx as nx
from scipy.optimize import linprog
import numpy as np

cascades = [
    {
        0: 0,        # seed infected at time 0
        1: 1, 2: 1,  # nodes 1 and 2 infected at time 1 (both neighbors of 0)
        3: 2, 4: 2,  # nodes 3 and 4 infected at time 2 (neighbors of 1 or 2)
        5: 3, 6: 3,  # nodes 5 and 6 infected at time 3
        7: 4, 8: 4,  # nodes 7 and 8 infected at time 4
        9: 5, 10: 5  # nodes 9 and 10 infected at time 5
    },
    {
        3: 0,         # different seed
        1: 1, 4: 1,  # infected together at time 1
        0: 2, 2: 2,  # infected at time 2
        5: 3, 6: 3,  # infected at time 3
        7: 4, 8: 4,  # infected at time 4
        9: 5, 10: 5  # infected at time 5
    },
    {
        10: 0,         # seed at 10
        8: 1, 9: 1,   # infected at time 1
        6: 2, 7: 2,   # infected at time 2
        4: 3, 5: 3,   # infected at time 3
        2: 4, 3: 4,   # infected at time 4
        0: 5, 1: 5    # infected at time 5
    }
]


# Get the set of all nodes that appear in any cascade
all_nodes = set()
for cascade in cascades:
    all_nodes.update(cascade.keys())

# Total number of nodes
n = max(all_nodes) + 1

# Create candidate edges
edges = [(i, j) for i in range(n) for j in range(n) if i != j]
edgesIdx = {edge: i for i, edge in enumerate(edges)}
total_edges = len(edges)

# NP Array of cost
c = np.ones(total_edges)

# Construct lin prog arrays
A = []
b = []
bounds = [(0, 1) for _ in range(total_edges)]

# Constructing A's constraint matrix
for cascade in cascades:
    sorted_nodes = sorted(cascade.items(), key=lambda x: x[1])
    for node_v, time_step_v in sorted_nodes:
        if time_step_v == 0:  # skip source node
            continue

        node_constraint = np.zeros(total_edges)   # initialize constraint with no candidates
        for node_u, time_step_u in cascade.items():
            if (time_step_u < time_step_v) and ((node_u, node_v) in edgesIdx):
                node_constraint[edgesIdx[(node_u, node_v)]] = -1

        A.append(node_constraint)
        b.append(-1)

A = np.array(A)
b = np.array(b)

res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

x_lp = res.x
x_binary = np.random.binomial(1, x_lp)

recovered_edges = [edges[i] for i, val in enumerate(x_binary) if val == 1]
G = nx.DiGraph()
G.add_edges_from(recovered_edges)

print(G.edges)
