"""
sprites/crop.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Procedural crop sprite surfaces and animation helpers for soil growth stages.
"""

from __future__ import annotations

import math
from typing import Dict

import pygame

from ..environment import CropStage


class CropSprites:
    """Build and animate crop visuals for planted, growing, and ready stages."""

    def __init__(self, tile_size: int) -> None:
        self.tile_size = tile_size
        self._cache: Dict[CropStage, pygame.Surface] = {}
        self._stem_color = (60, 140, 70)
        self._leaf_color = (95, 180, 105)
        self._fruit_color = (230, 210, 70)
        self._build_base_surfaces()

    def _build_base_surfaces(self) -> None:
        """Create static base surfaces for each crop stage."""
        base = self.tile_size
        planted = pygame.Surface((base, base), pygame.SRCALPHA)
        growing = pygame.Surface((base, base), pygame.SRCALPHA)
        ready = pygame.Surface((base, base), pygame.SRCALPHA)
        weed = pygame.Surface((base, base), pygame.SRCALPHA)

        center_x = base // 2
        soil_line = int(base * 0.78)

        # Planted: small sprout with two leaves.
        pygame.draw.line(
            planted,
            self._stem_color,
            (center_x, soil_line),
            (center_x, soil_line - int(base * 0.12)),
            max(2, base // 32),
        )
        pygame.draw.circle(
            planted,
            self._leaf_color,
            (center_x - int(base * 0.05), soil_line - int(base * 0.12)),
            max(2, base // 18),
        )
        pygame.draw.circle(
            planted,
            self._leaf_color,
            (center_x + int(base * 0.05), soil_line - int(base * 0.12)),
            max(2, base // 18),
        )

        # Growing: taller stem with additional leaves.
        pygame.draw.line(
            growing,
            self._stem_color,
            (center_x, soil_line),
            (center_x, soil_line - int(base * 0.32)),
            max(3, base // 26),
        )
        pygame.draw.circle(
            growing,
            self._leaf_color,
            (center_x - int(base * 0.1), soil_line - int(base * 0.18)),
            max(2, base // 16),
        )
        pygame.draw.circle(
            growing,
            self._leaf_color,
            (center_x + int(base * 0.1), soil_line - int(base * 0.22)),
            max(2, base // 16),
        )
        pygame.draw.circle(
            growing,
            self._leaf_color,
            (center_x, soil_line - int(base * 0.3)),
            max(3, base // 14),
        )

        # Ready: canopy plus a fruit highlight.
        pygame.draw.line(
            ready,
            self._stem_color,
            (center_x, soil_line),
            (center_x, soil_line - int(base * 0.4)),
            max(4, base // 22),
        )
        pygame.draw.circle(
            ready,
            self._leaf_color,
            (center_x, soil_line - int(base * 0.42)),
            max(6, base // 10),
        )
        pygame.draw.circle(
            ready,
            self._leaf_color,
            (center_x - int(base * 0.16), soil_line - int(base * 0.28)),
            max(4, base // 12),
        )
        pygame.draw.circle(
            ready,
            self._leaf_color,
            (center_x + int(base * 0.16), soil_line - int(base * 0.3)),
            max(4, base // 12),
        )
        pygame.draw.circle(
            ready,
            self._fruit_color,
            (center_x, soil_line - int(base * 0.32)),
            max(4, base // 14),
        )

        # Weed patch: tangled darker leaves.
        weed_color = (70, 110, 55)
        for offset in range(-2, 3):
            pygame.draw.line(
                weed,
                weed_color,
                (center_x + offset * 2, soil_line),
                (center_x + int(offset * 1.5), soil_line - int(base * 0.22)),
                max(2, base // 30),
            )
        pygame.draw.circle(
            weed,
            (60, 90, 40),
            (center_x - int(base * 0.14), soil_line - int(base * 0.18)),
            max(3, base // 18),
        )
        pygame.draw.circle(
            weed,
            (60, 90, 40),
            (center_x + int(base * 0.16), soil_line - int(base * 0.2)),
            max(3, base // 18),
        )

        self._cache[CropStage.PLANTED] = planted
        self._cache[CropStage.GROWING] = growing
        self._cache[CropStage.READY] = ready
        self._cache[CropStage.WEED] = weed

    def draw(
        self,
        surface: pygame.Surface,
        tile_rect: pygame.Rect,
        stage: CropStage,
        animation_time: float,
    ) -> None:
        """Render the crop animation for the provided stage inside a tile."""
        if stage not in self._cache:
            return

        sprite = self._cache[stage]
        draw_rect = sprite.get_rect(midbottom=(tile_rect.centerx, tile_rect.bottom - 4))
        offset_x = 0.0
        scale = 1.0

        if stage is CropStage.PLANTED:
            sway = math.sin(animation_time * 2.4 + tile_rect.left * 0.1) * 2.0
            offset_x = sway
        elif stage is CropStage.GROWING:
            sway = math.sin(animation_time * 1.8 + tile_rect.top * 0.08) * 3.0
            pulsate = 1.0 + 0.06 * math.sin(animation_time * 2.2 + tile_rect.left * 0.05)
            offset_x = sway
            scale = pulsate
        elif stage is CropStage.READY:
            glow_alpha = int(70 + 40 * math.sin(animation_time * 1.6 + tile_rect.left * 0.12))
            glow_radius = max(10, int(self.tile_size * 0.32))
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surface,
                (255, 220, 120, max(40, min(120, glow_alpha))),
                (glow_radius, glow_radius),
                glow_radius,
            )
            glow_center = (tile_rect.centerx, tile_rect.bottom - int(self.tile_size * 0.28))
            surface.blit(glow_surface, glow_surface.get_rect(center=glow_center))
            sway = math.sin(animation_time * 1.4 + tile_rect.left * 0.06) * 1.5
            offset_x = sway
        elif stage is CropStage.WEED:
            sway = math.sin(animation_time * 2.8 + tile_rect.left * 0.18) * 2.5
            offset_x = sway
            rustle = 1.0 + 0.04 * math.sin(animation_time * 3.0 + tile_rect.top * 0.22)
            scale = rustle

        if scale != 1.0:
            scaled = pygame.transform.rotozoom(sprite, 0, scale)
            scaled_rect = scaled.get_rect(midbottom=(draw_rect.centerx + offset_x, draw_rect.bottom))
            surface.blit(scaled, scaled_rect)
        else:
            draw_rect.centerx += int(offset_x)
            surface.blit(sprite, draw_rect)
