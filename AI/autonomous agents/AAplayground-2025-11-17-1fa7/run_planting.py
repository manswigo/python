"""
run_drone_planting.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Planting challenge launcher focused on maximising grown crop tiles.
"""

from __future__ import annotations

import argparse
import importlib
from typing import Optional, Type

from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from aa_playground import (
    BaseAgent,
    DroneGameConfig,
    DroneGameSession,
    DronePlantingField,
    KeyboardDroneAgent,
    run_headless,
)
from aa_playground.core import Action


class AutoPlantingField(DronePlantingField):
    """
    Modified planting field that automatically plants seeds at the drone's position
    after every action. This removes the need for explicit planting actions.
    """

    def execute_action(self, agent_id: int, action: Action | None) -> None:
        """Execute the action and automatically plant if on farmable soil."""
        # First execute the original action (movement or wait)
        super().execute_action(agent_id, action)
        
        # Then automatically plant at the current position
        state = self.agent_states.get(agent_id)
        if state is None:
            return
            
        position = state.position
        if not self.is_farmable(position):
            return
            
        # Get the soil at the current position
        soil = self._soil[position[1]][position[0]]
        
        # Automatically plant if the soil is empty and agent has seeds
        if soil.stage.value == "empty" and "seed" in state.inventory:
            self._handle_plant(state, soil)


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser for the planting challenge launcher."""
    parser = argparse.ArgumentParser(
        description="Drone planting challenge – grow as many plots as possible."
    )
    parser.add_argument("--width", type=int, default=15, help="Grid width.")
    parser.add_argument("--height", type=int, default=10, help="Grid height.")
    parser.add_argument("--turns", type=int, default=120, help="Maximum number of turns.")
    parser.add_argument(
        "--seed-turns",
        type=int,
        default=2,
        help="Turns required for a planted seed to transform into a growing crop.",
    )
    parser.add_argument(
        "--growing-turns",
        type=int,
        default=3,
        help="Turns required for a growing crop to become fully grown.",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=4,
        help="Seed units placed in the agent inventory at the start (inventory is replenished to ∞).",
    )
    parser.add_argument(
        "--controller",
        default="manual",
        help="Either 'manual' for keyboard-driven play or a dotted path to a custom agent class (e.g. package.module:AgentClass).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.3,
        help="Seconds between automatic turns for autonomous agents.",
    )
    parser.add_argument("--tile-size", type=int, default=64, help="Tile size in pixels.")
    parser.add_argument("--hud", type=int, default=120, help="HUD height in pixels.")
    parser.add_argument("--fps", type=int, default=60, help="Frame rate cap for pygame.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the agent without opening the pygame window (prints ASCII frames).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Additional pause between turns when running headless.",
    )
    return parser


def instantiate_agent(agent_path: Optional[str], fallback: BaseAgent) -> BaseAgent:
    """Instantiate a custom agent class or return the provided fallback."""
    if not agent_path:
        return fallback
    module_name, _, class_name = agent_path.partition(":")
    if not module_name or not class_name:
        raise ValueError("Invalid agent path. Use the format 'module.submodule:ClassName'.")
    module = importlib.import_module(module_name)
    agent_cls: Type[BaseAgent] = getattr(module, class_name)
    return agent_cls()


def run_manual_game(args: argparse.Namespace) -> None:
    """Launch the pygame session for interactive planting."""
    environment = AutoPlantingField(
        width=args.width,
        height=args.height,
        max_turns=args.turns,
        seed_turns=args.seed_turns,
        growing_turns=args.growing_turns,
    )
    controller = KeyboardDroneAgent()
    environment.register_agent(
        controller, position=environment.base_position, inventory={"seed": args.seeds}
    )

    config = DroneGameConfig(
        tile_size=args.tile_size,
        hud_height=args.hud,
        fps=args.fps,
        turn_interval=args.interval,
    )
    session = DroneGameSession(environment, controller, config)
    session.run()
    print("Simulation finished.")
    print("Final stats:", environment.summary())


def run_agent_game(args: argparse.Namespace) -> None:
    """Execute the planting challenge with an autonomous agent."""
    if not args.agent_path:
        raise ValueError("Agent control requires --controller to specify a controller class.")

    environment = AutoPlantingField(
        width=args.width,
        height=args.height,
        max_turns=args.turns,
        seed_turns=args.seed_turns,
        growing_turns=args.growing_turns,
    )
    controller = instantiate_agent(args.agent_path, KeyboardDroneAgent())
    agent_id = environment.register_agent(
        controller, position=environment.base_position, inventory={"seed": args.seeds}
    )

    if not args.headless:
        config = DroneGameConfig(
            tile_size=args.tile_size,
            hud_height=args.hud,
            fps=args.fps,
            turn_interval=args.interval,
        )
        session = DroneGameSession(environment, controller, config)
        session.run()
        print("Final stats:", environment.summary())
        return

    run_headless(environment, controller, agent_id, delay=args.delay)


def main() -> None:
    """Select the control scheme and start the planting challenge."""
    parser = build_parser()
    args = parser.parse_args()

    # If controller is "manual", run manual mode
    if args.controller == "manual":
        run_manual_game(args)
    else: # Otherwise, treat controller as an agent path and run agent mode
        args.agent_path = args.controller
        run_agent_game(args)


if __name__ == "__main__":
    main()
