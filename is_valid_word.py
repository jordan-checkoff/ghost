import json


def load_trie(path):
    with open(path) as f:
        return json.load(f)


def is_valid_word(trie, word):
    node = trie
    for char in word:
        if char not in node:
            return False
        node = node[char]
    return "$" in node


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python is_valid_word.py <word>")
        sys.exit(1)

    trie = load_trie("trie.json")
    word = sys.argv[1].upper()
    print(is_valid_word(trie, word))
