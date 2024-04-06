import networkit as nk
import numpy as np
import random
from diffusion_model import Diffusion_model


class SIR_model(Diffusion_model):
    _beta: float
    _gamma: float
    _infected_nodes: list
    _iterations_number: int

    def __init__(self, beta: float, gamma: float, infected_nodes: list, iterations_number: int):
        super().__init__()
        self._beta = beta
        self._gamma = gamma
        self._infected_nodes = infected_nodes
        self._iterations_number = iterations_number
        self.results = {}

    def run(self, graph: nk.Graph):
        # Initialize network nodes
        infected_nodes = {node for node in self._infected_nodes}
        infected_values = {node: 1 if node in self._infected_nodes else 0 for node in graph.iterNodes()}
        infected_times = {node: 0 for node in infected_values.keys()}
        recovered_times = {}
        infected_number = [len(self._infected_nodes)]
        recovered_number = [0]
        it_time = 0
        iterations_number = self._iterations_number
        total_infected_number = len(self._infected_nodes)
        total_recovered_number = 0

        while iterations_number > 0:
            #ASSERT iteration consistent
            assert iterations_number + it_time == self._iterations_number
            iterations_number -= 1
            it_time += 1
            node_to_infect = set()
            node_to_recover = set()
            for node in infected_nodes:
                for neighbor in graph.iterNeighbors(node):
                    # if neighbor is not just infected or ricovered
                    if infected_values[neighbor] not in [1, 2]:
                        # ASSERT infected value consistent
                        assert neighbor not in self._infected_nodes
                        # check if neighbor will infect
                        if random.random() < self._beta:
                            # if it will infect save the time and add mark it
                            total_infected_number += 1
                            infected_times[neighbor] = it_time
                            infected_values[neighbor] = 1
                            node_to_infect.add(neighbor)
                # recovered node with gamma probability
                if random.random() < self._gamma:
                    recovered_times[node] = it_time
                    infected_values[node] = 2
                    node_to_recover.add(node)
                    total_recovered_number += 1
            # ASSERT removed and added nodes consistent
            assert node_to_infect.isdisjoint(infected_nodes)
            assert node_to_recover.issubset(infected_nodes)
            assert all(infected_values[node] == 1 for node in node_to_infect)
            assert all(infected_values[node] == 2 for node in node_to_recover)
            assert all(any(neighbor in infected_nodes for neighbor in graph.iterNeighbors(node)) for node in node_to_infect)
            infected_nodes = infected_nodes.difference(node_to_recover)
            infected_nodes = infected_nodes.union(node_to_infect)
            assert all(infected_values[node] == 1 for node in infected_nodes)
            assert not any(value == 1 and node not in infected_nodes for node, value in infected_values.items())
            assert not any(value == 0 and node in infected_nodes for node, value in infected_values.items())
            assert not any(value == 2 and node in infected_nodes for node, value in infected_values.items())
            infected_number.append(total_infected_number)
            recovered_number.append(total_recovered_number)

        self._results = {"infected_times": infected_times, "recovered_times": recovered_times,
                        "infected_values": infected_values, "infected_number": infected_number, "recovered_number": recovered_number,
                        "total_infected_number": infected_number[-1], "current_infected_number": [i_n - r_n for i_n, r_n in zip(infected_number, recovered_number)]}

    def get_infected_times(self):
        return self._results['infected_times']

    def get_recovered_times(self):
        return self._results['recovered_times']

    def get_infected_values(self):
        return self._results['infected_values']

    def get_infected_number(self):
        return self._results['infected_number']

    def get_total_infected_number(self):
        return self._results['total_infected_number']
