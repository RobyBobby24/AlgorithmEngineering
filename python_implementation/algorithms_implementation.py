from networkit import readGraph
from networkit import Format
from networkit import community as comity
from networkit import graphtools
from networkit import centrality
from networkit.graph import Graph
from networkit.distance import BFS
from networkit.distance import MultiTargetBFS
from time import process_time, time
import os
from csv_writer import CsvWriter
import pdb
from networkit.graphio import BinaryPartitionReader


def compute_community(G):
    plm_community_algo = comity.PLM(G, True)
    plm_community_algo.run()
    plm_communities = plm_community_algo.getPartition()
    community_induced_graph = {}
    for i in range(plm_communities.numberOfSubsets()):
        subset = plm_communities.getMembers(i)
        community_induced_graph[i] = graphtools.subgraphFromNodes(G, subset)
    return plm_communities, community_induced_graph


def read_community(G: Graph, community_path):
    partition_reader = BinaryPartitionReader()
    plm_communities = partition_reader.read(community_path)
    community_induced_graph = {}
    for i in range(plm_communities.numberOfSubsets()):
        subset = plm_communities.getMembers(i)
        community_induced_graph[i] = graphtools.subgraphFromNodes(G, subset)
    return plm_communities, community_induced_graph


def btw_max(graph):
    LBC = centrality.Betweenness(graph)
    LBC.run()
    return LBC.ranking()[0]


def compute_community_gateway(graph: Graph, community_graph: Graph, community_nodes, max_LBC_node):
    max_ICL = 0
    max_ICL_nodes = []
    for node_from in community_nodes:
        total_degree = graph.degree(node_from)
        inner_degree = community_graph.degree(node_from)
        out_degree = total_degree - inner_degree
        if out_degree > max_ICL:
            max_ICL_nodes = [node_from]
            max_ICL = out_degree
        elif out_degree == max_ICL:
            max_ICL_nodes.append(node_from)

    if len(max_ICL_nodes) == 1:
        return max_ICL_nodes[0]
    else:
        min_distance = 0
        max_ICL_node = -1
        for node in max_ICL_nodes:
            bfs = BFS(community_graph, node, False, False, max_LBC_node)
            bfs.run()
            distance = bfs.distance(max_LBC_node)
            if max_ICL_node == -1 or distance < min_distance:
                min_distance = distance
                max_ICL_node = node
        return max_ICL_node


def compute_GLR(node, graph: Graph, LBC_nodes, gateways, alpha1=0.5, alpha2=0.5):
    # pdb.set_trace() # start debug
    bfs = MultiTargetBFS(graph, node, LBC_nodes.values())
    bfs.run()
    summation_LBC_distances = sum(bfs.getDistances())
    bfs = MultiTargetBFS(graph, node, gateways.values())
    bfs.run()
    summation_gateways_distances = sum(bfs.getDistances())
    return 1 / (alpha1 * summation_LBC_distances + alpha2 * summation_gateways_distances)


def community_centrality_std(G, start_time, measure_time_func=None):
    # pdb.set_trace()
    times = {}
    community_sets, community_graphs = compute_community(G)  # compute community from graph
    # community_sets, community_graphs = read_community(G, "../partial_results/community") #load community from file

    if measure_time_func is not None:
        times["Community computation"] = measure_time_func() - start_time
    else:
        print("community computation: ", time() - start_time)

    max_LBC_community = {}
    gateways = {}
    # pdb.set_trace() # start debug
    for i in community_graphs.keys():
        max_LBC_node = btw_max(community_graphs[i])[0]
        max_LBC_community[i] = max_LBC_node
        gateways[i] = compute_community_gateway(G, community_graphs[i], community_sets.getMembers(i), max_LBC_node)

    if measure_time_func is not None:
        times["Nodes computation"] = measure_time_func() - start_time
    else:
        print("nodes_computation: ", time() - start_time)

    ranking_nodes = []
    for node in G.iterNodes():
        glr_i = compute_GLR(node, G, max_LBC_community, gateways)
        ranking_nodes.append((node, glr_i))

    if measure_time_func is not None:
        times["GLR computation"] = measure_time_func() - start_time
    else:
        print("GLR_computation: ", time() - start_time)

    ranking_nodes.sort(reverse=False, key=lambda item: item[1])

    if measure_time_func is not None:
        return ranking_nodes, times

    else:
        return ranking_nodes


if __name__ == "__main__":
    for i, gp in enumerate(os.listdir("../graphs/")):
        print(f"{i + 1}) ../graphs/{gp}")
    graph_path = input("Enter the graph path (above you can find some suggestions):")
    G = readGraph(graph_path, Format.METIS)
    start = process_time()
    measure_time = True

    centrality_rank, times = community_centrality_std(G, start, process_time)

    if measure_time:
        times["Total"] = process_time() - start
        print(process_time() - start)
    else:
        print(process_time() - start)
    file_name = graph_path.split("/")[-1]

    CsvWriter().write(
        centrality_rank,
        f"../results/pythonStd({file_name})",
        ["Node", "Centrality Degree"],
        lambda node_degree: {"Node": node_degree[0], "Centrality Degree": node_degree[1]}
    )

    if measure_time:
        times["Graph"] = file_name
        print(times)
        CsvWriter().write(
            [times],
            f"../results/time",
            ["Graph", "Community computation", "Nodes computation", "GLR computation", "Total"],
            file_open_mode="a"
        )
