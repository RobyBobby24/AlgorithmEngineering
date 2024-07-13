import os


# utility function
def filter_file(keyword, root):
    result = []
    for i, gp in enumerate(os.listdir(root)):
        if keyword in gp:
            result.append(f"{root}{gp}")
    return result


def compute_partition_path(obj, graph_path: str):
    start_pos = len(obj._configuration["graphs_dir"])
    graph_name = graph_path[start_pos:]
    if graph_name.endswith(".graph"):
        graph_name = graph_name[:-len(".graph")]
    return f"{obj._configuration['partition_dir']}/{graph_name}"


# strategies

def partition_graph_strategy(obj):
    graph_paths = filter_file(obj._configuration["filter_world"], obj._configuration["graphs_dir"])
    return {graph_path: compute_partition_path(obj, graph_path) for graph_path in graph_paths}


def graph_strategy(obj):
    graph_paths = filter_file(obj._configuration["filter_world"], obj._configuration["graphs_dir"])
    return {graph_path: None for graph_path in graph_paths}


def partition_strategy(obj):
    partitions_paths = filter_file(obj._configuration["filter_world"],obj._configuration["strategies"]["partition"]["graphs_dir"])
    graph_path = obj._configuration["strategies"]["partition"]["graph_path"]
    return {graph_path: partition_path for partition_path in partitions_paths}

