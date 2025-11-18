"""
sample_agents/random_agent.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Minimal drone agent that chooses random moves each turn.
"""

from __future__ import annotations

import random
from typing import Optional

from aa_playground import Action, ActionType, BaseAgent, Direction, Observation


class RandomAgent(BaseAgent):
    """Agent that issues random move commands."""

    def __init__(self, name: str = "RandomAgent") -> None:
        super().__init__(name=name)
        self._rng = random.Random()

    def decide(self, observation: Observation) -> Optional[Action]:
        print(f"Observation received: {observation}")
        direction = self._rng.choice(list(Direction))
        return Action(ActionType.MOVE, direction=direction)
