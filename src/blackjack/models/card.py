"""Suit and Rank enums + the immutable Card model"""

from enum import StrEnum
from pydantic import BaseModel, ConfigDict, computed_field


class Suit(StrEnum):
    """The four suits. StrEnum members behave like strings."""

    HEARTS = "❤️"
    DIAMONDS = "◆"
    CLUBS = "♣️"
    SPADE = "♠️"


class Rank(StrEnum):
    """The Thirteen ranks"""

    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    @property
    def points(self) -> int:
        """Blackjack points for this rank (Ace counted as 11 here; Hand adjust it)."""
        if self is Rank.ACE:
            return 11
        if self in (Rank.JACK, Rank.QUEEN, Rank.KING):
            return 10
        return int(self.value)


class Card(BaseModel):
    """A Single playing card. frozen=True -> immutable and hashable."""

    model_config = ConfigDict(frozen=True)
    rank: Rank
    suit: Suit

    @computed_field
    @property
    def value(self) -> int:
        return self.rank.points

    @property
    def is_ace(self) -> bool:
        return self.rank is Rank.ACE

    def __str__(self) -> str:
        return f"{self.rank.value}{self.suit.value}"
