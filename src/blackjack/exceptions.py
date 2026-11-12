"""Custom exception hierarchy.

Every Game error inherits from BlackjackError, so callers can catch "any game problem" with a single `except BlackjackError`.
"""

class BlackjackError(Exception):
    """Base class for all game errors."""

class InvalidActionError(BlackjackError):
    """The player tried an action that isnt allowed right now. (e.g hit before betting.)"""

class InvalidBetError(BlackjackError):
    """The bet amount is not allowed (too small, or not enough chips.)"""

class TooManyAttemptsError(BlackjackError):
    """The user typed invalid input too many times in a row."""
