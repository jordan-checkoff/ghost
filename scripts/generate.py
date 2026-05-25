import json
from pathlib import Path

from wordfreq import word_frequency

ROOT = Path(__file__).parent.parent
WORDS_PATH = ROOT / "data/all_words.txt"
VALID_WORDS_TRIE_PATH = ROOT / "data/valid_words_trie.json"

LEVELS = {
    "easy": 1e-6,
    "medium": 1e-7,
    "hard": 1e-8,
    "legendary": 0,
}

def strategy_path(level: str, cpu_first: bool) -> Path:
    label = "cpu" if cpu_first else "human"
    return ROOT / f"data/cpu_strategy_{label}_first_{level}.json"


MIN_WORD_LENGTH = 3
_cache: dict[int, bool] = {}


def build_trie(words: list[str]) -> dict:
    root = {}
    for word in words:
        if len(word) <= MIN_WORD_LENGTH:
            continue
        node = root
        for char in word.upper():
            if "$" in node:
                break
            node = node.setdefault(char, {})
        else:
            node["$"] = {}
    return root


def save_trie(path: Path, trie: dict) -> None:
    with open(path, "w") as f:
        json.dump(trie, f, separators=(",", ":"))


def can_win(node: dict) -> bool:
    nid = id(node)
    if nid not in _cache:
        _cache[nid] = any("$" not in child and not can_win(child) for child in node.values())
    return _cache[nid]


def build_strategy(node: dict, cpu_turn: bool) -> dict:
    if cpu_turn:
        winnable_moves = {
            letter: child for letter, child in node.items()
            if "$" not in child and not can_win(child)
        }
        candidates = winnable_moves or node
    else:
        candidates = node

    return {
        letter: build_strategy(child, not cpu_turn)
        for letter, child in candidates.items()
    }


if __name__ == "__main__":
    with open(WORDS_PATH) as f:
        all_words = [line.strip() for line in f if line.strip()]

    trie = build_trie(all_words)
    save_trie(VALID_WORDS_TRIE_PATH, trie)
    print(f"Wrote {VALID_WORDS_TRIE_PATH} ({len(all_words)} words)")

    for level, threshold in LEVELS.items():
        _cache.clear()
        cpu_words = [w for w in all_words if word_frequency(w.lower(), "en") >= threshold]
        trie = build_trie(cpu_words)
        for cpu_first in (True, False):
            path = ROOT / strategy_path(level, cpu_first)
            save_trie(path, build_strategy(trie, cpu_first))
            print(f"Wrote {path}")
