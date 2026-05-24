# Ghost

Ghost is a word game where two players take turns adding letters to a growing fragment. The player who completes a real word (of 4 or more letters) loses. You also lose if you play a letter that makes the fragment impossible to extend into any valid word.

## Rules

- Players alternate adding one letter at a time to the fragment.
- If the fragment becomes a complete word (4+ letters), the player who played the last letter loses.
- If a player plays a letter that creates an invalid prefix (no valid word starts with it), the other player may challenge. The challenged player must name a valid word starting with the current fragment — if they can't, they lose; if they can, the challenger loses.

## Playing

```bash
uv run play_ghost.py --level medium
```

Levels: `easy`, `medium`, `hard`, `legendary`. Defaults to `medium`.

The game randomly decides who goes first. On your turn, type a single letter. The CPU plays optimally for its difficulty level.

## How it works

### Word list

`data/all_words.txt` is the source word list. Words of 3 letters or fewer are ignored (too short to lose on).

### Valid words trie

`data/valid_words_trie.json` is a trie built from every word in the word list. It's used at runtime to validate the human's moves — if a letter leads outside this trie, the prefix is invalid.

### CPU strategy trie

The CPU plays using a precomputed strategy trie, one per difficulty level and per starting player (e.g. `data/cpu_strategy_human_first_medium.json`).

It's built in two steps:

1. **Filter words by frequency.** Using [wordfreq](https://github.com/rspeer/wordfreq), words below a frequency threshold are removed. This defines what the CPU "knows." Lower threshold = harder CPU.

2. **Compute optimal play with minimax.** For each node in the filtered trie, we determine whether the player to move can force a win. A position is a win if there exists any move that puts the opponent in a losing position. The strategy trie stores only the CPU's winning moves at each turn, and all possible human responses (so the CPU is ready for anything the human plays).

When the human steers the game into a fragment the CPU has no strategy for (because it doesn't know any words with that prefix), the CPU issues a challenge instead.

### Difficulty levels

| Level | Frequency threshold | ~Word count |
|---|---|---|
| easy | 1e-6 | ~22k |
| medium | 1e-7 | ~54k |
| hard | 1e-8 | ~100k+ |
| legendary | 0 (all words) | ~170k |

Higher difficulty means the CPU knows more obscure words, making it harder to steer the fragment somewhere it can't handle.

## Regenerating data files

Install dependencies:

```bash
uv sync
```

Regenerate everything:

```bash
uv run generate_all.py
```

This produces `data/valid_words_trie.json` and strategy tries for all four levels and both starting players.

## Tuning difficulty

Thresholds are defined in `generate_all.py`:

```python
LEVELS = {
    "easy": 1e-6,
    "medium": 1e-7,
    "hard": 1e-8,
    "legendary": 0,
}
```

Adjust the thresholds and re-run `generate_all.py`. To add a new level, add an entry to `LEVELS` and add the name to the `--level` choices in `play_ghost.py`.
