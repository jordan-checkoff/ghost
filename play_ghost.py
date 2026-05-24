import random
from utils import load_trie

def play():
    human_first = random.choice([True, False])
    label = "human" if human_first else "cpu"
    trie = load_trie(f"data/best_moves_{label}_first.json")

    print("=== GHOST ===")
    print("Take turns adding a letter to the fragment.")
    print("Complete a real word (4+ letters) and you lose.")
    print("Play an invalid prefix and you lose.\n")

    print(f"{'You go' if human_first else 'CPU goes'} first!\n")

    fragment = ""
    node = trie
    human_turn = human_first

    while True:
        print(f"Fragment: [{fragment or '...'}]")

        if human_turn:
            raw = input("Your move: ").strip()

            if len(raw) != 1 or not raw.isalpha():
                print("Enter a single letter.\n")
                continue

            letter = raw.upper()

            if letter not in node:
                print(f"'{(fragment + letter)}' is not a valid word prefix. You lose!\n")
                break

            fragment += letter
            node = node[letter]

            if "$" in node:
                print(f"[{fragment}] is a complete word. You lose!\n")
                break

            human_turn = False

        else:
            valid = [l for l in node if l != "$"]
            if not valid:
                print("CPU has no valid moves. CPU loses!\n")
                break

            letter = random.choice(valid)
            fragment += letter
            node = node[letter]
            print(f"CPU plays: {letter}")

            if "$" in node:
                print(f"[{fragment}] is a complete word. CPU loses!\n")
                break

            human_turn = True

        print()


if __name__ == "__main__":
    play()
