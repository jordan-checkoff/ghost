import json
from wordfreq import word_frequency
from utils import build_trie
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


def generate(words_path, output_path, cpu_first, threshold):
    with open(words_path) as f:
        all_words = [line.strip() for line in f if line.strip()]

    cpu_words = [w for w in all_words if word_frequency(w.lower(), "en") >= threshold]
    trie = build_trie(cpu_words)

    result = build(trie, cpu_first)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Wrote {output_path}")
