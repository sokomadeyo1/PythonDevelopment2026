"""Bulls and cows game.
Letters with correctly guessed position are considered bulls;
guessed letters that appear in the secret word, for which the position is
guessed incorrectly are considered cows.
"""

import argparse
import random
from pathlib import Path
from urllib.request import urlopen
from cowsay import cowsay


def bullscows(guess: str, secret: str) -> (int, int):
    """Get the number of bulls and cows."""
    assert len(guess) == len(secret)
    l = len(guess)
    bulls = map(lambda a, b: a == b, guess, secret)
    n_bulls = list(bulls).count(True)
    cows = [guess[i] != secret[i] and guess[i] in secret for i in range(l)]
    n_cows = cows.count(True)
    return n_bulls, n_cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    """Main gameloop."""
    secret = random.choice(words)
    attempts = 0
    while True:
        guess = ask("Введите слово: ", words)
        attempts += 1
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if guess == secret:
            return attempts


def inform(format: str, *args) -> None:
    """Formatted output."""
    print(cowsay(format.format(*args)))


def ask(prompt: str, valid: list[str] = None) -> str:
    """Input a word from valid words list."""
    if valid is None:
        return input(prompt)
    while True:
        inp = input(prompt)
        if inp in valid:
            return inp
        else:
            print("Invalid input")


def parseargs() -> (list[str], int):
    """Parse cmdline args and read the dictionary."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dict",
        type=str,
        help="filename or a URL to the dictionary to be used in game",
    )
    parser.add_argument(
        "length",
        type=int,
        nargs="?",
        default=5,
        help="length of the words to be used in game",
    )
    args = parser.parse_args()

    path = args.dict
    dict = []
    dict_file = Path(path)
    if dict_file.exists():
        with open(path) as f:
            dict = [l.strip() for l in f.readlines()]
    elif path.startswith("http://") or path.startswith("https://"):
        with urlopen(path) as f:
            dict = [l.decode().strip() for l in f.readlines()]
    else:
        raise ValueError(f"file {path} not found")

    return dict, args.length


if __name__ == "__main__":
    dict, length = parseargs()
    dict_filtered = [word for word in dict if len(word) == length]
    attempts = gameplay(ask, inform, dict_filtered)
    print(f"Correct! You guessed the word in {attempts} attempts")
