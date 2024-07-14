from typing import Callable
from networkit import community as comity
import json
from networkit.graphio import BinaryPartitionWriter
import os
import strategies


class PartitionGenerator:
    _configuration: dict

    def __new__(cls, config_file="./partition_config.json"):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PartitionGenerator, cls).__new__(cls)
            cls.instance._config_file = config_file
            with open(config_file, 'r') as file:
                cls.instance._configuration = json.load(file)
            cls.instance.strategy = getattr(strategies, f"{cls.instance._configuration['strategy_name']}_strategy")
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

    def read_config(self, *keys):
        result = self._configuration
        for key in keys:
            result = result[key]
        return result

    def run(self):
        gen_func, parameters, output_paths = self.strategy(self)
        for output_path, parameter in zip(output_paths, parameters):
            partition = gen_func(*parameter)
            partition_writer = BinaryPartitionWriter()
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)
            partition_writer.write(partition, output_path)


if __name__ == '__main__':
    PartitionGenerator().run()
