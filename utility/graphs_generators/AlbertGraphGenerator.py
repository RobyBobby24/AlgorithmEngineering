# BarabasiAlbertGenerator begin with a _start Graph that has n_0  connected nodes
# at each step connect a new node to a random node (n_i) with probability of:
# (deg(n_i)/ sum( deg(n_j) ) for n_j in set of G nodes )

from networkit.generators import BarabasiAlbertGenerator
from networkit import writeGraph, Format
from random import randint
from GraphGenerator import GraphGenerator

class AlbertGraphGenerator(GraphGenerator):
    start_node_number: int
    max_node_number: int
    doubling_n_factor: int

    def __init__(self, graph_flag: str, result_folder: str, start_node_number: int, max_node_number: int, doubling_n_factor: int = 2):
        super(AlbertGraphGenerator, self).__init__(result_folder, graph_flag)
        self.start_node_number = start_node_number
        self.max_node_number = max_node_number
        self.doubling_n_factor = doubling_n_factor

    def run(self):
        node_number = self.start_node_number
        while node_number < self.max_node_number:
            attachment_nodes = randint(2, 7)
            # We chose a random attachment_nodes to randomized most important nodes
            # (because node just has neighbor => deg > 0)
            # The random interval is in percentual to the total number of graph nodes 0%-50%
            graph_generator = BarabasiAlbertGenerator(attachment_nodes, node_number)
            G = graph_generator.generate()
            writeGraph(G, f"{self.result_folder}/{self.graph_flag}(n={node_number}, m={G.numberOfEdges()}).graph", Format.METIS)
            print("genereted: ", f"{self.result_folder}/{self.graph_flag}(n={node_number}, m={G.numberOfEdges()}).graph")
            node_number *= self.doubling_n_factor
        print("generation terminated")

if __name__ == "__main__":
    output_folder = "../../graphs/albert/"
    graph_flag = "Albert"
    start_node_number = 160
    max_node_number = 30000

    generator = AlbertGraphGenerator(graph_flag, output_folder, start_node_number, max_node_number)
