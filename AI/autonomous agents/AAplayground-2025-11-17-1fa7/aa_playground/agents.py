"""
agents.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Agent base classes and reference implementations for the playground.
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Optional, Tuple, TYPE_CHECKING

from .core import Action, ActionType, Direction

if TYPE_CHECKING:  # pragma: no cover - type checking aid
    from .environment import Observation


class BaseAgent:
    """Base class for controllers that act inside the playground."""

    def __init__(self, name: str = "Agent") -> None:
        """
        Store the agent name and initialise the registration slot.
        """
        self.name = name
        self.agent_id: Optional[int] = None

    @property
    def requires_interaction(self) -> bool:
        """
        Return `True` when the agent expects external input before advancing turns.
        """
        return False

    def has_pending_actions(self) -> bool:
        """
        Return `True` when the agent already queued actions to be executed.
        """
        return False

    def on_registered(self, agent_id: int) -> None:
        """
        Store the identifier assigned by the environment.
        """
        self.agent_id = agent_id

    def decide(self, observation: "Observation") -> Optional[Action]:
        """
        Produce the next action given the latest environment observation.

        By default the agent waits in place.
        """
        return Action(ActionType.WAIT)


class KeyboardDroneAgent(BaseAgent):
    """Agent controlled through keyboard input processed by the pygame loop."""

    def __init__(self, name: str = "Pilot") -> None:
        """
        Initialise the interactive agent with an empty action queue.
        """
        super().__init__(name=name)
        self._queued_actions: Deque[Action] = deque()

    @property
    def requires_interaction(self) -> bool:
        """
        Indicate that the agent requires manual confirmation to progress turns.
        """
        return True

    def has_pending_actions(self) -> bool:
        """
        Track whether any user-triggered actions are waiting to be executed.
        """
        return bool(self._queued_actions)

    def queue_action(self, action: Action) -> None:
        """
        Push a new action onto the queue.
        """
        self._queued_actions.append(action)

    def decide(self, observation: "Observation") -> Optional[Action]:
        """
        Pop the oldest queued action or wait when no input is available.
        """
        return self._queued_actions.popleft() if self._queued_actions else Action(ActionType.WAIT)


class BreadthFirstNavigator(BaseAgent):
    """
    Simple reference agent that uses breadth-first search to reach a navigation goal.
    """

    def __init__(self, name: str = "Navigator") -> None:
        """
        Initialise the agent and the reusable path buffer.
        """
        super().__init__(name=name)
        self._path: Deque[Direction] = deque()

    def decide(self, observation: "Observation") -> Optional[Action]:
        """
        Plan or replay a path to the goal tile, returning a single movement action.
        """
        if not self._path:
            goal = self._locate_goal(observation)
            if goal is None:
                return Action(ActionType.WAIT)
            self._path = self._plan_path(observation, goal)
        if not self._path:
            return Action(ActionType.WAIT)
        direction = self._path.popleft()
        return Action(ActionType.MOVE, direction=direction)

    def _locate_goal(self, observation: "Observation") -> Optional[Tuple[int, int]]:
        """
        Identify the goal tile location from the observation metadata.
        """
        for position, tile in observation.tiles.items():
            if tile.get("terrain") == "goal":
                return position
        return None

    def _plan_path(self, observation: "Observation", goal: Tuple[int, int]) -> Deque[Direction]:
        """
        Compute a shortest path from the agent position to the goal via BFS.
        """
        start = observation.position
        if start == goal:
            return deque()

        frontier: Deque[Tuple[int, int]] = deque([start])
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {start: start}

        while frontier:
            current = frontier.popleft()
            if current == goal:
                break
            for direction in Direction:
                dx, dy = direction.delta()
                neighbor = (current[0] + dx, current[1] + dy)
                tile_dict = observation.tiles.get(neighbor)
                if tile_dict is None:
                    continue
                terrain = tile_dict.get("terrain", "")
                # Tile is walkable if it's not an obstacle
                is_walkable = terrain not in ("obstacle", "base")
                if neighbor not in came_from and (is_walkable or neighbor == goal):
                    came_from[neighbor] = current
                    frontier.append(neighbor)

        if goal not in came_from:
            return deque()

        path: Deque[Direction] = deque()
        current = goal
        while current != start:
            previous = came_from[current]
            path.appendleft(self._direction_from_delta(previous, current))
            current = previous
        return path

    @staticmethod
    def _direction_from_delta(start: Tuple[int, int], end: Tuple[int, int]) -> Direction:
        """
        Convert the difference between two adjacent tiles into a direction enum value.
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        for direction in Direction:
            ddx, ddy = direction.delta()
            if (dx, dy) == (ddx, ddy):
                return direction
        raise ValueError(f"No direction matches delta {(dx, dy)}")  # pragma: no cover - defensive guard
