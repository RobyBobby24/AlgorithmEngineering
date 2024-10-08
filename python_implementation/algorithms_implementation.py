import threading

from networkit import readGraph
from networkit import Format
from networkit import community as comity
from networkit import graphtools
from networkit import centrality
from networkit.graph import Graph
from networkit.distance import BFS
from networkit.distance import SPSP
from networkit.distance import MultiTargetBFS
from time import process_time, time
import os
from csv_writer import CsvWriter
import argparse
import pdb
from networkit.graphio import BinaryPartitionReader
from mytimer import MyTimer
from threading import Thread


# Function for Algorithm
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
    bfs = MultiTargetBFS(graph, node, LBC_nodes.values())
    bfs.run()
    summation_LBC_distances = sum(bfs.getDistances())
    bfs = MultiTargetBFS(graph, node, gateways.values())
    bfs.run()
    summation_gateways_distances = sum(bfs.getDistances())
    return 1 / (alpha1 * summation_LBC_distances + alpha2 * summation_gateways_distances)

# undirected version

def compute_GLR_undirected(graph: Graph, LBC_nodes, gateways, alpha1=0.5, alpha2=0.5):
    ranking_nodes = []
    sources = LBC_nodes + gateways
    distances_computer = SPSP(graph, sources)
    distances_computer.run()
    for node in graph.iterNodes():
        summation_LBC_distances = 0
        for u in LBC_nodes:
            summation_LBC_distances += distances_computer.getDistance(u, node)
        summation_gateways_distances = 0
        for u in gateways:
            summation_gateways_distances += distances_computer.getDistance(u, node)
        ranking_nodes.append((node, 1 / (alpha1 * summation_LBC_distances + alpha2 * summation_gateways_distances)))
    return ranking_nodes


def compute_community_gateway_undirected(graph: Graph, community_graph: Graph, community_nodes, max_LBC_node):
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
        bfs = MultiTargetBFS(community_graph, max_LBC_node, max_ICL_nodes)
        bfs.run()
        distances = bfs.getDistances()
        min_distance = 0
        max_ICL_node = -1
        for node, distance in zip(max_ICL_nodes, distances):
            if max_ICL_node == -1 or distance < min_distance:
                min_distance = distance
                max_ICL_node = node
        return max_ICL_node

# std implementation

def community_centrality_std(G: Graph, measure_time: bool = True, check_correctness: bool = False,
                             partition_path: str = None):
    times = {}
    # Community Computation
    if partition_path is None:
        community_sets, community_graphs = compute_community(G)  # compute community from graph
    else:
        community_sets, community_graphs = read_community(G, partition_path)  # load community from file

    _COMMUNITY_COMPUTATION_PAUSE(times, community_sets, measure_time, check_correctness)

    # Nodes Computation
    max_LBC_community = {}
    gateways = {}
    for i in community_graphs.keys():
        if len(community_sets.getMembers(i)) != 0:
            max_LBC_node = btw_max(community_graphs[i])[0]
            max_LBC_community[i] = max_LBC_node
            gateways[i] = compute_community_gateway(G, community_graphs[i], community_sets.getMembers(i), max_LBC_node)
            _CHECK_NODES_COMPUTATION(max_LBC_node, community_sets, gateways, i, check_correctness)

    _NODES_COMPUTATION_PAUSE(times, measure_time)

    # GLR Computation
    ranking_nodes = []
    for node in G.iterNodes():
        glr_i = compute_GLR(node, G, max_LBC_community, gateways)
        ranking_nodes.append((node, glr_i))

    _GLR_COMPUTATION_PAUSE(times, measure_time)

    ranking_nodes.sort(reverse=False, key=lambda item: item[1])

    if measure_time:
        return ranking_nodes, times

    else:
        return ranking_nodes

# undirected implementation

def community_centrality_undirected(G: Graph, measure_time: bool = True, check_correctness: bool = False, partition_path: str = None):
    times = {}
    # Community Computation
    if partition_path is None:
        community_sets, community_graphs = compute_community(G)  # compute community from graph
    else:
        community_sets, community_graphs = read_community(G, partition_path)  # load community from file

    _COMMUNITY_COMPUTATION_PAUSE(times, community_sets, measure_time, check_correctness)

    # Nodes Computation
    max_LBC_community = []
    gateways = []
    for i in community_graphs.keys():
        if len(community_sets.getMembers(i)) != 0:
            max_LBC_node = btw_max(community_graphs[i])[0]
            max_LBC_community.append(max_LBC_node)
            gateways.append(compute_community_gateway_undirected(G, community_graphs[i], community_sets.getMembers(i), max_LBC_node))
            _CHECK_NODES_COMPUTATION(max_LBC_node, community_sets, gateways, i, check_correctness)

    _NODES_COMPUTATION_PAUSE(times, measure_time)

    # GLR Computation
    ranking_nodes = compute_GLR_undirected(G, max_LBC_community, gateways)

    _GLR_COMPUTATION_PAUSE(times, measure_time)

    ranking_nodes.sort(reverse=False, key=lambda item: item[1])

    if measure_time:
        return ranking_nodes, times

    else:
        return ranking_nodes


# Utility function to manage input/output

def _COMMUNITY_COMPUTATION_PAUSE(times, community_sets, measure_time=True, check_correctness=False):
    # PAUSE!!!
    current_time = MyTimer().get_elapsed_time()
    MyTimer().pause()
    if check_correctness:
        nodes = set()
        for i in range(0, len(community_sets)):
            nodes = nodes.union(community_sets.getMembers(i))
            for j in range(i + 1, len(community_sets)):
                assert community_sets.getMembers(i).isdisjoint(community_sets.getMembers(j))
        assert len(nodes) == G.numberOfNodes()

    if measure_time:
        times["Community computation"] = current_time
    else:
        print("community computation: ", current_time)

    MyTimer().resume()
    # RESUME!!!


def _NODES_COMPUTATION_PAUSE(times, measure_time=True):
    # PAUSE!!!
    current_time = MyTimer().get_elapsed_time()
    MyTimer().pause()
    if measure_time:
        times["Nodes computation"] = current_time
    else:
        print("nodes_computation: ", current_time)
    MyTimer().resume()
    # RESUME!!!


def _GLR_COMPUTATION_PAUSE(times, measure_time=True):
    # PAUSE!!!
    current_time = MyTimer().get_elapsed_time()
    MyTimer().pause()
    if measure_time:
        times["GLR computation"] = current_time
    else:
        print("GLR_computation: ", current_time)
    MyTimer().resume()
    # RESUME!!!


def _CHECK_NODES_COMPUTATION(max_LBC_node, community_sets, gateways, i, check_correctness=False):
    if check_correctness:
        assert max_LBC_node in community_sets.getMembers(i) and gateways[i] in community_sets.getMembers(i)


def show_file(root: str):
    for i, gp in enumerate(os.listdir(root)):
        file = f"{root}/{gp}"
        if os.path.isdir(file):
            show_file(file)
        else:
            print(f"{i + 1}) {file}")


def get_IO_paths():
    # Read Parameters
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('-g', '--graph', type=str, help='Path to the graph file', required=False)
    parser.add_argument('-r', '--result-folder', type=str, help='Path of result folder', required=False)
    parser.add_argument('-f', '--flag', type=str, help='A flag to mark the result', required=False)
    parser.add_argument('-p', '--partition', type=str, help='Path to the partition file', required=False)
    parser.add_argument('-u', '--undirected', action='store_true', help='Enable undirected optimization', required=False)
    args = parser.parse_args()

    graph_path = args.graph
    result_folder = args.result_folder
    flag = args.flag
    partition_path = args.partition
    undirected = args.undirected
    # If graph is not passed as args require it as standard input
    if graph_path is None:
        show_file("../graphs")
        graph_path = input("Enter the graph path (above you can find some suggestions):")

    if result_folder is None:
        result_folder = "../results"

    if flag is None:
        flag = "prova"

    return graph_path, result_folder, flag, partition_path, undirected


def save_results(file_name, centrality_rank, times=None):
    CsvWriter().write(
        centrality_rank,
        f"{result_folder}/pythonStd({file_name})",
        ["Node", "Centrality Degree"],
        lambda node_degree: {"Node": node_degree[0], "Centrality Degree": node_degree[1]},
        True
    )

    if times is not None:
        times["Graph"] = file_name
        print(times)
        CsvWriter().write(
            [times],
            f"{result_folder}/time",
            ["Code", "Graph", "Partition", "Flag", "Community computation", "Nodes computation", "GLR computation", "Total"],
            file_open_mode="a"
        )


if __name__ == "__main__":

    graph_path, result_folder, flag, partition_path, undirected = get_IO_paths()

    # load graph from path
    G = readGraph(graph_path, Format.METIS)
    # setup time
    measure_time = True

    # choose if exec the algorithm in multi-threading or no
    if undirected:
        print("turn on undirected optimization")
        community_centrality = community_centrality_undirected
    else:
        community_centrality = community_centrality_std

    # exec algorithm (save result in centrality_rank, and time in times)
    if partition_path is not None:
        MyTimer(process_time)
        centrality_rank, times = community_centrality(G, partition_path=partition_path)
        total_time = MyTimer().get_elapsed_time()
    else:
        MyTimer(process_time)
        centrality_rank, times = community_centrality(G)
        total_time = MyTimer().get_elapsed_time()

    # compute and print final time and save results
    file_name = graph_path.split("/")[-1]
    if measure_time:
        times["Total"] = total_time
        times["Code"] = "python"
        times["Flag"] = flag
        times["Partition"] = partition_path if partition_path is not None else "None"
        print(total_time)
        save_results(file_name, centrality_rank, times)
    else:
        print(total_time)
        save_results(file_name, centrality_rank)
