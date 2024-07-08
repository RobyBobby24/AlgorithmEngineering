import subprocess
import os
import sys
import json


def filter_graph(keyword, root):
    result = []
    for i, gp in enumerate(os.listdir(root)):
        if keyword in gp:
            result.append(f"{root}{gp}")
    return result


class DoubleExperimentExecutor:
    _configuration: dict
    _config_filename: str
    _code_language: str

    def __new__(cls, config_file_name="./doubleexp_config.json"):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DoubleExperimentExecutor, cls).__new__(cls)
            cls.instance._config_filename = config_file_name
            with open(config_file_name, 'r') as file:
                cls.instance._configuration = json.load(file)
        return cls.instance

    def _get_partition_path(self, graph_path: str):
        start_pos = len(self._configuration["graphs_dir"])
        graph_name = graph_path[start_pos:]
        if graph_name.endswith(".graph"):
            graph_name = graph_name[:-len(".graph")]
        return f"{self._configuration['partition_dir']}/{graph_name}"

    def _interpeter_cmd(self, graph, code_language, interpeter_func):
        interpeter_executable = interpeter_func()
        exe_file = self._configuration['languages_codes'][code_language]["exe_path"]
        if self._configuration['load_partition']:
            partition_path = self._get_partition_path(graph)
            print("read partition mode")
            return [interpeter_executable, exe_file, "-g", graph, "-f", self._configuration["result_flag"], "-p", partition_path]
        else:
            return [interpeter_executable, exe_file, "-g", graph, "-f", self._configuration["result_flag"]]

    def _compiled_cmd(self, graph, code_language):
        exe_file = self._configuration['languages_codes'][code_language]["exe_path"]
        if self._configuration['load_partition']:
            partition_path = self._get_partition_path(graph)
            print("read partition mode")
            return [exe_file, "-g", graph, "-f", self._configuration["result_flag"], "-p", partition_path]
        else:
            return [exe_file, "-g", graph, "-f", self._configuration["result_flag"]]

    def run(self, code_language, get_interpeter=None):
        graph_paths = filter_graph(self._configuration["filter_world"], self._configuration["graphs_dir"])
        for graph in graph_paths:
            print("Start execution of algorithms applied for graph", graph)
            if get_interpeter != None:
                cmd = self._interpeter_cmd(graph, code_language, get_interpeter)
            else:
                cmd = self._compiled_cmd(graph, code_language)

            result = subprocess.run(cmd, capture_output=True, text=True)
            with open(self._configuration["log_file"], "a") as file:
                file.write(f"STANDARD OUTPUT ({graph}):\n")
                file.write(result.stdout)
                file.write(f"ERROR({graph}):\n")
                file.write(result.stderr)
            print("End execution of algorithms applied for graph", graph)
        print("End Double Experiment!!")


if __name__ == "__main__":
    language_codes = ["python", "c++"]
    for i, code in enumerate(language_codes):
        print(f"{i}) {code}")
    code = language_codes[int(input("Enter the language code id: "))]
    if 'python' == code:
        DoubleExperimentExecutor().run(code, lambda: sys.executable)
    elif code == "c++":
        DoubleExperimentExecutor().run(code)
