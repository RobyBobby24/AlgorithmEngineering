import subprocess
import os
import sys


def filter_graph(keyword, root):
    result = []
    for i, gp in enumerate(os.listdir(root)):
        if keyword in gp:
            result.append(f"{root}{gp}")
    return result


if __name__ == "__main__":
    graph_dir = "2expnode"
    root = f"../graphs/{graph_dir}/"
    graph_paths = filter_graph("2expnode", root)
    language_codes = ["python", "c++"]
    python_executable = sys.executable
    for i, code in enumerate(language_codes):
        print(f"{i}) {code}")
    code = language_codes[int(input("Enter the language code id: "))]
    command = []
    for graph in graph_paths:
        if 'python' in code:
            command = [python_executable, r'../python_implementation/algorithms_implementation.py', "-g", graph, "-f", graph_dir]
        elif code == "c++":
            command = ["../c++_implementation/main", "-g", graph, "-f", graph_dir]
        result = subprocess.run(command, capture_output=True, text=True)
        with open("log.txt", "a") as file:
            file.write(f"STANDARD OUTPUT ({graph}):\n")
            file.write(result.stdout)
            file.write(f"ERROR({graph}):\n")
            file.write(result.stderr)
        print("End execution of algorithms applied for graph", graph)
    print("End Double Experiment!!")
