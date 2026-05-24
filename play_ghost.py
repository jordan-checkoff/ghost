import json
import random
import sys

def load_trie(path):
    with open(path) as f:
        return json.load(f)



def can_win(node: dict) -> bool:
    """True if the player to move from this node can force a win with optimal play."""
    return any("$" not in child and not can_win(child) for child in node.values())


def cpu_pick_letter(node: dict) -> str | None:
    winning_moves = [l for l, child in node.items() if "$" not in child and not can_win(child)]
    print(f"  [debug] winning moves: {[m.lower() for m in winning_moves]}")
    if winning_moves:
        return random.choice(winning_moves)
    safe_moves = [l for l, child in node.items() if "$" not in child]
    return random.choice(safe_moves) if safe_moves else random.choice(list(node)) if node else None


def play():
    try:
        trie = load_trie("trie.json")
    except FileNotFoundError:
        print("trie.json not found. Run generate_trie.py first.")
        sys.exit(1)

    print("=== GHOST ===")
    print("Take turns adding a letter to the fragment.")
    print("Complete a real word (4+ letters) and you lose.")
    print("Play an invalid prefix and you lose.\n")

    human_first = random.choice([True, False])
    print(f"{'You go' if human_first else 'CPU goes'} first!\n")

    fragment = ""
    node = trie
    human_turn = human_first

    while True:
        print(f"Fragment: [{fragment or '...'}]")

        if human_turn:
            raw = input("Your move: ").strip().lower()

            if len(raw) != 1 or not raw.isalpha():
                print("Enter a single letter.\n")
                continue

            letter = raw.upper()

            if letter not in node:
                print(f"'{(fragment + letter).lower()}' is not a valid word prefix. You lose!\n")
                break

            fragment += letter
            node = node[letter]

            if "$" in node:
                print(f"[{fragment.lower()}] is a complete word. You lose!\n")
                break

            human_turn = False

        else:
            letter = cpu_pick_letter(node)

            if letter is None:
                print("CPU has no valid moves. CPU loses!\n")
                break

            fragment += letter
            node = node[letter]
            print(f"CPU plays: {letter.lower()}")

            if "$" in node:
                print(f"[{fragment.lower()}] is a complete word. CPU loses!\n")
                break

            human_turn = True

        print()


if __name__ == "__main__":
    play()
