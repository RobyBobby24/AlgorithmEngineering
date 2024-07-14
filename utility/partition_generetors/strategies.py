from networkit import community as comity
from networkit import readGraph
from networkit import Format
import os


def compute_graphs_paths(obj, path):
    paths_to_check = [path]
    paths = []
    while len(paths_to_check) > 0:
        current_path = paths_to_check.pop()
        if os.path.isdir(current_path):
            for new_path in os.listdir(current_path):
                paths_to_check.append(f"{current_path}/{new_path}")
        elif obj.read_config("filter_keyword") in current_path:
            paths.append(current_path)
    return paths


def _read_graph(path):
    print("Start generation of partition for", path)
    return readGraph(path, Format.METIS)


def _end_partition_gen(path):
    print("End generation of partition for", path)


def PLM_partition(path):
    G = _read_graph(path)
    plm_community_algo = comity.PLM(G, True)
    plm_community_algo.run()
    _end_partition_gen(path)
    return plm_community_algo.getPartition()


def BalancedClustering_partition(path, k):
    G = _read_graph(path)
    partition_generator = comity.ClusteringGenerator()
    _end_partition_gen(path)
    return partition_generator.makeContinuousBalancedClustering(G, k)


def PLM_strategy(obj):
    paths = compute_graphs_paths(obj, obj.read_config("strategies", "PLM", "graphs_path"))
    output_dir = obj.read_config("strategies", "PLM", "output_folder")
    parameters = [[path] for path in paths]
    output_names = []
    for path in paths:
        output_file = os.path.basename(path)
        output_names.append(f"{output_dir}/{output_file}")
    return PLM_partition, parameters, output_names


def BalancedClustering_strategy(obj):
    # Read config (graphs_path, output_folder,  min_number_communities, max_number_communities)
    paths = compute_graphs_paths(obj, obj.read_config("strategies", "BalancedClustering", "graphs_path"))
    output_dir = obj.read_config("strategies", "BalancedClustering", "output_folder")
    number_community = obj.read_config("strategies", "BalancedClustering", "min_number_communities")
    max_number_communities = obj.read_config("strategies", "BalancedClustering", "max_number_communities")

    # doubling number of community
    numbers_community = []
    while number_community <= max_number_communities:
        numbers_community.append(number_community)
        number_community *= 2

    # set parameter to pass to the generator
    parameters = [[path, number_community] for path in paths for number_community in numbers_community]

    # compute output files path
    output_names = []
    for path in paths:
        graph_name = os.path.basename(path)[:-len('.graph')]
        output_names += [f"{output_dir}/{graph_name}/partition{number_community}" for number_community in numbers_community]
    return BalancedClustering_partition, parameters, output_names
