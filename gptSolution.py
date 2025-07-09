import cvxpy as cp
import numpy as np
import networkx as nx

n = 20  # number of nodes
edges = [(i, j) for i in range(n) for j in range(n) if i != j]
edge_indices = {e: k for k, e in enumerate(edges)}
x = cp.Variable(len(edges))


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
