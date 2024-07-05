import networkit as nk
from networkit import writeGraph, Format
from random import choice, randint
import pdb

def double_exp_generator(n : int, m: int, connect=True):
    #pdb.set_trace()
    if m < n-1 and connect:
        raise ValueError('graph must have at least n-1 edges to be connect')
    if m > n * (n-1)/2:
        raise ValueError('graph can have at most n*(n-1)/2 edges')
    G = nk.graph.Graph()
    G.addNodes(n)
    added_node = []
    number_edges = 0
    for node in G.iterNodes():
        if len(added_node) == 0:
            added_node.append(node)
        else:
            u = choice(added_node)
            G.addEdge(u, node)
            added_node.append(node)
            number_edges += 1
    while number_edges < m:
        nodes = [i for i in range(0, n)]
        while len(nodes) > 0 and number_edges < m:
            v = nodes.pop(randint(0, len(nodes)-1))
            v_neighbors = [neighbor for neighbor in G.iterNeighbors(v)]
            possible_nodes = [node for node in G.iterNodes() if node not in v_neighbors]
            if len(possible_nodes) > 0:
                u = choice(possible_nodes)
                G.addEdge(u, v)
                number_edges += 1
    return G


if __name__ == '__main__':
    output_folder = "../../graphs/"
    value_to_doubling = "n"
    result_folder = "2exp"+"node" if value_to_doubling == "n" else "2exp"+"edge"
    maxNumberOfGraph = 10
    numberOfNodes = int(input('number of nodes:'))
    numberOfEdges = int(input('number of edges:'))
    generate = True
    numberOfGraph = 0
    while generate and numberOfGraph < maxNumberOfGraph:
        try:
            G = double_exp_generator(numberOfNodes, numberOfEdges)
            writeGraph(G, f"{output_folder}{result_folder}/{result_folder}(n={numberOfNodes}, m={numberOfEdges}).graph", Format.METIS)
            print("genereted: ", f"{output_folder}{result_folder}/{result_folder}(n={numberOfNodes}, m={numberOfEdges}).graph")
            if value_to_doubling == "n":
                numberOfNodes *= 2
            elif value_to_doubling == "m":
                numberOfEdges *= 2
            numberOfGraph += 1
        except:
            generate = False
    print("generation terminated")


