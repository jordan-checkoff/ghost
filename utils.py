import json

MIN_WORD_LENGTH = 3


def load_trie(path):
    with open(path) as f:
        return json.load(f)


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
