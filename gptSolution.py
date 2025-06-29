import cvxpy as cp
import numpy as np

n = 11  # number of nodes
edges = [(i, j) for i in range(n) for j in range(n) if i != j]
edge_indices = {e: k for k, e in enumerate(edges)}
x = cp.Variable(len(edges))

# Example cascade constraints: list of (source, target) pairs and times
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

constraints = []
for cascade in cascades:
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

print("Recovered edges:", graph_edges)
