import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import graphs as gp
from scipy.optimize import linprog

# Class TestGraph
# --- Given a ground truth graph
# --- Given or assigns a set of initial nodes to be infected
# --- Given or assigns a random threshold b to each node

class testGraph:
    
    def __init__(self, G_init: nx.graph, b: np.array, x0: np.array):
        
        self.ground = G_init
        self.x0 = x0
        
        self.current = G_init
        self.x = x0
        
        self.b = b
        
        self.n = self.ground.number_of_nodes()
        
        # self.xo = np.empty(self.n)
        # self.b = np.empty(self.n)
        
        # for idx, node in enumerate(self.ground):
        #     self.xo[idx] = int(np.random.uniform(-1, 2))
        #     self.b[idx] = int(np.random.uniform(0, len(list(self.ground.neighbors(node)))))





# --------------- TEST CASE GENERATION ---------------

# Generate Cascade

# g0 initial graph with node and node neighbors, using NetworkX Graph class
# b - set of pairs indicating each nodes threshold

# infects nodes if the number of neighbors infected (aka =1) is greater than b[i] 

def cascade(g0: testGraph, b: np.array) -> tuple[np.array, bool]:
    
    x_new = g0.x.copy()
    
    for i in range(len(g0.x)):
        if g0.x[i] == 0:
            count = sum(1 for node in g0.current.neighbors(i) if g0.x[node] == 1)
            if count >= b[i]:
                x_new[i] = 1
    
    updated = not np.array_equal(x_new, g0.x)
    g0.x = x_new
    
    return (x_new, updated)


# Generate Cascade Sequence
# T -> Time Steps (number of the cascade step)
# M -> Total cascade amount

def generate_cascade_sequence(g0: testGraph, M: int):
    
    infection_matrix = [g0.x0.copy()]
    for i in range(M):
        x_new, updated = cascade(g0, g0.b)
        if not updated:
            break
        infection_matrix.append(x_new)
    
    return np.array(infection_matrix)



    

# --------------- GRAPH SOLVERS ---------------

# [1] X_(t+1),i - X_t,i = 1 iff \sum A_ij * x_t,j >= b_i
# [2] X_(t+1),i = 0         iff \sum A_ij * X_t,j < b_i


# Build Constraints
# -> returns tuple (t-step, node, infection_status)

# iterates through time steps/cascades from the infection matrix
# if x_t1 - x_t == 1: the node is newly infected

def build_constraints(infection_matrix: np.ndarray, b: np.array, n: int) -> tuple[int, int, str]:
    constraints = []
    
    for t in range(len(infection_matrix) - 1):
        x_t  = infection_matrix[t]
        x_t1 = infection_matrix[t + 1]
        
        for i in range(n):
            if x_t1[i] - x_t[i] == 1:
                constraints.append((t, i, 'infected'))
            elif x_t1[i] == 0:
                constraints.append((t, i, 'clean'))
    
    return constraints


# Claude Solver Implementation

def solve(g0: testGraph, infection_matrix: np.ndarray, constraints: list) -> np.ndarray:
    n = g0.n
    n2 = n * n

    # --- Objective: minimise sum(A), i.e. find sparsest graph
    c = np.ones(n2)

    # --- Build inequality constraints
    A_ub, b_ub = [], []

    for (t, i, condition) in constraints:
        x_t = infection_matrix[t]
        row = np.zeros(n2)

        # The sum we care about is: sum_j A[i][j] * x_t[j]
        # In the flattened vector, A[i][j] lives at index i*n + j
        row[i*n : i*n + n] = x_t

        if condition == 'infected':
            # sum >= b[i]  →  -sum <= -b[i]
            A_ub.append(-row)
            b_ub.append(-g0.b[i])
        else:
            # sum < b[i]  →  sum <= b[i] - 1  (integer assumption)
            A_ub.append(row)
            b_ub.append(g0.b[i] - 1)

    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    # --- Bounds: 0 <= A_ij <= 1 (relaxed binary)
    bounds = [(0, 1)] * n2

    # --- Solve
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if not result.success:
        print("Solver failed:", result.message)
        return None

    # --- Round to binary and reshape to n x n
    A_hat = np.round(result.x).reshape(n, n)

    # --- Enforce symmetry and zero diagonal
    A_hat = np.triu(A_hat, k=1)
    A_hat = A_hat + A_hat.T

    return A_hat





# --------------- SIMULATE ---------------

def display_graph(graph: nx.Graph):
    nx.draw(graph, with_labels=True, node_color="skyblue", edge_color="gray", node_size=800)
    plt.title(str(graph))
    plt.show()
    
ZACKARY_KARATE_CLUB = testGraph(gp.zkc, gp.zkc_b, gp.zkc_x0)
LES_MISERABLES = testGraph(gp.lm, gp.lm_b, gp.lm_x0)

infection_graph = generate_cascade_sequence(LES_MISERABLES, 10)