import json
import os


class KnnParamSource:
    def __init__(self, track, params, **kwargs):
        if len(track.indices) == 1:
            default_index = track.indices[0].name
        else:
            default_index = "_all"

        self._index_name = params.get("index", default_index)
        self._cache = params.get("cache", False)
        self._params = params
        self._queries = []

        cwd = os.path.dirname(__file__)
        with open(os.path.join(cwd, "data/queries.json"), "r") as file:
            for line in file:
                self._queries.append(json.loads(line))
        self._iters = 0
        self.infinite = True

    def partition(self, partition_index, total_partitions):
        return self

    def params(self):
        result = {
            "index": self._index_name,
            "cache": self._params.get("cache", False),
            "size": self._params.get("k", 10),
            "body": {
                "knn": {
                    "field": "vector",
                    "query_vector": self._queries[self._iters],
                    "k": self._params.get("k", 10),
                    "num_candidates": self._params.get("num-candidates", 100),
                },
                "_source": False
            }
        }
        self._iters += 1
        if self._iters >= len(self._queries):
            self._iters = 0
        return result

def register(registry):
    registry.register_param_source("knn-param-source", KnnParamSource)

