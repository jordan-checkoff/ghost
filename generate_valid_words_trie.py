import json
from utils import build_trie

def generate(words_path, output_path):
    with open(words_path) as f:
        words = [line.strip() for line in f if line.strip()]

    trie = build_trie(words)

    with open(output_path, "w") as f:
        json.dump(trie, f, separators=(",", ":"))
    print(f"Wrote {output_path} ({len(words)} words)")
