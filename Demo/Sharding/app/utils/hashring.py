import hashlib
import bisect


class HashRing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas  # 각 노드당 가상 노드 수
        self.ring = dict()
        self.sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            virtual_node_key = f"{node}#{i}"
            hash_val = self._hash(virtual_node_key)
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)

    def remove_node(self, node):
        for i in range(self.replicas):
            virtual_node_key = f"{node}#{i}"
            hash_val = self._hash(virtual_node_key)
            self.ring.pop(hash_val, None)
            index = bisect.bisect_left(self.sorted_keys, hash_val)
            if index < len(self.sorted_keys) and self.sorted_keys[index] == hash_val:
                self.sorted_keys.pop(index)

    def get_node(self, key):
        if not self.ring:
            return None

        hash_val = self._hash(key)
        index = bisect.bisect_right(self.sorted_keys, hash_val)
        if index == len(self.sorted_keys):
            index = 0
        return self.ring[self.sorted_keys[index]]
