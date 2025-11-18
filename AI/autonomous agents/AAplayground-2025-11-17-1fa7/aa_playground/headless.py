"""
headless.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Headless (ASCII-based) game runner for autonomous agents.
"""

from __future__ import annotations

import math
import time
from typing import Optional

from .agents import BaseAgent
from .environment import DronePlantingField


def render_ascii(
    environment: DronePlantingField, agent_id: Optional[int] = None
) -> str:
    """
    Render an ASCII snapshot of the planting field.
    
    Args:
        environment: The drone planting field to render.
        agent_id: Optional agent ID to show the drone position.
    
    Returns:
        ASCII string representation of the field.
    
    Legend:
        D = Drone
        B = Base/Launch pad
        T = Tree/Obstacle
        # = Non-farmable
        . = Empty farmable soil
        s = Planted seed
        g = Growing crop
        F = Fully grown crop (ready)
        w = Weed
    """
    agent_position: Optional[tuple[int, int]] = None
    if agent_id is not None and agent_id in environment.agent_states:
        agent_position = environment.agent_states[agent_id].position

    rows: list[str] = []
    for y in range(environment.height):
        cells: list[str] = []
        for x in range(environment.width):
            position = (x, y)
            if agent_position == position:
                cells.append("D")
                continue
            metadata = environment.tile_metadata(position)
            soil_info: dict | None = metadata.get("soil")
            if metadata.get("launch_pad"):
                cells.append("B")
            elif metadata.get("obstacle"):
                cells.append("T")
            elif not metadata.get("farmable", True):
                cells.append("#")
            elif soil_info:
                stage = soil_info.get("stage")
                if stage == "seed":
                    cells.append("s")
                elif stage == "growing":
                    cells.append("g")
                elif stage == "ready":
                    cells.append("F")
                elif stage == "weed":
                    cells.append("w")
                else:
                    cells.append(".")
            else:
                cells.append(".")
        rows.append("".join(cells))
    return "\n".join(rows)


def run_headless(
    environment: DronePlantingField,
    controller: BaseAgent,
    agent_id: int,
    delay: float = 0.0,
) -> None:
    """
    Run the planting challenge in headless mode (ASCII output).
    
    Args:
        environment: The drone planting field environment.
        controller: The agent controller.
        agent_id: The ID of the agent in the environment.
        delay: Additional pause between turns (in seconds).
    """
    print("Initial field:")
    print(render_ascii(environment, agent_id))
    print()

    while True:
        if environment.max_turns is not None and environment.turn >= environment.max_turns:
            print("Reached max turns.")
            break

        environment.step()
        state = environment.agent_states[agent_id]
        grown = len(environment.grown_plots)
        
        # Format seeds count (handle infinity)
        seeds_value = state.inventory.get("seed", 0)
        seeds_text = (
            "∞" if isinstance(seeds_value, (int, float)) and math.isinf(seeds_value) 
            else str(seeds_value)
        )
        
        # Format battery level (handle infinity)
        battery_value = environment.battery_level(agent_id)
        battery_text = (
            "∞"
            if isinstance(battery_value, (int, float)) and math.isinf(battery_value)
            else str(battery_value)
        )
        
        print(
            f"Turn {environment.turn}: position={state.position}, seeds={seeds_text}, "
            f"battery={battery_text}, grown_plots={grown}"
        )
        print(render_ascii(environment, agent_id))
        print()

        if environment.max_turns is not None and environment.turn >= environment.max_turns:
            break
        if delay > 0:
            time.sleep(delay)

    print("Final stats:", environment.summary())
