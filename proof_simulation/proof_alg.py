import networkx as nx
import numpy as np
import random
import math
import matplotlib.pyplot as plt

p = 0.2
m = 250
n = 100

class TestGraph:
    def __init__(self, G: nx.Graph):
        self.G = G
        self.n = G.number_of_nodes()
        self.dmax = max(G.degree(node) for node in G.nodes())


def create_seed_nodes(n: int) -> np.ndarray:
    return (np.random.random(n) <= p).astype(float)


def cascade_sequence(graph: TestGraph) -> tuple[np.ndarray, np.ndarray]:
    t0 = create_seed_nodes(graph.n)
    t1 = t0.copy()

    for node in graph.G.nodes():
        if t0[node] == 1:
            continue
        for neighbor in graph.G.neighbors(node):
            if t0[neighbor] == 1:
                t1[node] = 1
                break

    return t0, t1


def generate_cascades(G: TestGraph, M: int) -> list[tuple[np.ndarray, np.ndarray]]:
    return [cascade_sequence(G) for _ in range(M)]


def get_certified_non_edges_from_cascade(t0: np.ndarray, t1: np.ndarray) -> set[tuple[int, int]]:
    seeds = np.where(t0 == 1)[0]
    uninfected = np.where(t1 == 0)[0]

    if len(seeds) == 0 or len(uninfected) == 0:
        return set()

    u, v = np.meshgrid(seeds, uninfected)
    pairs = np.stack([np.minimum(u, v), np.maximum(u, v)], axis=-1).reshape(-1, 2)

    return set(map(tuple, pairs))


def bound_analysis(G: TestGraph, delta: float) -> float:
    return (math.log(G.n) / (p * (1-p)**G.dmax)) * math.log(1 / delta)


def generate_random_graph() -> TestGraph:
    return TestGraph(nx.dense_gnm_random_graph(n, m))


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
    
    print(f"Will be set() if correct conditions for non-edges: {false_negatives},\nTotal Non-Edge Recovery: {false_positives}%")


def plot_recovery_vs_cascades(G: TestGraph, M_values: list[int]):
    true_non_edges = set(nx.non_edges(G.G))

    rates = []
    for M in M_values:
        recovered = recover_non_edges(G, M)
        rate = len(recovered) / len(true_non_edges) * 100
        rates.append(rate)
        print(f"M={M}: {rate:.2f}%")

    plt.figure(figsize=(10, 6))
    plt.plot(M_values, rates, marker='o')
    plt.xlabel('Number of Cascades (M)')
    plt.ylabel('Non-Edge Recovery Rate (%)')
    plt.title('Non-Edge Recovery Rate vs Number of Cascades')
    plt.ylim(0, 105)
    plt.grid(True)
    plt.show()


M_values = [1, 5, 10, 20, 50, 100, 200]
plot_recovery_vs_cascades(generate_random_graph(), M_values)