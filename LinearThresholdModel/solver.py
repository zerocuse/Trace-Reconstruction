import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import graphs as gp
from scipy.optimize import linprog
import pickle

# Class TestGraph
# --- Given a ground truth graph
# --- Given or assigns a set of initial nodes to be infected
# --- Given or assigns a random threshold b to each node

class testGraph:
    
    def __init__(self, G_init: nx.graph, b: np.ndarray, x0: np.ndarray):
        
        # ground state
        self.ground = G_init
        self.x0 = x0.copy()
        
        # guessing the graph
        self.current = G_init
        self.x = x0.copy()
        
        # threshold array
        self.b = b
        
        self.n = G_init.number_of_nodes()
        
        # self.xo = np.empty(self.n)
        # self.b = np.empty(self.n)
        
        # for idx, node in enumerate(self.ground):
        #     self.xo[idx] = int(np.random.uniform(-1, 2))
        #     self.b[idx] = int(np.random.uniform(0, len(list(self.ground.neighbors(node)))))

    def reset(self):
        self.x = self.x0.copy()




# --------------- TEST CASE GENERATION ---------------

# Generate Cascade

# g0 initial graph with node and node neighbors, using NetworkX Graph class
# b - set of pairs indicating each nodes threshold

# infects nodes if the number of neighbors infected (aka =1) is greater than b[i] 

def cascade(g0: testGraph) -> tuple[np.ndarray, bool]:
    
    x_new = g0.x.copy()
    
    for i in range(len(g0.x)):
        if g0.x[i] == 0:
            count = sum(1 for node in g0.current.neighbors(i) if g0.x[node] == 1)
            if count >= g0.b[i]:
                x_new[i] = 1
    
    updated = not np.array_equal(x_new, g0.x)
    g0.x = x_new
    
    return (x_new, updated)


# Generate Cascade Sequence
# T -> Time Steps (number of the cascade step)
# M -> Total cascade amount

def generate_cascade_sequence(g0: testGraph, M: int) -> np.ndarray:
    
    infection_matrix = [g0.x0.copy()]
    for i in range(M):
        x_new, updated = cascade(g0)
        if not updated:
            break
        infection_matrix.append(x_new.copy())
    
    return np.array(infection_matrix)



    

# --------------- GRAPH SOLVERS ---------------

# [1] X_(t+1),i - X_t,i = 1 iff \sum A_ij * x_t,j >= b_i
# [2] X_(t+1),i = 0         iff \sum A_ij * X_t,j < b_i


# Build Constraints
# -> returns tuple (t-step, node, infection_status)

# iterates through time steps/cascades from the infection matrix
# if x_t1 - x_t == 1: the node is newly infected

def build_constraints(infection_matrix: np.ndarray, b: np.ndarray, n: int) -> tuple[int, int, str]:
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


# Count Contradictions
# -> return a matrix of contradiction counts
# -> return matrix where matrix[i] = 1 if node i is in contradiction

def count_contradicitons(g: testGraph, x_guess: np.ndarray) -> np.ndarray:
    
    contradictions = np.zeros(g.n)
    
    for i in range(g.n):
        infected_neighbors = sum(1 for node in g.current.neighbors(i) if x_guess[j] == 1)
        
        # xhat thinks its infected when it shouldnt be
        if (x_guess[i] == 1) and (infected_neighbors < g.b[i]):
            contradictions[i] = 1
        
        # xhat thinks its clean when it should be infected
        elif (x_guess[i] == 0) and (infected_neighbors >= g.b[i]):
            contradictions[i] = 1

    return contradictions


# Greedy LTM Solver
# Updates xhat iteratively until either max iteration, or no contradictory nodes

def greedy_ltm_solver(g: testGraph, x_guess: np.ndarray, max_steps: int=1000):
    
    x = x_guess.copy()
    
    for step in range(max_steps):
        
        contradictions = count_contradicitons(g, x)
        total = np.sum(contradictions)
        
        if total == 0:
            return x_guess
        
        best_reduction = 0
        best_node = None
        
        for i in range(g.n):
            
            x_test = x.copy()
            x_test[i] = 1 - x_test[i]
            
            new_total = np.sum(count_contradicitons(g, x_test))
            reduction = total - new_total
            
            if reduction > best_reduction:
                best_reduction = reduction
                best_node = i
            
        if best_node is None:
            return x
                
        x[best_node] = 1 - x[best_node]
        
    return x
        




# --------------- SIMULATE ---------------

def display_graph(graph: nx.Graph):
    nx.draw(graph, with_labels=True, node_color="skyblue", edge_color="gray", node_size=800)
    plt.title(str(graph))
    plt.show()
    
ZACKARY_KARATE_CLUB = testGraph(gp.zkc, gp.zkc_b, gp.zkc_x0)
LES_MISERABLES = testGraph(gp.lm, gp.lm_b, gp.lm_x0)