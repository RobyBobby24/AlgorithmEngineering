import os


# utility function
def filter_file(keyword, root):
    result = []
    for i, gp in enumerate(os.listdir(root)):
        if keyword in gp:
            result.append(f"{root}{gp}")
    return result


def compute_partition_path(obj, graph_path: str, graph_dir: str, partition_dir: str):
    start_pos = len(graph_dir)
    graph_name = graph_path[start_pos:]
    if graph_name.endswith(".graph"):
        graph_name = graph_name[:-len(".graph")]
    return f"{partition_dir}/{graph_name}"


# strategies

def partition_graph_strategy(obj):
    graph_dir = obj.read_config("strategies", "partition_graph", "graphs_dir")
    partition_dir = obj.read_config("strategies", "partition_graph", "partition_dir")
    graph_paths = filter_file(obj.read_config("filter_world"), graph_dir)
    return {graph_path: compute_partition_path(obj, graph_path, graph_dir, partition_dir) for graph_path in graph_paths}


def graph_strategy(obj):
    graph_dir = obj.read_config("strategies", "graph", "graphs_dir")
    graph_paths = filter_file(obj.read_config("filter_world"), graph_dir)
    return {graph_path: None for graph_path in graph_paths}


def partition_strategy(obj):
    partition_dir = obj.read_config("strategies", "partition", "partition_dir")
    partitions_paths = filter_file(obj.read_config("filter_world"), partition_dir)
    graph_path = obj.read_config("strategies", "partition", "graph_path")
    return {graph_path: partition_path for partition_path in partitions_paths}

