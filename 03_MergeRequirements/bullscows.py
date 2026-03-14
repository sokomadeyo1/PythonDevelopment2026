"""Bulls and cows game.
Letters with correctly guessed position are considered bulls;
guessed letters that appear in the secret word, for which the position is
guessed incorrectly are considered cows.
"""

import random


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
    print(format.format(*args))


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
