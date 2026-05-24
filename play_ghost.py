import argparse
import random
from utils import load_trie

def is_valid_word(word: str, node_at_fragment: dict, fragment: str) -> bool:
    node = node_at_fragment
    for char in word[len(fragment):]:
        if char not in node:
            return False
        node = node[char]
    return "$" in node


def play(level):
    human_first = random.choice([True, False])
    label = "human" if human_first else "cpu"

    valid_node = load_trie("data/valid_words_trie.json")
    strategy_node = load_trie(f"data/cpu_strategy_{label}_first_{level}.json")

    print("=== GHOST ===")
    print("Take turns adding a letter to the fragment.")
    print("Complete a real word (4+ letters) and you lose.")
    print("Play an invalid prefix and you lose.\n")

    print(f"{'You go' if human_first else 'CPU goes'} first!\n")

    fragment = ""
    human_turn = human_first

    while True:
        print(f"Fragment: [{fragment or '...'}]")

        if human_turn:
            raw = input("Your move: ").strip()

            if len(raw) != 1 or not raw.isalpha():
                print("Enter a single letter.\n")
                continue

            letter = raw.upper()
            fragment += letter

            if letter not in valid_node:
                print(f"CPU challenges! Enter a valid word starting with '{fragment}': ", end="")
                word = input().strip().upper()
                while not word.startswith(fragment):
                    print(f"Enter a word starting with '{fragment}': ", end="")
                    word = input().strip().upper()
                print(f"[{word}] is not a valid word. You lose!\n")
                break

            valid_node = valid_node[letter]
            strategy_node = strategy_node.get(letter, {})

            if "$" in valid_node:
                print(f"[{fragment}] is a complete word. You lose!\n")
                break

            human_turn = False

        else:
            if not strategy_node:
                print(f"CPU challenges! Enter a valid word starting with '{fragment.lower()}': ", end="")
                word = input().strip().upper()
                while not word.startswith(fragment):
                    print(f"Enter a word starting with '{fragment}': ", end="")
                    word = input().strip().upper()
                if word.startswith(fragment) and is_valid_word(word, valid_node, fragment):
                    print(f"[{word.lower()}] is a valid word. CPU loses!\n")
                else:
                    print(f"[{word.lower()}] is not a valid word. You lose!\n")
                break

            letter = random.choice(list(strategy_node.keys()))
            fragment += letter
            valid_node = valid_node[letter]
            strategy_node = strategy_node[letter]
            print(f"CPU plays: {letter}")

            if "$" in valid_node:
                print(f"[{fragment}] is a complete word. CPU loses!\n")
                break

            human_turn = True

        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=["easy", "medium", "hard", "legendary"], default="medium")
    args = parser.parse_args()
    play(args.level)
