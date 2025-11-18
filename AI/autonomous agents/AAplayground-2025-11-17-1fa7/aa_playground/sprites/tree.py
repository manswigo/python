"""
sprites/tree.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Tree obstacle sprite creation and wind animation logic.
"""

from __future__ import annotations

import math
import random
from typing import Dict, Tuple

import pygame


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


class TreeSprites:
    """Generate and render obstacle trees with gentle wind sway."""

    def __init__(self, tile_size: int) -> None:
        self.tile_size = tile_size
        self._states: Dict[Tuple[int, int], Dict[str, float]] = {}
        self._build_surfaces()

    def _build_surfaces(self) -> None:
        tile_size = self.tile_size

        trunk_width = max(6, tile_size // 6)
        trunk_height = max(16, tile_size // 2)
        self._trunk_surface = pygame.Surface((trunk_width, trunk_height), pygame.SRCALPHA)
        pygame.draw.rect(
            self._trunk_surface,
            (92, 62, 32),
            pygame.Rect(0, 0, trunk_width, trunk_height),
            border_radius=trunk_width // 2,
        )
        pygame.draw.rect(
            self._trunk_surface,
            (135, 96, 56),
            pygame.Rect(trunk_width // 4, trunk_height // 6, trunk_width // 2, trunk_height // 2),
            border_radius=trunk_width // 3,
        )

        canopy_radius = max(14, tile_size // 2 - tile_size // 6)
        canopy_size = canopy_radius * 2
        self._canopy_surface = pygame.Surface((canopy_size, canopy_size), pygame.SRCALPHA)
        center = canopy_radius
        pygame.draw.circle(
            self._canopy_surface,
            (44, 120, 68),
            (center, center),
            canopy_radius,
        )
        pygame.draw.circle(
            self._canopy_surface,
            (70, 160, 92),
            (center - canopy_radius // 4, center - canopy_radius // 3),
            canopy_radius // 2,
        )
        pygame.draw.circle(
            self._canopy_surface,
            (25, 80, 48, 130),
            (center + canopy_radius // 3, center + canopy_radius // 5),
            canopy_radius // 2,
        )
        lobe_radius = max(6, canopy_radius // 2)
        lobe_offset = canopy_radius // 2
        pygame.draw.circle(
            self._canopy_surface,
            (34, 110, 60),
            (center - lobe_offset, center + lobe_radius),
            lobe_radius,
        )
        pygame.draw.circle(
            self._canopy_surface,
            (34, 110, 60),
            (center + lobe_offset, center + lobe_radius // 2),
            int(lobe_radius * 0.85),
        )

        self._trunk_half_width = self._trunk_surface.get_width() // 2
        self._canopy_half_width = self._canopy_surface.get_width() // 2
        self._canopy_height = self._canopy_surface.get_height()

    def _state_for(self, position: Tuple[int, int]) -> Dict[str, float]:
        state = self._states.get(position)
        if state is None:
            rng = random.Random(hash(position))
            amplitude = rng.uniform(self.tile_size * 0.04, self.tile_size * 0.08)
            state = {
                "phase": rng.uniform(0, math.tau),
                "speed": rng.uniform(0.6, 1.1),
                "amplitude": amplitude,
                "gust_phase": rng.uniform(0, math.tau),
                "gust_speed": rng.uniform(0.1, 0.25),
                "vertical_phase": rng.uniform(0, math.tau),
                "vertical_amp": rng.uniform(1.0, self.tile_size * 0.05),
            }
            self._states[position] = state
        return state

    def draw(
        self,
        surface: pygame.Surface,
        tile_rect: pygame.Rect,
        position: Tuple[int, int],
        animation_time: float,
    ) -> None:
        """Render the tree inside the specified tile rectangle."""
        state = self._state_for(position)
        sway_base = math.sin(animation_time * state["speed"] + state["phase"]) * state["amplitude"]
        gust = math.sin(animation_time * state["gust_speed"] + state["gust_phase"]) * (state["amplitude"] * 0.4)
        sway = sway_base + gust
        vertical_offset = math.sin(
            animation_time * (state["speed"] * 0.9) + state["vertical_phase"]
        ) * state["vertical_amp"]

        trunk_center_x = _clamp(
            tile_rect.centerx + sway * 0.25,
            tile_rect.left + self._trunk_half_width,
            tile_rect.right - self._trunk_half_width,
        )
        trunk_bottom_y = tile_rect.bottom - 2
        trunk_rect = self._trunk_surface.get_rect(midbottom=(int(trunk_center_x), int(trunk_bottom_y)))
        surface.blit(self._trunk_surface, trunk_rect)

        min_canopy_center_x = tile_rect.left + self._canopy_half_width
        max_canopy_center_x = tile_rect.right - self._canopy_half_width
        canopy_center_x = _clamp(tile_rect.centerx + sway, min_canopy_center_x, max_canopy_center_x)

        min_canopy_bottom = tile_rect.top + self._canopy_height
        max_canopy_bottom = tile_rect.bottom - 4
        canopy_bottom = _clamp(
            trunk_rect.top - vertical_offset + 6,
            min_canopy_bottom,
            max_canopy_bottom,
        )
        canopy_rect = self._canopy_surface.get_rect(
            midbottom=(int(canopy_center_x), int(canopy_bottom))
        )
        surface.blit(self._canopy_surface, canopy_rect)
