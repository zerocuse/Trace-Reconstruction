# ----- TEST CASE GENERATION -----

# Generate Cascade

# generate_cascade(G_init: Graph, T: int, M: int, b: Dict[node: thr]) -> Graph

# T - high bound time steps
# M - high bound cascades
# G_o initial graph with node and node neighbors, using NetworkX Graph class
# b - set of pairs indicating each nodes threshold

# Generates M cascades with T timesteps (producing T x vectors), with each node being infected iff the number of neighbor nodes is greater than or equal to the nodes' threshold

# ------ TEST CASE GENERATION -----



# ------ GRAPH SOLVERS ------

# [1] X_(t+1),i - X_t,i = 1 iff \sum A_ij * x_t,j >= b_i
# [2] X_(t+1),i = 0         iff \sum A_ij * X_t,j < b_i

# ------ GRAPH SOLVERS ------



# Problem 1

# Given: set of infected node vectors X_o, ..., X_T \in {0,1}^n
# Goal: Find A \in {0,1}^(nxn) such that:
#   --> A^T = A
#   --> [1] and [2] hold for all t \in [T], i \in [n], and m \in [M]