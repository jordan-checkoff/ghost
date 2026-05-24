import json
from utils import load_trie

_cache: dict[int, bool] = {}

def can_win(node: dict) -> bool:
    nid = id(node)
    if nid not in _cache:
        _cache[nid] = any("$" not in child and not can_win(child) for child in node.values())
    return _cache[nid]


def build(node: dict, cpu_turn: bool) -> dict:
    if cpu_turn:
        winnable_moves = {
            l: child for l, child in node.items()
            if "$" not in child and not can_win(child)
        }
        candidates = winnable_moves or node
    else:
        candidates = node

    return {
        l: build(child, not cpu_turn)
        for l, child in candidates.items()
    }


def main():
    trie = load_trie("data/trie.json")

    for cpu_first in (True, False):
        label = "cpu" if cpu_first else "human"
        print(f"Building best-moves trie ({label} first)...")
        result = build(trie, cpu_first)
        path = f"data/best_moves_{label}_first.json"
        with open(path, "w") as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
