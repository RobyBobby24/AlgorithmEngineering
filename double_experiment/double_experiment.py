import subprocess
import strategies
import os
import sys
import json




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
            cls.instance.strategy = getattr(strategies, f"{cls.instance._configuration['strategy_name']}_strategy")
        return cls.instance

    def _interpeter_cmd(self, graph, partition, code_language, interpeter_func):
        interpeter_executable = interpeter_func()
        exe_file = self._configuration['languages_codes'][code_language]["exe_path"]
        undirected = self._configuration['languages_codes'][code_language]['undirected']
        cmd = [interpeter_executable, exe_file, "-g", graph, "-f", self._configuration["result_flag"]]
        if partition is not None:
            print("read partition mode")
            cmd += ["-p", partition]
        if undirected:
            print("undirected mode")
            cmd += ["-u"]

        return cmd

    def _compiled_cmd(self, graph, partition, code_language):
        exe_file = self._configuration['languages_codes'][code_language]["exe_path"]
        undirected = self._configuration['languages_codes'][code_language]['undirected']
        cmd = [exe_file, "-g", graph, "-f", self._configuration["result_flag"]]
        if partition is not None:
            print("read partition mode")
            cmd += ["-p", partition]
        if undirected:
            print("undirected mode")
            cmd += ["-u", "true"]

        return cmd

    def read_config(self, *keys):
        result = self._configuration
        for key in keys:
            result = result[key]
        return result

    def run(self, code_language, get_interpeter=None):
        graph_partitions = self.strategy(self)
        for graph, partition in graph_partitions:
            print("Start execution of algorithms applied for graph", graph, "with partition", partition)
            if get_interpeter != None:
                cmd = self._interpeter_cmd(graph, partition, code_language, get_interpeter)
            else:
                cmd = self._compiled_cmd(graph, partition, code_language)

            repetition = self._configuration["repetition"]
            for i in range(repetition):
                result = subprocess.run(cmd, capture_output=True, text=True)
                with open(self._configuration["log_file"], "a") as file:
                    file.write(f"STANDARD OUTPUT ({graph}):\n")
                    file.write(result.stdout)
                    file.write(f"ERROR({graph}):\n")
                    file.write(result.stderr)
                print(f"{i+1}/{repetition} done")
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
