"""Bulls and cows game.
Letters with correctly guessed position are considered bulls;
guessed letters that appear in the secret word, for which the position is
guessed incorrectly are considered cows.
"""


def bullscows(guess: str, secret: str) -> (int, int):
    """Get the number of bulls and cows."""
    assert len(guess) == len(secret)
    l = len(guess)
    bulls = map(lambda a, b: a == b, guess, secret)
    n_bulls = list(bulls).count(True)
    cows = [guess[i] != secret[i] and guess[i] in secret for i in range(l)]
    n_cows = cows.count(True)
    return n_bulls, n_cows
