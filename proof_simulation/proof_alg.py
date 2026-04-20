import networkx as nx
import numpy as np
import random

p = 0.2
M = 10

class TestGraph:
    
    def __init__(self, G: nx.Graph):
        self.G = G
        self.n = G.number_of_nodes()
        self.infection_array = np.zeros(self.n)
        self.dmax = max(G.degree(node) for node in G.nodes())


def create_seed_nodes(n: int) -> np.ndarray:
    
    res = np.zeros(n)
    
    for i in range(n):
        if random.random() <= p:
            res[i] = 1
    
    return res


def cascade_sequence(graph: TestGraph) -> tuple[np.ndarray]:
    
    infection_state = create_seed_nodes(graph.n)
    res = [infection_state]
    
    new_infection_state = infection_state.copy()

    for node in graph.G.nodes():

        if infection_state[node] == 1:
            continue
        for neighbor in graph.G.neighbors(node):
            if infection_state[neighbor] == 1:
                new_infection_state[node] = 1
                break
            
    res.append(new_infection_state)
    infection_state = new_infection_state
    
    return res


def generate_cascades(G: TestGraph, M: int) -> list[tuple[np.ndarray, np.ndarray]]:
    return [cascade_sequence(G) for _ in range(M)]


def get_certified_non_edges_from_cascade(t0: np.ndarray, t1: np.ndarray) -> set[tuple[int, int]]:
    seeds = np.where(t0 == 1)[0]
    uninfected = np.where(t1 == 0)[0]
    ret = set()
    for v in uninfected:
        for u in seeds:
            ret.add((min(u, v), max(u,v)))
    
    return ret


def recover_non_edges(G: TestGraph, M: int) -> set[tuple[int, int]]:
    cascades = generate_cascades(G, M)
    recovered_non_edges = set()
    for cascade in cascades:
        recovered_non_edges.update((get_certified_non_edges_from_cascade(cascade[0], cascade[1])))
    
    return recovered_non_edges


def test_recovery_coverage(G: TestGraph, M: int):

    true_edges = set(G.G.edges())
    true_non_edges = set(nx.non_edges(G.G))
    recovered_non_edges = recover_non_edges(G, M)

    # said edge does not exist, but does
    false_negatives = recovered_non_edges & true_edges

    # were not able to rule out edge, but it doesn't exist in graph
    false_positives = round(len(recovered_non_edges) / len(true_non_edges) * 100, 2)
    
    print(f"Will be set() if correct proof for non-edges: {false_negatives},\nTotal Non-Edge Recovery: {false_positives}%")

lm = nx.les_miserables_graph()
lm = nx.convert_node_labels_to_integers(lm)
lm = TestGraph(lm)

test_recovery_coverage(lm, M=200)