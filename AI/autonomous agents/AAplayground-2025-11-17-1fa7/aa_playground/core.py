"""
core.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Shared data structures and enumerations for the drone playground.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional, Tuple


class Direction(Enum):
    """Cardinal directions for movement on a 2D grid."""

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def delta(self) -> Tuple[int, int]:
        """Return the `(dx, dy)` delta associated with the direction."""
        if self is Direction.UP:
            return (0, -1)
        if self is Direction.DOWN:
            return (0, 1)
        if self is Direction.LEFT:
            return (-1, 0)
        if self is Direction.RIGHT:
            return (1, 0)
        raise ValueError(f"Unhandled direction: {self}")  # pragma: no cover - defensive guard


class ActionType(Enum):
    """Enumeration of all base actions that an agent can request."""

    WAIT = auto()
    MOVE = auto()
    PICK_UP = auto()
    DROP = auto()
    USE = auto()
    PLANT = auto()
    WATER = auto()
    HARVEST = auto()


@dataclass(frozen=True)
class Action:
    """Request issued by an agent to the environment."""

    type: ActionType
    direction: Optional[Direction] = None
    item: Optional[str] = None
    metadata: Optional[Dict[str, object]] = None

    def with_metadata(self, **kwargs: object) -> "Action":
        """
        Return a copy of the action with the supplied metadata merged in.

        Parameters
        ----------
        **kwargs:
            Additional metadata values to attach to the action.
        """
        merged: Dict[str, object] = dict(self.metadata or {})
        merged.update(kwargs)
        return Action(type=self.type, direction=self.direction, item=self.item, metadata=merged)
