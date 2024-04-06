from os import listdir
from networkit import readGraph, Format
from SIR_model import SIR_model
import json


class Diffusion_Modell_Fectory:

    model_names = ["SIR"]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Diffusion_Modell_Fectory, cls).__new__(cls)
        return cls.instance

    def get_model(self, model_name):
        return getattr(self, f"_get_{model_name}")()

    def get_model_naes(self):
        return self.model_names

    def _get_model_SIR(self):
        return SIR_model(0.5, 0.2, [1], 100)


if __name__ == '__main__':
    for name in Diffusion_Modell_Fectory().get_modell_names():
        print(f"{name}\n")
    model_name = input("Enter the model name (above you can find some suggestions):")
    model = Diffusion_Modell_Fectory().get_model()

    for i, gp in enumerate(listdir("../graphs/")):
        print(f"{i + 1}) ../graphs/{gp}")
    graph_path = input("Enter the graph path (above you can find some suggestions):")
    G = readGraph(graph_path, Format.METIS)

    model.run(G)
    print(model.get_all_info())
