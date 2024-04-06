from os import listdir
from networkit import readGraph, Format
from SIR_model import SIR_model
import json

if __name__ == '__main__':
    model = SIR_model(0.5, 0.2, [1], 100)

    for i, gp in enumerate(listdir("../graphs/")):
        print(f"{i + 1}) ../graphs/{gp}")
    graph_path = input("Enter the graph path (above you can find some suggestions):")
    G = readGraph(graph_path, Format.METIS)

    model.run(G)
    print(model.get_all_info())
