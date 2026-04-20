import networkx as nx
import numpy as np
import random
import math
import matplotlib.pyplot as plt

p = 0.2
m = 4000
n = 1000

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


def plot_recovery_vs_cascades(G: TestGraph, M_values: list[int]):
    true_non_edges = set(nx.non_edges(G.G))
    max_M = max(M_values)
    M_set = set(M_values)

    all_cascades = generate_cascades(G, max_M)
    recovered = set()
    recovery_rates = {}

    for i, cascade in enumerate(all_cascades):
        recovered.update(get_certified_non_edges_from_cascade(cascade[0], cascade[1]))
        if (i + 1) in M_set:
            recovery_rates[i + 1] = len(recovered) / len(true_non_edges) * 100
        if recovered >= true_non_edges:
            for M in M_values:
                if M not in recovery_rates:
                    recovery_rates[M] = 100.0
            break

    rates = [recovery_rates.get(M, 100.0) for M in M_values]

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