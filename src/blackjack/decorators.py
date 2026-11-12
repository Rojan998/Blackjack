"""Our custom decorators - three flavours, from simple to advanced.

1. log_call          plain decorator (no arguments)
2. retry_on(...)     decorator WITH arguments (a "decorator factory")
3. requires_phase()  decorator factory designed for METHODS (uses `self`)
"""

import functools
import os
from collections.abc import Callable
from enum import Enum
from typing import Any

from blackjack.exceptions import InvalidActionError, TooManyAttemptsError

# Type alias: "any callable, any arguments, any return value".
Func = Callable[..., Any]

# Read once at import time. Turn on with:  BLACKJACK_DEBUG=1 uv run blackjack
DEBUG: bool = os.getenv("BLACKJACK_DEBUG") == "1"


# ---------------------------------------------------------------------------
# 1) Plain decorator: @log_call
# ---------------------------------------------------------------------------
def log_call(func: Func) -> Func:
    """Print every call and its return value - only when DEBUG is on."""

    @functools.wraps(func)  # keep func's __name__, __doc__, etc.
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # *args / **kwargs: accept ANY arguments, so this works on any function.
        if DEBUG:
            print(f"[debug] -> {func.__qualname__} args={args!r} kwargs={kwargs!r}")
        result = func(*args, **kwargs)  # call the ORIGINAL function
        if DEBUG:
            print(f"[debug] <- {func.__qualname__} returned {result!r}")
        return result

    return wrapper


# ---------------------------------------------------------------------------
# 2) Decorator with arguments: @retry_on(ValueError, attempts=5)
# ---------------------------------------------------------------------------
def retry_on(*exceptions: type[Exception], attempts: int = 3) -> Callable[[Func], Func]:
    """Re-run the function if it raises one of `exceptions`, up to `attempts` times.

    *exceptions -> collects ANY number of exception classes into a tuple
    attempts    -> keyword-only (it comes after *exceptions), so it must be named
    """
    if not exceptions:
        raise TypeError("retry_on() needs at least one exception type")

    def decorator(func: Func) -> Func:  # layer 2: receives the function
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:  # layer 3: runs on each call
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)  # success -> return immediately
                except exceptions as exc:  # `except` accepts a tuple of types
                    left = attempts - attempt
                    hint = (
                        f" ({left} {'try' if left == 1 else 'tries'} left)"
                        if left
                        else ""
                    )
                    print(f"  x {exc}{hint}")
            raise TooManyAttemptsError(f"Gave up after {attempts} invalid attempts.")

        return wrapper

    return decorator  # layer 1 returns the decorator


# ---------------------------------------------------------------------------
# 3) Decorator for methods: @requires_phase(GamePhase.PLAYER_TURN)
# ---------------------------------------------------------------------------
def requires_phase(*allowed: Enum) -> Callable[[Func], Func]:
    """Only allow the method to run when `self.phase` is one of `allowed`.

    Works on methods because the first positional argument of a method call
    is always the object itself (`self`).
    """

    def decorator(method: Func) -> Func:
        @functools.wraps(method)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            if self.phase not in allowed:
                needed = ", ".join(phase.value for phase in allowed)
                raise InvalidActionError(
                    f"Can't {method.__name__} right now "
                    f"(phase is '{self.phase.value}', needs: {needed})."
                )
            return method(self, *args, **kwargs)

        return wrapper

    return decorator
