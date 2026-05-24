import json


def load_trie(path):
    with open(path) as f:
        return json.load(f)
