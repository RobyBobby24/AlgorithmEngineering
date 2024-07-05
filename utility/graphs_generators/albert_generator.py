# BarabasiAlbertGenerator begin with a _start Graph that has n_0  connected nodes
# at each step connect a new node to a random node (n_i) with probability of:
# (deg(n_i)/ sum( deg(n_j) ) for n_j in set of G nodes )

from networkit.generators import BarabasiAlbertGenerator
from networkit import writeGraph, Format
from random import randint

if __name__ == "__main__":
    output_folder = "../../graphs/"
    start_node_number = 10
    max_node_number = 30000

    number_nodes = start_node_number

    while number_nodes < max_node_number:
        attachment_nodes = randint(2, 7)
        # We chose a random attachment_nodes to randomized most important nodes
        # (because node just has neighbor => deg > 0)
        # The random interval is in percentual to the total number of graph nodes 0%-50%
        graph_generator = BarabasiAlbertGenerator(attachment_nodes, number_nodes)
        G = graph_generator.generate()
        writeGraph(G, f"{output_folder}DoubleExperiment(n={number_nodes}).graph", Format.METIS)
        print("genereted: ", f"{output_folder}DoubleExperiment(n={number_nodes}).graph")
        number_nodes *= 2
