"""Build tree paths for hdfs logs"""
from typing import Generator, Tuple
import logging
import re
from hashlib import md5


class HdfsTreePaths:
    """Tree Paths for Hdfs files"""
    def __init__(self):
        """Initialize object"""
        self.domain = "hdfs://zalopaynewcluster"
        self.valid_path_pattern = re.compile(
            r"^hdfs://zalopaynewcluster/zalopay/[a-zA-Z0-9\+\=\[\]\.\:\/()!~&#@%_\s-]*$"
        )
        self.root_node = ("zalopay", md5("zalopay".encode()).hexdigest())
        self.graph = {}

    def append_file_path(self, file_path: str):
        """Split file path to nodes and insert these nodes to tree

        Parameters:
            file_path(str): path of file in HDFS
        """
        if self.valid_path_pattern.match(string=file_path) is None:
            logging.warning("Path is invalid [%s]", file_path)
            return
        list_nodes = [node for node in file_path[len(self.domain):].split("/") if node.strip()]
        for i, value in enumerate(list_nodes[:-1]):
            key = (value, md5("/".join(list_nodes[:i + 1]).encode()).hexdigest())
            if not self.graph.get(key):
                self.graph[key] = set()
            self.graph.get(key).add((
                list_nodes[i + 1], md5("/".join(list_nodes[:i + 2]).encode()).hexdigest())
            )

    def list_all_leaf_node_paths(self, current: Tuple, path: str) -> Generator[str, None, None]:
        """List all paths of leaf nodes in tree

        Parameters:
            current(tuple(node_name: str, id: str)): current node identified
                by node name and its hashed value
            path(str): init file path

        Return list of paths corresponding to leaf nodes
        """
        path += f"/{current[0]}"
        if not self.graph.get(current):
            yield path
        else:
            for node in self.graph[current]:
                yield from self.list_all_leaf_node_paths(current=node, path=path)
