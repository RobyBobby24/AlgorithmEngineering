import networkit as nk


class Diffusion_model:
    _results: dict

    def __init__(self):
        self._results = {}

    def run(self, graph: nk.Graph):
        raise NotImplementedError("abstract method")

    def get_all_info(self):
        return self._results

    def get_info_by_name(self, info_name):
        return self._results[info_name]
