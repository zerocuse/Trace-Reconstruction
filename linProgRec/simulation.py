from solution import recover_graph
from gptSolution import gpt_recover_graph
import networkx as nx


def simulate(graph, cascades, trials):

    n = graph.number_of_nodes()
    recovered_edges = {(i, j): 0 for i in range(n) for j in range(n) if i != j}

    for _ in range(trials):
        rec_graph = recover_graph(cascade_set=cascades)
        for edge in rec_graph.edges:
            recovered_edges[edge] += 1

    has_different_edges = False
    compare_value = None
    for edge, count in recovered_edges.items():
        if count != 0:
            if compare_value and count != compare_value:
                has_different_edges = True
                break
            elif not compare_value:
                compare_value = count

    print(recovered_edges)
    print(has_different_edges)
