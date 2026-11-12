import random
from collections.abc import Iterator
from typing import Self

from blackjack.models.card import Card, Rank, Suit


class Deck:
    CARDS_PER_DECK = 52  # class attribute: shared by every Deck

    def __init__(self, num_decks: int = 1, *, seed: int | None = None) -> None:
        if num_decks < 1:
            raise ValueError("num_decks must be atleast 1")
        self.num_decks = num_decks
        self._rng = random.Random(seed)
        self._cards: list[Card] = []
        self.reset()

    # static method: needs neither self nor cls
    @staticmethod
    def build_single_deck() -> list[Card]:
        """52 Cards: nested comprehension over every suit x every rank"""
        return [Card(rank=rank, suit=suit) for suit in Suit for rank in Rank]

    # instance methods
    def reset(self) -> None:
        """Rebuild the full shoe and suffle it."""
        self._cards = [
            card for _ in range(self.num_decks) for card in self.build_single_deck()
        ]
        self.shuffle()

    def shuffle(self) -> None:
        self._rng.shuffle(self._cards)

    def draw(self) -> Card:
        """Take the top card: reshuffle a fresh shoe if empty."""
        if not self._cards:
            self.reset()
        return self._cards.pop()

    # dunder methods:
    def __len__(self) -> int:
        return len(self._cards)

    def __iter__(self) -> Iterator[Card]:
        yield from reversed(self._cards)

    def __repr__(self) -> str:
        return f"Deck(num_decks={self.num_decks}, remaning={len(self)})"
