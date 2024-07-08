from typing import Callable
from networkit import community as comity
from networkit import readGraph
from networkit import Format
import json
from networkit.graphio import BinaryPartitionWriter
import os


class PartitionGenerator:
    _configuration: dict

    def __new__(cls, config_file="./partition_config.json"):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PartitionGenerator, cls).__new__(cls)
            cls.instance._config_file = config_file
            with open(config_file, 'r') as file:
                cls.instance._configuration = json.load(file)
        return cls.instance

    def reload_config(self):
        with open(self._config_file, 'r') as file:
            self._configuration = json.load(file)

    def _get_graphs_paths(self, path):
        paths_to_check = [path]
        paths = []
        while len(paths_to_check) > 0:
            current_path = paths_to_check.pop()
            if os.path.isdir(current_path):
                for new_path in os.listdir(current_path):
                    paths_to_check.append(f"{current_path}/{new_path}")
            elif self._configuration["filter_keyword"] in current_path:
                paths.append(current_path)
        return paths

    def run(self, gen_func: Callable):
        paths = self._get_graphs_paths(self._configuration["graphs_path"])
        for path in paths:
            print("Start generation of partition for", path)
            G = readGraph(path, Format.METIS)
            partition = gen_func(G)
            partition_writer = BinaryPartitionWriter()
            graph_name = path.split('/')[-1]
            if graph_name.endswith(".graph"):
                graph_name = graph_name[:-len(".graph")]
            partition_writer.write(partition, os.path.join(self._configuration["output_folder"], graph_name))
            print("End generation of partition for", path)


def PLM_partition(G):
    plm_community_algo = comity.PLM(G, True)
    plm_community_algo.run()
    return plm_community_algo.getPartition()


def BalancedClustering_partition(G, k):
    partition_generator = comity.ClusteringGenerator()
    return partition_generator.makeContinuousBalancedClustering(G, k)


if __name__ == '__main__':
    PartitionGenerator().run(PLM_partition)
