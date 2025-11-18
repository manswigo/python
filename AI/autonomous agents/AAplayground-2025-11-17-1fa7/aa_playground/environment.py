"""
environment.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Core grid-world environment and the drone farming scenarios.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional, Tuple, TYPE_CHECKING

from .core import Action, ActionType, Direction

if TYPE_CHECKING:  # pragma: no cover - type checking aid
    from .agents import BaseAgent


@dataclass
class Tile:
    """Mutable representation of a single grid cell."""

    terrain: str = "plain"
    blocking: bool = False
    items: Dict[str, int] = field(default_factory=dict)
    agents: List[int] = field(default_factory=list)

    def is_walkable(self) -> bool:
        """Return `True` when the tile can be entered by an agent."""
        return not self.blocking and not self.agents

    def add_item(self, item: str, amount: int = 1) -> None:
        """
        Place one or more units of an item on the tile.

        Parameters
        ----------
        item:
            Item name.
        amount:
            Quantity to add (default `1`).
        """
        self.items[item] = self.items.get(item, 0) + amount
        if self.items[item] <= 0:
            del self.items[item]

    def remove_item(self, item: str, amount: int = 1) -> bool:
        """
        Remove one or more units of an item if available.

        Returns
        -------
        bool
            `True` when the removal succeeded, `False` otherwise.
        """
        if self.items.get(item, 0) < amount:
            return False
        self.items[item] -= amount
        if self.items[item] == 0:
            del self.items[item]
        return True


@dataclass(frozen=True)
class TileView:
    """Immutable snapshot of a tile presented to an agent."""

    position: Tuple[int, int]
    terrain: str
    items: Dict[str, int]
    agent_present: bool
    walkable: bool
    metadata: Dict[str, object]


@dataclass(frozen=True)
class Observation:
    """Observation bundle delivered to an agent before it decides an action."""

    turn: int
    time_remaining: Optional[int]
    position: Tuple[int, int]
    inventory: Dict[str, int]
    tiles: Dict[Tuple[int, int], Dict[str, str]]
    width: int
    height: int


@dataclass
class AgentState:
    """Runtime state tracked for each registered agent."""

    agent_id: int
    name: str
    controller: "BaseAgent"
    position: Tuple[int, int]
    inventory: Dict[str, int] = field(default_factory=dict)

    def add_item(self, item: str, amount: int = 1) -> None:
        """
        Add items to the agent inventory, removing the key when the count reaches zero.
        """
        self.inventory[item] = self.inventory.get(item, 0) + amount
        if self.inventory[item] <= 0:
            del self.inventory[item]

    def remove_item(self, item: str, amount: int = 1) -> bool:
        """
        Remove items from the agent inventory if enough units are available.
        """
        if self.inventory.get(item, 0) < amount:
            return False
        self.inventory[item] -= amount
        if self.inventory[item] == 0:
            del self.inventory[item]
        return True


class GridWorld:
    """Base implementation of a 2D grid world supporting multiple agents."""

    def __init__(self, width: int, height: int, *, max_turns: Optional[int] = None) -> None:
        """
        Initialise the grid world with blank tiles.

        Parameters
        ----------
        width, height:
            Grid dimensions.
        max_turns:
            Optional episode length cap. `None` means unlimited turns.
        """
        self.width = width
        self.height = height
        self.max_turns = max_turns
        self.turn = 0

        self._grid: List[List[Tile]] = [
            [Tile() for _ in range(width)] for _ in range(height)
        ]
        self._agents: Dict[int, AgentState] = {}
        self._next_agent_id = 1

    def in_bounds(self, position: Tuple[int, int]) -> bool:
        """Return `True` when the supplied position lies inside the grid."""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile(self, position: Tuple[int, int]) -> Tile:
        """Return the mutable tile instance at the given position."""
        if not self.in_bounds(position):
            raise ValueError(f"Position {position} is outside the grid.")
        x, y = position
        return self._grid[y][x]

    def scatter_items(self, position: Tuple[int, int], item: str, amount: int = 1) -> None:
        """Convenience helper to deposit resources on a tile."""
        self.get_tile(position).add_item(item, amount)

    def register_agent(
        self,
        agent: "BaseAgent",
        position: Tuple[int, int],
        *,
        inventory: Optional[Dict[str, int]] = None,
    ) -> int:
        """
        Register an agent controller and place it on the grid.

        Returns
        -------
        int
            The unique agent identifier assigned to the controller.
        """
        if not self.in_bounds(position):
            raise ValueError(f"Cannot place agent at out-of-bounds position {position}.")

        tile = self.get_tile(position)
        if not tile.is_walkable():
            raise ValueError(f"Tile {position} is not walkable.")

        agent_id = self._next_agent_id
        self._next_agent_id += 1

        state = AgentState(
            agent_id=agent_id,
            name=agent.name,
            controller=agent,
            position=position,
            inventory=dict(inventory or {}),
        )
        self._agents[agent_id] = state
        tile.agents.append(agent_id)
        agent.on_registered(agent_id)
        return agent_id

    @property
    def agent_states(self) -> Dict[int, AgentState]:
        """Return the mutable mapping of agent identifiers to their state."""
        return self._agents

    def step(self) -> None:
        """Advance the simulation by a single turn."""
        if not self._agents:
            return

        for agent_id in list(self._agents.keys()):
            state = self._agents.get(agent_id)
            if state is None:
                continue
            observation = self._build_observation(agent_id)
            action = state.controller.decide(observation)
            self.execute_action(agent_id, action)

        self.after_step()
        self.turn += 1

    def run(self, steps: Optional[int] = None) -> None:
        """Run the simulation for a fixed amount of steps or until termination."""
        iterations = steps if steps is not None else self.max_turns
        while iterations is None or iterations > 0:
            if self.max_turns is not None and self.turn >= self.max_turns:
                break
            self.step()
            if iterations is not None:
                iterations -= 1

    def execute_action(self, agent_id: int, action: Optional[Action]) -> None:
        """Resolve an agent action by delegating to the appropriate handler."""
        if action is None:
            return

        state = self._agents.get(agent_id)
        if state is None:
            return

        if action.type == ActionType.WAIT:
            return
        if action.type == ActionType.MOVE:
            if not action.direction:
                return
            self._move_agent(agent_id, action.direction)
            return
        if action.type == ActionType.PICK_UP:
            self._pickup_item(state, action.item)
            return
        if action.type == ActionType.DROP:
            self._drop_item(state, action.item)
            return
        if action.type == ActionType.USE:
            self.handle_use(state, action)
            return

        if not self.handle_custom_action(state, action):
            # Unsupported action type; ignore silently.
            return

    def handle_use(self, state: AgentState, action: Action) -> None:
        """Hook implemented by subclasses to react to `ActionType.USE`."""

    def handle_custom_action(self, state: AgentState, action: Action) -> bool:
        """
        Allow subclasses to implement bespoke action handling.

        Returns
        -------
        bool
            `True` when the action was processed, `False` to fall back to the
            default handling.
        """
        return False

    def after_step(self) -> None:
        """Hook executed after all agents have acted in the current turn."""

    def tile_metadata(self, position: Tuple[int, int]) -> Dict[str, object]:
        """Return supplementary information for observers."""
        return {}

    # -- internal helpers -------------------------------------------------

    def _move_agent(self, agent_id: int, direction: Direction) -> None:
        """Move the agent in the specified direction if the target tile is walkable."""
        state = self._agents.get(agent_id)
        if state is None:
            return

        dx, dy = direction.delta()
        new_position = (state.position[0] + dx, state.position[1] + dy)
        if not self.in_bounds(new_position):
            return
        target_tile = self.get_tile(new_position)
        if not target_tile.is_walkable():
            return

        current_tile = self.get_tile(state.position)
        if agent_id in current_tile.agents:
            current_tile.agents.remove(agent_id)
        target_tile.agents.append(agent_id)
        state.position = new_position

    def _pickup_item(self, state: AgentState, item_name: Optional[str]) -> None:
        """Transfer an item from the tile to the agent, if available."""
        tile = self.get_tile(state.position)
        if not tile.items:
            return
        name = item_name or next(iter(tile.items.keys()))
        if tile.remove_item(name):
            state.add_item(name)

    def _drop_item(self, state: AgentState, item_name: Optional[str]) -> None:
        """Drop a single unit of an item from the agent inventory to the tile."""
        if not item_name or item_name not in state.inventory:
            return
        if state.remove_item(item_name):
            tile = self.get_tile(state.position)
            tile.add_item(item_name)

    def _build_observation(self, agent_id: int) -> Observation:
        """
        Construct the observation bundle delivered to the agent controller.
        Only includes the current position and immediate neighbors (4-connected).
        """
        state = self._agents[agent_id]
        tiles: Dict[Tuple[int, int], Dict[str, str]] = {}
        
        # Include current position
        current_pos = state.position
        positions_to_include = [current_pos]
        
        # Include only immediate neighbors (4-connected: up, down, left, right)
        for direction in Direction:
            dx, dy = direction.delta()
            neighbor_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if self.in_bounds(neighbor_pos):
                positions_to_include.append(neighbor_pos)
        
        # Build simplified tile dict with just terrain info
        for position in positions_to_include:
            x, y = position
            tile = self._grid[y][x]
            metadata = self.tile_metadata(position)
            
            # Determine terrain string based on tile state
            terrain_str = self._get_terrain_string(tile, metadata)
            tiles[position] = {"terrain": terrain_str}

        time_remaining: Optional[int] = None
        if self.max_turns is not None:
            time_remaining = max(self.max_turns - self.turn, 0)

        return Observation(
            turn=self.turn,
            time_remaining=time_remaining,
            position=state.position,
            inventory=dict(state.inventory),
            tiles=tiles,
            width=self.width,
            height=self.height,
        )

    def _get_terrain_string(self, tile: Tile, metadata: Dict[str, object]) -> str:
        """
        Convert tile and metadata into a simple terrain string.
        """
        # Check for special tiles first
        if metadata.get("obstacle"):
            return "obstacle"
        if metadata.get("launch_pad"):
            return "base"
        if metadata.get("goal"):
            return "goal"
        
        # Check soil status for farmable tiles
        soil = metadata.get("soil")
        if soil and isinstance(soil, dict):
            stage = soil.get("stage")
            if stage == "seed":
                return "seed"
            elif stage == "growing":
                return "growing"
            elif stage == "ready":
                return "ready"
            elif stage == "weed":
                return "weed"
            elif stage == "empty":
                return "empty"
        
        # Check if not farmable
        if not metadata.get("farmable", True):
            return "non-farmable"
        
        # Default to empty for farmable tiles
        return "empty"


class CropStage(str, Enum):
    """Possible lifecycle stages for a crop tile or obstructed soil."""

    EMPTY = "empty"
    PLANTED = "seed"
    GROWING = "growing"
    READY = "ready"
    WEED = "weed"


@dataclass
class SoilPlot:
    """Mutable state describing a single patch of soil."""

    stage: CropStage = CropStage.EMPTY
    growth: int = 0
    hydration: int = 0
    dry_turns: int = 0

    def reset(self) -> None:
        """Reset the plot to an empty, dry state."""
        self.stage = CropStage.EMPTY
        self.growth = 0
        self.hydration = 0
        self.dry_turns = 0

    @property
    def needs_water(self) -> bool:
        """Return `True` when the plot requires watering."""
        return self.stage in {CropStage.PLANTED, CropStage.GROWING} and self.hydration <= 0

    def to_metadata(self) -> Dict[str, object]:
        """Return a serialisable view of the plot for observers."""
        return {
            "stage": self.stage.value,
            "growth": self.growth,
            "hydration": self.hydration,
            "dry_turns": self.dry_turns,
            "needs_water": self.needs_water,
        }


class DroneField(GridWorld):
    """
    Drone-based farming environment combining planting, watering, and harvesting actions.
    """

    def __init__(
        self,
        width: int,
        height: int,
        *,
        max_turns: int = 120,
        growth_threshold_seedling: int = 2,
        growth_threshold_mature: int = 3,
        max_hydration: int = 3,
        water_source_capacity: int = 5,
        seed_spawn_rate: int = 1,
        battery_capacity: int = 80,
        idle_cost: int = 1,
        move_cost: int = 2,
        action_cost: int = 3,
        recharge_rate: int = 5,
        base_position: Optional[Tuple[int, int]] = None,
    ) -> None:
        """
        Create the environment and seed default resource tiles.
        """
        super().__init__(width, height, max_turns=max_turns)
        self._soil: List[List[SoilPlot]] = [
            [SoilPlot() for _ in range(width)] for _ in range(height)
        ]

        self.growth_threshold_seedling = growth_threshold_seedling
        self.growth_threshold_mature = growth_threshold_mature
        self.max_hydration = max_hydration
        self.water_source_capacity = water_source_capacity
        self.seed_spawn_rate = seed_spawn_rate

        self.total_harvested = 0
        self.turns_since_last_seed_spawn = 0

        self.base_position = base_position or (width - 1, 0)
        self.battery_capacity = battery_capacity
        self.idle_cost = idle_cost
        self.move_cost = move_cost
        self.action_cost = action_cost
        self.recharge_rate = recharge_rate
        self._battery: Dict[int, int] = {}

        # Resource tiles along the bottom edge by default.
        bottom_row = height - 1
        self.water_sources: List[Tuple[int, int]] = [(width // 2, bottom_row)]
        self.seed_supply: List[Tuple[int, int]] = [(0, bottom_row)]

        self._farmable: List[List[bool]] = [
            [True for _ in range(width)] for _ in range(height)
        ]

        for pos in self.water_sources + self.seed_supply:
            self._farmable[pos[1]][pos[0]] = False

        for position in self.water_sources:
            self.scatter_items(position, "water", self.water_source_capacity)
        for position in self.seed_supply:
            self.scatter_items(position, "seed", self.seed_spawn_rate)

        base_tile = self.get_tile(self.base_position)
        base_tile.terrain = "launch_pad"
        self._farmable[self.base_position[1]][self.base_position[0]] = False

    def register_agent(
        self,
        agent: "BaseAgent",
        position: Tuple[int, int],
        *,
        inventory: Optional[Dict[str, int]] = None,
    ) -> int:
        """Register the agent and initialise its battery."""
        agent_id = super().register_agent(agent, position, inventory=inventory)
        self._battery[agent_id] = self.battery_capacity
        return agent_id

    def execute_action(self, agent_id: int, action: Optional[Action]) -> None:
        """Resolve the action while applying energy costs to drone agents."""
        if agent_id not in self._battery:
            super().execute_action(agent_id, action)
            return

        if self._battery[agent_id] <= 0:
            super().execute_action(agent_id, Action(ActionType.WAIT))
            return

        starting_battery = self._battery[agent_id]
        super().execute_action(agent_id, action)

        cost = self.idle_cost
        if action is not None:
            if action.type == ActionType.MOVE:
                cost = self.move_cost
            elif action.type in {ActionType.PLANT, ActionType.WATER, ActionType.HARVEST}:
                cost = self.action_cost

        self._battery[agent_id] = max(starting_battery - cost, 0)

    def after_step(self) -> None:
        """Advance crop growth, replenish resources, and recharge drones on the pad."""
        self._advance_crops()
        self._replenish_resources()
        for agent_id, state in self.agent_states.items():
            if agent_id not in self._battery:
                continue
            if state.position == self.base_position:
                self._battery[agent_id] = min(
                    self.battery_capacity, self._battery[agent_id] + self.recharge_rate
                )

    def tile_metadata(self, position: Tuple[int, int]) -> Dict[str, object]:
        """Include soil information and launch pad markers for each tile."""
        x, y = position
        soil = self._soil[y][x]
        return {
            "soil": soil.to_metadata() if self._farmable[y][x] else None,
            "farmable": self._farmable[y][x],
            "launch_pad": position == self.base_position,
        }

    def battery_level(self, agent_id: int) -> int:
        """Return the current battery level for the agent."""
        return self._battery.get(agent_id, self.battery_capacity)

    def summary(self) -> Dict[str, object]:
        """Return a concise snapshot of the simulation."""
        weed_plots = sum(
            1
            for row in self._soil
            for soil in row
            if soil.stage is CropStage.WEED
        )
        return {
            "turn": self.turn,
            "total_harvested": self.total_harvested,
            "weed_plots": weed_plots,
        }

    def is_farmable(self, position: Tuple[int, int]) -> bool:
        """Return `True` when the position is a plot that can hold crops."""
        x, y = position
        return self._farmable[y][x]

    # -- crop interactions -------------------------------------------------

    def _handle_plant(self, state: AgentState, soil: SoilPlot) -> bool:
        """Plant a seed if the soil is empty and the agent has seeds."""
        if soil.stage not in {CropStage.EMPTY}:
            return False
        if "seed" not in state.inventory:
            return False
        if not state.remove_item("seed"):
            return False
        soil.stage = CropStage.PLANTED
        soil.growth = 0
        soil.hydration = max(soil.hydration, 1)
        soil.dry_turns = 0
        return True

    def _handle_water(self, state: AgentState, soil: SoilPlot) -> bool:
        """Water a planted or growing crop if water is available."""
        if soil.stage not in {CropStage.PLANTED, CropStage.GROWING}:
            return False
        if "water" not in state.inventory:
            return False
        if not state.remove_item("water"):
            return False
        soil.hydration = min(self.max_hydration, soil.hydration + 2)
        soil.dry_turns = 0
        return True

    def _handle_harvest(self, state: AgentState, soil: SoilPlot) -> bool:
        """Harvest a ready crop and reset the soil plot."""
        if soil.stage is CropStage.READY:
            soil.reset()
            state.add_item("crop")
            self.total_harvested += 1
            return True
        if soil.stage is CropStage.WEED:
            soil.reset()
            return True
        return False

    def handle_custom_action(self, state: AgentState, action: Action) -> bool:  # type: ignore[override]
        """Process planting, watering, and harvesting requests."""
        position = state.position
        if not self.is_farmable(position):
            return False
        soil = self._soil[position[1]][position[0]]

        if action.type == ActionType.PLANT:
            return self._handle_plant(state, soil)
        if action.type == ActionType.WATER:
            return self._handle_water(state, soil)
        if action.type == ActionType.HARVEST:
            return self._handle_harvest(state, soil)
        return False

    # -- lifecycle helpers ------------------------------------------------

    def _advance_crops(self) -> None:
        """Progress crop growth based on hydration and stage thresholds."""
        for y, row in enumerate(self._soil):
            for x, soil in enumerate(row):
                if not self._farmable[y][x]:
                    continue
                if soil.stage in {CropStage.EMPTY, CropStage.WEED}:
                    soil.dry_turns = 0
                    continue
                if soil.hydration > 0:
                    soil.growth += 1
                    soil.hydration -= 1
                    soil.dry_turns = 0
                else:
                    soil.dry_turns += 1

                if soil.stage == CropStage.PLANTED and soil.growth >= self.growth_threshold_seedling:
                    soil.stage = CropStage.GROWING
                    soil.growth = 0
                    soil.dry_turns = 0
                elif soil.stage == CropStage.GROWING and soil.growth >= self.growth_threshold_mature:
                    soil.stage = CropStage.READY
                    soil.growth = 0
                    soil.dry_turns = 0
                elif soil.stage in {CropStage.PLANTED, CropStage.GROWING} and soil.dry_turns >= 2:
                    soil.stage = CropStage.WEED
                    soil.growth = 0
                    soil.hydration = 0

    def _replenish_resources(self) -> None:
        """Top up resource tiles with water and seeds."""
        for position in self.water_sources:
            tile = self.get_tile(position)
            current = tile.items.get("water", 0)
            if current < self.water_source_capacity:
                tile.add_item("water", self.water_source_capacity - current)

        self.turns_since_last_seed_spawn += 1
        if self.turns_since_last_seed_spawn >= 3:
            for position in self.seed_supply:
                tile = self.get_tile(position)
                tile.add_item("seed", self.seed_spawn_rate)
            self.turns_since_last_seed_spawn = 0


class DronePlantingField(DroneField):
    """Planting-focused variant where crops mature automatically and remain indefinitely."""

    def __init__(
        self,
        width: int = 8,
        height: int = 6,
        *,
        max_turns: int = 120,
        seed_turns: int = 2,
        growing_turns: int = 3,
        obstacles: Optional[Iterable[Tuple[int, int]]] = None,
    ) -> None:
        """Initialise the planting challenge with automatic crop growth."""
        super().__init__(
            width,
            height,
            max_turns=max_turns,
            growth_threshold_seedling=seed_turns,
            growth_threshold_mature=growing_turns,
            max_hydration=0,
            water_source_capacity=0,
            seed_spawn_rate=2,
            battery_capacity=float("inf"),
        )
        self.seed_turns = max(1, seed_turns)
        self.growing_turns = max(1, growing_turns)
        self.grown_plots: set[tuple[int, int]] = set()
        obstacle_positions = set(obstacles or self._default_obstacles(width, height))
        self._planting_obstacles: Dict[Tuple[int, int], bool] = {}
        self._place_obstacles(obstacle_positions)

    def _handle_plant(self, state: AgentState, soil: SoilPlot) -> bool:  # type: ignore[override]
        """Plant a seed without introducing hydration requirements."""
        if soil.stage is not CropStage.EMPTY:
            return False
        if "seed" not in state.inventory:
            state.inventory["seed"] = float("inf")
        soil.stage = CropStage.PLANTED
        soil.growth = 0
        soil.hydration = 0
        soil.dry_turns = 0
        return True

    def _handle_water(self, state: AgentState, soil: SoilPlot) -> bool:  # type: ignore[override]
        """Disable watering – crops grow without hydration in this challenge."""
        return False

    def _handle_harvest(self, state: AgentState, soil: SoilPlot) -> bool:  # type: ignore[override]
        """Prevent harvesting – grown crops remain as persistent planted cells."""
        if soil.stage is CropStage.WEED:
            soil.reset()
            return True
        return False

    def _advance_crops(self) -> None:  # type: ignore[override]
        """Progress planted crops to the grown stage without hydration requirements."""
        for y, row in enumerate(self._soil):
            for x, soil in enumerate(row):
                if not self._farmable[y][x]:
                    continue
                position = (x, y)
                if soil.stage is CropStage.EMPTY:
                    continue
                if soil.stage is CropStage.WEED:
                    continue
                if soil.stage is CropStage.PLANTED:
                    soil.growth = min(soil.growth + 1, self.seed_turns)
                    if soil.growth >= self.seed_turns:
                        soil.stage = CropStage.GROWING
                        soil.growth = 0
                elif soil.stage is CropStage.GROWING:
                    soil.growth = min(soil.growth + 1, self.growing_turns)
                    if soil.growth >= self.growing_turns:
                        soil.stage = CropStage.READY
                        soil.growth = 0
                        self.grown_plots.add(position)
                elif soil.stage is CropStage.READY:
                    self.grown_plots.add(position)

    def tile_metadata(self, position: Tuple[int, int]) -> Dict[str, object]:  # type: ignore[override]
        """Expose planting challenge metadata for HUDs and agents."""
        metadata = super().tile_metadata(position)
        soil_meta = metadata.get("soil")
        metadata.update(
            {
                "grown_crop": position in self.grown_plots,
                "weed": bool(soil_meta and soil_meta.get("stage") == CropStage.WEED.value),
                "obstacle": position in self._planting_obstacles,
            }
        )
        return metadata

    def summary(self) -> Dict[str, object]:  # type: ignore[override]
        """Include the number of grown plots in the simulation summary."""
        data = super().summary()
        data.update(
            {
                "grown_plots": len(self.grown_plots),
                "seed_turns": self.seed_turns,
                "growing_turns": self.growing_turns,
                "obstacle_count": len(self._planting_obstacles),
            }
        )
        return data

    def register_agent(  # type: ignore[override]
        self,
        agent: "BaseAgent",
        position: Tuple[int, int],
        *,
        inventory: Optional[Dict[str, int]] = None,
    ) -> int:
        """Register the agent and grant infinite seeds."""
        agent_id = super().register_agent(agent, position, inventory=inventory)
        state = self.agent_states[agent_id]
        state.inventory["seed"] = float("inf")
        self._battery[agent_id] = float("inf")
        return agent_id

    @staticmethod
    def _default_obstacles(width: int, height: int) -> set[Tuple[int, int]]:
        """Generate a few static tree obstacles for the planting field."""
        obstacles: set[Tuple[int, int]] = set()
        if width < 4 or height < 4:
            return obstacles
        mid_y = max(1, height // 2)
        for x in range(1, width, 3):
            obstacles.add((x, mid_y))
        for y in range(2, height, 4):
            obstacles.add((width // 2, y))
        return obstacles

    def _place_obstacles(self, obstacles: Iterable[Tuple[int, int]]) -> None:
        """Mark obstacle tiles as trees and make them non-farmable."""
        for position in obstacles:
            if not self.in_bounds(position):
                continue
            if position == self.base_position:
                continue
            tile = self.get_tile(position)
            tile.blocking = True
            tile.terrain = "tree"
            self._farmable[position[1]][position[0]] = False
            self._soil[position[1]][position[0]].reset()
            self._planting_obstacles[position] = True

    def planting_obstacles(self) -> List[Tuple[int, int]]:
        """Return the list of obstacle coordinates."""
        return list(self._planting_obstacles.keys())


class DroneNavigationField(DroneField):
    """Variant of the drone field containing static obstacles and a navigation goal."""

    def __init__(
        self,
        width: int = 8,
        height: int = 6,
        *,
        layout: Optional[Iterable[str]] = None,
        obstacles: Optional[Iterable[Tuple[int, int]]] = None,
        start_position: Optional[Tuple[int, int]] = None,
        goal_position: Optional[Tuple[int, int]] = None,
        max_turns: int = 120,
    ) -> None:
        """Initialise the navigation challenge with optional custom layout."""
        grid_width = width
        grid_height = height
        layout_rows: Optional[List[str]] = None
        if layout is not None:
            layout_rows = list(layout)
            if layout_rows:
                row_length = len(layout_rows[0])
                for index, row in enumerate(layout_rows):
                    if len(row) != row_length:
                        raise ValueError(f"Row {index} width does not match the layout's first row.")
                grid_width = row_length
                grid_height = len(layout_rows)
            else:
                layout_rows = None

        parsed_layout = self._parse_layout(layout_rows, grid_width, grid_height)
        resolved_start = start_position or parsed_layout.get("start") or (0, grid_height - 1)
        resolved_goal = goal_position or parsed_layout.get("goal") or (grid_width - 1, 0)
        layout_obstacles = parsed_layout.get("obstacles")
        if obstacles is not None:
            resolved_obstacles = set(obstacles)
        elif layout_obstacles is not None:
            resolved_obstacles = set(layout_obstacles)
        else:
            resolved_obstacles = set()
        if not resolved_obstacles and obstacles is None and layout_obstacles is None:
            resolved_obstacles = self._default_obstacle_field(grid_width, grid_height)

        super().__init__(
            grid_width,
            grid_height,
            max_turns=max_turns,
            battery_capacity=60,
            idle_cost=0,
            move_cost=1,
            action_cost=2,
            recharge_rate=6,
            seed_spawn_rate=0,
            water_source_capacity=0,
            base_position=resolved_start,
        )

        self.start_position = resolved_start
        self.goal_position = resolved_goal
        self.goal_reached: bool = False
        self.goal_turn: Optional[int] = None
        self.goal_agent_id: Optional[int] = None

        self._obstacles: Dict[Tuple[int, int], bool] = {}
        self._prepare_field(resolved_obstacles)

    @staticmethod
    def _parse_layout(
        layout: Optional[Iterable[str]], expected_width: int, expected_height: int
    ) -> Dict[str, object]:
        """Parse an ASCII layout description, returning obstacles, start, and goal."""
        if layout is None:
            return {}
        rows = list(layout)
        if len(rows) != expected_height:
            raise ValueError("Layout height does not match the configured grid height.")

        obstacles: set[Tuple[int, int]] = set()
        start: Optional[Tuple[int, int]] = None
        goal: Optional[Tuple[int, int]] = None

        for y, row in enumerate(rows):
            if len(row) != expected_width:
                raise ValueError(f"Row {y} width does not match the configured grid width.")
            for x, char in enumerate(row):
                if char == "#":
                    obstacles.add((x, y))
                elif char == "S":
                    start = (x, y)
                elif char == "G":
                    goal = (x, y)
                elif char not in {".", " "}:
                    raise ValueError(f"Unsupported character {char!r} at {(x, y)}.")
        return {"obstacles": obstacles, "start": start, "goal": goal}

    @staticmethod
    def _default_obstacle_field(width: int, height: int) -> set[Tuple[int, int]]:
        """Generate a deterministic obstacle pattern with deliberate gaps."""
        obstacles: set[Tuple[int, int]] = set()
        if width < 4 or height < 4:
            return obstacles

        mid_x = width // 2
        for y in range(1, height - 1):
            if y % 2 == 0:
                continue
            obstacles.add((mid_x, y))

        for x in range(1, width - 1, 3):
            obstacles.add((x, height // 2))

        gap = (mid_x, height - 2)
        obstacles.discard(gap)
        return obstacles

    def _prepare_field(self, obstacles: Iterable[Tuple[int, int]]) -> None:
        """Clear farming resources and place obstacles and the goal marker."""
        for pos in self.water_sources + self.seed_supply:
            tile = self.get_tile(pos)
            tile.items.clear()

        self.water_sources = []
        self.seed_supply = []
        self.turns_since_last_seed_spawn = 0

        self._obstacles.clear()
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile((x, y))
                tile.blocking = False
                tile.terrain = "plain"
                self._farmable[y][x] = True

        base_tile = self.get_tile(self.start_position)
        base_tile.terrain = "launch_pad"
        self._farmable[self.start_position[1]][self.start_position[0]] = False

        for position in obstacles:
            if not self.in_bounds(position):
                continue
            if position == self.start_position or position == self.goal_position:
                continue
            tile = self.get_tile(position)
            tile.blocking = True
            tile.terrain = "tree"
            self._farmable[position[1]][position[0]] = False
            self._soil[position[1]][position[0]].reset()
            self._obstacles[position] = True

        goal_tile = self.get_tile(self.goal_position)
        goal_tile.terrain = "goal"
        goal_tile.blocking = False
        self._farmable[self.goal_position[1]][self.goal_position[0]] = True

    def after_step(self) -> None:  # type: ignore[override]
        """Override to monitor goal completion while retaining base updates."""
        super().after_step()
        if self.goal_reached:
            return
        for agent_id, state in self.agent_states.items():
            if state.position == self.goal_position:
                self.goal_reached = True
                self.goal_turn = self.turn + 1
                self.goal_agent_id = agent_id
                break

    def tile_metadata(self, position: Tuple[int, int]) -> Dict[str, object]:  # type: ignore[override]
        """Expose obstacle and goal markers in addition to base metadata."""
        metadata = super().tile_metadata(position)
        metadata.update(
            {
                "obstacle": position in self._obstacles,
                "goal": position == self.goal_position,
                "start": position == self.start_position,
            }
        )
        return metadata

    def summary(self) -> Dict[str, object]:  # type: ignore[override]
        """Extend the base summary with navigation-specific progress."""
        data = super().summary()
        data.update(
            {
                "goal_reached": self.goal_reached,
                "goal_turn": self.goal_turn,
                "goal_agent_id": self.goal_agent_id,
            }
        )
        return data

    def obstacles(self) -> List[Tuple[int, int]]:
        """Return a copy of the obstacle list for external use."""
        return list(self._obstacles.keys())
