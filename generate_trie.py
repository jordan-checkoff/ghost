import json

MIN_WORD_LENGTH = 3


def build_trie(input_path, output_path):
    with open(input_path) as f:
        words = [line.strip() for line in f if line.strip()]

    root = {}
    for word in words:
        if len(word) <= MIN_WORD_LENGTH:
            continue
        node = root
        for char in word:
            if "$" in node:
                # prefix is already a complete word, skip this longer word
                break
            node = node.setdefault(char, {})
        else:
            node["$"] = {}  # marks end of a valid word

    with open(output_path, "w") as f:
        json.dump(root, f, separators=(",", ":"))


if __name__ == "__main__":
    build_trie("data/all_words.txt", "data/trie.json")
