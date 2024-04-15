from networkit import readGraph, Format
from time import process_time, time, perf_counter
import os
from csv_writer import CsvWriter
from algorithms_implementation import community_centrality_std

iteration_for_graph = 5
max_time = 300

def filter_graph(keyword):
    result = []
    for i, gp in enumerate(os.listdir("../graphs/")):
        if keyword in gp:
            result.append(f"../graphs/{gp}")
    return result


if __name__ == "__main__":
    graph_paths = filter_graph("DoubleExperiment")

    for graph_path in graph_paths:
        it = 0
        start_time = time()
        print("Processing graph", graph_path)
        G = readGraph(graph_path, Format.METIS)
        while it < iteration_for_graph and time()-start_time < max_time:
            it += 1

            start_CPU = perf_counter()

            centrality_rank, times = community_centrality_std(G, start_CPU, perf_counter)

            times["Total"] = perf_counter() - start_CPU
            print(perf_counter() - start_CPU)

            file_name = graph_path.split("/")[-1]

            times["Graph"] = file_name
            CsvWriter().write(
                [times],
                f"../results/time",
                ["Graph", "Community computation", "Nodes computation", "GLR computation", "Total"],
                file_open_mode="a"
            )
