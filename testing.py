import networkx as nx
import matplotlib.pyplot as plt
from solution import recover_graph
from gptSolution import gpt_recover_graph
from hamming_distance import calculate_hamming_distance as chd

# Construct Graph
graph = nx.Graph()
graph_edges = [
    (0, 1), (0, 2),
    (1, 3), (1, 4),
    (2, 5),
    (3, 6),
    (4, 6), (4, 7),
    (5, 7), (5, 8),
    (6, 9),
    (7, 9), (7, 10),
    (8, 10),
    (9, 11),
    (10, 11)
]
graph.add_edges_from(graph_edges)

# Construct Cascades from Original Graph
cascades = [
    {
        0: 0,
        1: 1, 2: 1,
        3: 2, 4: 2, 5: 2,
        6: 3, 7: 3, 8: 3,
        9: 4, 10: 4,
        11: 5
    },
    {
        2: 0,
        5: 1,
        7: 2, 8: 2,
        9: 3, 10: 3,
        11: 4
    },
    {
        5: 0,
        7: 1, 8: 1,
        10: 2,
        11: 3
    },
    {
        1: 0,
        3: 1, 4: 1,
        6: 2, 7: 2,
        9: 3, 10: 3,
        11: 4
    },
    {
        4: 0,
        6: 1, 7: 1,
        9: 2, 10: 2,
        11: 3
    },
    {
        8: 0,
        10: 1,
        11: 2
    }
]

# Establish a recovered graph based on recovered edges
recovered_graph = recover_graph(cascade_set=cascades)

# OPTIONAL: Print Hamming Distance
print(chd(graph, recovered_graph))


# COMPARING GRAPH vs. RECOVERED GRAPH

# Shared layout for both graphs
pos = nx.spring_layout(graph, seed=42)

# Create side-by-side plots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Original graph
nx.draw(
    graph,
    pos=pos,
    ax=axes[0],
    with_labels=True,
    node_color='lightblue',
    edge_color='gray',
    node_size=800,
    font_size=10
)
axes[0].set_title("Original Graph")
axes[0].axis('off')

# Recovered graph
nx.draw(
    recovered_graph,
    pos=pos,  # same layout for fair comparison
    ax=axes[1],
    with_labels=True,
    node_color='lightblue',
    edge_color='gray',
    node_size=800,
    font_size=10
)
axes[1].set_title("Recovered Graph")
axes[1].axis('off')

plt.tight_layout()
plt.show()
