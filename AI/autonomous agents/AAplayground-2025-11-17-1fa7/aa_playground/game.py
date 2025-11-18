"""
game.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Pygame front-end for the drone farming playground.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import pygame

from .agents import BaseAgent, KeyboardDroneAgent
from .core import Action, ActionType, Direction
from .environment import AgentState, CropStage, DroneField
from .sprites import CropSprites, DroneSprites, TreeSprites


@dataclass(frozen=True)
class DroneGameConfig:
    """Configuration values that control the look-and-feel of the pygame session."""

    tile_size: int = 64
    hud_height: int = 120
    fps: int = 60
    turn_interval: float = 0.4


class DroneGameSession:
    """Orchestrates the pygame window, input handling, and simulation updates."""

    def __init__(self, environment: DroneField, agent: BaseAgent, config: DroneGameConfig) -> None:
        """
        Prepare the window, fonts, and pre-computed sprites used throughout the session.
        """
        pygame.init()
        pygame.font.init()

        self.environment = environment
        self.agent = agent
        self.config = config

        width = environment.width * config.tile_size
        height = environment.height * config.tile_size + config.hud_height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Drone Field - Turn Based Playground")

        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_large = pygame.font.SysFont("arial", 24, bold=True)

        self._time_since_last_step = 0.0
        self._running = True
        self._pending_step = False

        self._animation_time = 0.0
        self._rotor_angle = 0.0
        self._rotor_speed = 720.0
        self._bob_speed = 2.6
        self._bob_amplitude = max(3.0, self.config.tile_size * 0.06)
        self._drone_sprites = DroneSprites(self.config.tile_size)
        self._tree_sprites = TreeSprites(self.config.tile_size)
        self._crop_sprites = CropSprites(self.config.tile_size)

    @staticmethod
    def _format_quantity(value: object) -> str:
        """Pretty-print numeric values, mapping infinities to the ∞ symbol."""
        if isinstance(value, (int, float)):
            if math.isinf(value):
                return "∞"
            if value == int(value):
                return str(int(value))
        if value is None:
            return "?"
        return str(value)

    def _handle_events(self) -> None:
        """Process pygame events, converting key presses into queued actions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif isinstance(self.agent, KeyboardDroneAgent):
                    action = self._map_key_to_action(event.key)
                    if action:
                        self.agent.queue_action(action)
                        self._pending_step = True

    def _map_key_to_action(self, key: int) -> Optional[Action]:
        """Map key presses to agent actions for the keyboard-controlled player."""
        if key == pygame.K_UP:
            return Action(ActionType.MOVE, direction=Direction.UP)
        if key == pygame.K_DOWN:
            return Action(ActionType.MOVE, direction=Direction.DOWN)
        if key == pygame.K_LEFT:
            return Action(ActionType.MOVE, direction=Direction.LEFT)
        if key == pygame.K_RIGHT:
            return Action(ActionType.MOVE, direction=Direction.RIGHT)
        if key == pygame.K_p:
            return Action(ActionType.PLANT)
        if key == pygame.K_w:
            return Action(ActionType.WATER)
        if key == pygame.K_h or key == pygame.K_SPACE:
            return Action(ActionType.HARVEST)
        if key == pygame.K_g:
            return Action(ActionType.PICK_UP)
        if key == pygame.K_PERIOD or key == pygame.K_s:
            return Action(ActionType.WAIT)
        return None

    def _update_animation(self, delta_seconds: float) -> None:
        """Advance the animation timeline for rotor rotation and bobbing."""
        self._animation_time += delta_seconds
        self._rotor_angle = (self._rotor_angle + self._rotor_speed * delta_seconds) % 360.0

    def _step_environment(self, delta_seconds: float) -> None:
        """Advance the simulation either on demand or at a fixed interval."""
        if self.agent.requires_interaction:
            has_pending = self.agent.has_pending_actions()
            if self.environment.max_turns is not None and self.environment.turn >= self.environment.max_turns:
                self._running = False
                return
            if not self._pending_step and not has_pending:
                return
            self.environment.step()
            self._pending_step = self.agent.has_pending_actions()
            return

        self._time_since_last_step += delta_seconds
        if self._time_since_last_step < self.config.turn_interval:
            return
        self._time_since_last_step = 0.0

        if self.environment.max_turns is not None and self.environment.turn >= self.environment.max_turns:
            self._running = False
            return

        self.environment.step()

    def _draw_grid(self) -> None:
        """Render the world grid, including soil states, launch pad, and obstacles."""
        tile_size = self.config.tile_size
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                position = (x, y)
                tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                metadata = self.environment.tile_metadata(position)
                soil = metadata.get("soil")
                launch_pad = metadata.get("launch_pad", False)
                farmable = metadata.get("farmable", False)
                obstacle = metadata.get("obstacle", False)
                goal_tile = metadata.get("goal", False)

                color = (60, 60, 60)
                if obstacle:
                    color = (76, 52, 30)
                elif goal_tile:
                    color = (80, 110, 170)
                elif launch_pad:
                    color = (60, 90, 140)
                elif not farmable:
                    color = (44, 82, 52)
                elif soil:
                    stage = soil.get("stage")
                    if stage == "empty":
                        color = (120, 85, 60)
                    elif stage == "seed":
                        color = (110, 150, 80)
                    elif stage == "growing":
                        color = (70, 160, 75)
                    elif stage == "ready":
                        color = (200, 170, 40)
                    elif stage == "weed":
                        color = (85, 130, 55)
                    else:
                        color = (90, 90, 90)
                pygame.draw.rect(self.surface, color, tile_rect)
                pygame.draw.rect(self.surface, (30, 30, 30), tile_rect, width=1)

                tile = self.environment.get_tile(position)
                offset = 6
                if tile.items.get("seed"):
                    seed_rect = pygame.Rect(
                        tile_rect.left + offset, tile_rect.top + offset, 12, 12
                    )
                    pygame.draw.rect(self.surface, (230, 230, 230), seed_rect)
                if tile.items.get("water"):
                    water_rect = pygame.Rect(
                        tile_rect.right - offset - 12, tile_rect.top + offset, 12, 12
                    )
                    pygame.draw.rect(self.surface, (60, 140, 200), water_rect)

                if soil:
                    stage_name = soil.get("stage")
                    try:
                        crop_stage = CropStage(stage_name) if stage_name else None
                    except ValueError:
                        crop_stage = None
                    if crop_stage in {CropStage.PLANTED, CropStage.GROWING, CropStage.READY, CropStage.WEED}:
                        self._crop_sprites.draw(self.surface, tile_rect, crop_stage, self._animation_time)

                if obstacle:
                    self._tree_sprites.draw(self.surface, tile_rect, position, self._animation_time)

        for state in self.environment.agent_states.values():
            self._draw_drone(state)

    def _draw_drone(self, state: AgentState) -> None:
        """Draw a single drone with bobbing, glow, shadow, and rotating rotors."""
        self._drone_sprites.draw(
            surface=self.surface,
            state=state,
            animation_time=self._animation_time,
            rotor_angle=self._rotor_angle,
            bob_speed=self._bob_speed,
            bob_amplitude=self._bob_amplitude,
        )

    def _draw_hud(self) -> None:
        """Render HUD text with controls, turns, and agent summaries."""
        tile_size = self.config.tile_size
        hud_top = self.environment.height * tile_size
        hud_rect = pygame.Rect(0, hud_top, self.surface.get_width(), self.config.hud_height)
        pygame.draw.rect(self.surface, (18, 18, 22), hud_rect)

        control_hint = (
            "Controls: arrows move (seeds auto-plant) | . wait | Esc quit"
            if isinstance(self.agent, KeyboardDroneAgent)
            else "Autonomous agent running – press Esc to exit."
        )
        lines = [
            control_hint,
            f"Turn {self.environment.turn}/{self.environment.max_turns or '∞'}",
        ]

        goal_position = getattr(self.environment, "goal_position", None)
        goal_reached = getattr(self.environment, "goal_reached", False)
        if goal_position is not None:
            status = "reached" if goal_reached else "not reached"
            lines.append(f"Navigation goal at {goal_position} ({status})")

        line_y = hud_top + 10
        for line in lines:
            text_surface = self.font_small.render(line, True, (220, 220, 220))
            self.surface.blit(text_surface, (14, line_y))
            line_y += 24

        stats_y = line_y + 6
        for agent_id, state in self.environment.agent_states.items():
            battery = self.environment.battery_level(agent_id)
            capacity = getattr(self.environment, "battery_capacity", None)
            battery_text = self._format_quantity(battery)
            capacity_text = self._format_quantity(capacity)
            inventory_text = (
                ", ".join(
                    f"{item}:{self._format_quantity(amount)}" for item, amount in state.inventory.items()
                )
                or "empty"
            )
            text = (
                f"{state.name} (id {agent_id}) – battery {battery_text}/{capacity_text} "
                f"– inventory [{inventory_text}]"
            )
            text_surface = self.font_large.render(text, True, (230, 230, 100))
            self.surface.blit(text_surface, (14, stats_y))
            stats_y += 32

    def _draw(self) -> None:
        """Render the full frame including grid and HUD."""
        self.surface.fill((12, 12, 20))
        self._draw_grid()
        self._draw_hud()

    def run(self) -> None:
        """Execute the main event loop until the window is closed."""
        while self._running:
            delta_ms = self.clock.tick(self.config.fps)
            delta_seconds = delta_ms / 1000.0

            self._handle_events()
            self._update_animation(delta_seconds)
            self._step_environment(delta_seconds)
            self._draw()
            pygame.display.flip()

        pygame.quit()


def run_game(
    *,
    agent: Optional[BaseAgent] = None,
    width: int = 8,
    height: int = 6,
    turns: int = 120,
    turn_interval: float = 0.4,
    tile_size: int = 64,
    hud_height: int = 120,
    fps: int = 60,
    starting_inventory: Optional[dict[str, int]] = None,
) -> tuple[DroneField, BaseAgent]:
    """
    Helper that creates the environment, registers the agent, and starts the session.

    Returns
    -------
    Tuple[DroneField, BaseAgent]
        The environment and controller used during the session. Inspection of the
        environment after the call allows collecting statistics such as harvested crops.
    """
    environment = DroneField(width, height, max_turns=turns)
    controller = agent or KeyboardDroneAgent()
    environment.register_agent(
        controller,
        position=(0, height - 1),
        inventory=starting_inventory or {"seed": 2, "water": 1},
    )

    config = DroneGameConfig(
        tile_size=tile_size,
        hud_height=hud_height,
        fps=fps,
        turn_interval=turn_interval,
    )

    session = DroneGameSession(environment, controller, config)
    session.run()
    return environment, controller
