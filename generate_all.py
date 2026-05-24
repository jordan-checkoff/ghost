from generate_valid_words_trie import generate as generate_valid_words
from generate_cpu_strategy_trie import generate as generate_cpu_strategy

WORDS_PATH = "data/all_words.txt"
VALID_WORDS_TRIE_PATH = "data/valid_words_trie.json"

LEVELS = {
    "easy": 1e-6,
    "medium": 1e-7,
    "hard": 1e-8,
    "legendary": 0,
}

if __name__ == "__main__":
    generate_valid_words(words_path=WORDS_PATH, output_path=VALID_WORDS_TRIE_PATH)

    for level, threshold in LEVELS.items():
        for cpu_first in (True, False):
            label = "cpu" if cpu_first else "human"
            output_path = f"data/cpu_strategy_{label}_first_{level}.json"
            generate_cpu_strategy(words_path=WORDS_PATH, output_path=output_path, cpu_first=cpu_first, threshold=threshold)
