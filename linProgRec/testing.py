import networkx as nx
import matplotlib.pyplot as plt
from solution import recover_graph
from gptSolution import gpt_recover_graph
from hamming_distance import calculate_hamming_distance as chd


def choose_layout(graph):
    try:
        if nx.is_tree(graph):
            # Tree layout using Graphviz if available
            try:
                from networkx.drawing.nx_pydot import graphviz_layout
                return graphviz_layout(graph, prog="dot")
            except ImportError:
                # Fallback to shell layout if Graphviz is not installed
                return nx.shell_layout(graph)
        elif nx.cycle_graph(len(graph.nodes())).edges() <= graph.edges() and nx.is_connected(graph):
            return nx.circular_layout(graph)
        elif nx.is_bipartite(graph):
            left, _ = nx.bipartite.sets(graph)
            return nx.bipartite_layout(graph, nodes=left)
        else:
            return nx.spring_layout(graph, seed=42)
    except Exception:
        return nx.spring_layout(graph, seed=42)


def test(og_graph, cascades):
    # Recover the graph
    recovered_graph = recover_graph(cascade_set=cascades)

    # Calculate Hamming distance
    hamming_dist = chd(og_graph, recovered_graph)

    # Choose appropriate layout
    pos = choose_layout(og_graph)

    # Create side-by-side plots
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Original graph
    nx.draw(
        og_graph,
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
        pos=pos,
        ax=axes[1],
        with_labels=True,
        node_color='lightblue',
        edge_color='gray',
        node_size=800,
        font_size=10
    )
    axes[1].set_title(f"Recovered Graph\nHamming Distance: {hamming_dist}")
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()
