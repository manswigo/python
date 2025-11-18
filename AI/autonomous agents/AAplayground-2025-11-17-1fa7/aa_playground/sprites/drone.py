"""
sprites/drone.py

Author: Marco Della Vedova <marco.dellavedova@chalmers.se>
Description: Drone sprite creation and rendering helpers.
"""

from __future__ import annotations

import math
from typing import Tuple

import pygame

from ..environment import AgentState


class DroneSprites:
    """Build and render the animated drone sprites."""

    def __init__(self, tile_size: int) -> None:
        self.tile_size = tile_size
        self._build_surfaces()

    def _build_surfaces(self) -> None:
        tile_size = self.tile_size
        base_size = tile_size
        center = base_size // 2

        offset = int(tile_size * 0.32)
        self._rotor_offsets: Tuple[Tuple[int, int], ...] = (
            (-offset, -offset),
            (offset, -offset),
            (-offset, offset),
            (offset, offset),
        )

        self._drone_body = pygame.Surface((base_size, base_size), pygame.SRCALPHA)
        arm_width = max(2, int(tile_size * 0.06))
        arm_color = (140, 160, 185)
        for ox, oy in self._rotor_offsets:
            end_point = (center + ox, center + oy)
            pygame.draw.line(self._drone_body, arm_color, (center, center), end_point, arm_width)

        fuselage_radius = int(tile_size * 0.22)
        pygame.draw.circle(self._drone_body, (200, 210, 230), (center, center), fuselage_radius)
        pygame.draw.circle(self._drone_body, (85, 95, 120), (center, center), int(fuselage_radius * 0.72))
        pygame.draw.circle(self._drone_body, (45, 205, 255), (center, center), int(fuselage_radius * 0.32))
        highlight = pygame.Surface((base_size, base_size), pygame.SRCALPHA)
        pygame.draw.circle(
            highlight,
            (255, 255, 255, 120),
            (center - int(tile_size * 0.08), center - int(tile_size * 0.12)),
            max(2, int(tile_size * 0.08)),
        )
        self._drone_body.blit(highlight, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        pod_radius = max(4, int(tile_size * 0.12))
        pod_size = pod_radius * 2 + 2
        self._rotor_pod = pygame.Surface((pod_size, pod_size), pygame.SRCALPHA)
        pod_center = pod_radius + 1
        pygame.draw.circle(self._rotor_pod, (65, 75, 90), (pod_center, pod_center), pod_radius)
        pygame.draw.circle(self._rotor_pod, (115, 130, 150), (pod_center, pod_center), int(pod_radius * 0.7))
        pygame.draw.circle(
            self._rotor_pod,
            (210, 220, 235, 160),
            (pod_center - int(pod_radius * 0.2), pod_center - int(pod_radius * 0.3)),
            max(1, int(pod_radius * 0.35)),
        )

        blade_radius = max(8, int(tile_size * 0.18))
        blade_size = blade_radius * 2
        self._rotor_blade = pygame.Surface((blade_size, blade_size), pygame.SRCALPHA)
        blade_center = blade_radius
        blade_length = int(blade_radius * 1.8)
        blade_width = max(2, int(tile_size * 0.05))
        blade_color = (225, 235, 245)
        pygame.draw.rect(
            self._rotor_blade,
            blade_color,
            pygame.Rect(blade_center - blade_length // 2, blade_center - blade_width // 2, blade_length, blade_width),
            border_radius=blade_width,
        )
        pygame.draw.rect(
            self._rotor_blade,
            blade_color,
            pygame.Rect(blade_center - blade_width // 2, blade_center - blade_length // 2, blade_width, blade_length),
            border_radius=blade_width,
        )
        pygame.draw.circle(self._rotor_blade, (255, 255, 255), (blade_center, blade_center), max(2, blade_width // 2))

        self._drone_shadow_base = pygame.Surface((base_size, base_size), pygame.SRCALPHA)
        shadow_rect = pygame.Rect(0, 0, int(tile_size * 0.64), int(tile_size * 0.26))
        shadow_rect.center = (center, center + int(tile_size * 0.18))
        pygame.draw.ellipse(self._drone_shadow_base, (0, 0, 0, 160), shadow_rect)

        glow_size = max(8, int(tile_size * 1.6))
        self._drone_glow_base = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_center = glow_size // 2
        pygame.draw.circle(
            self._drone_glow_base,
            (70, 160, 255, 60),
            (glow_center, glow_center),
            max(4, int(tile_size * 0.55)),
        )
        pygame.draw.circle(
            self._drone_glow_base,
            (120, 200, 255, 35),
            (glow_center, glow_center),
            max(4, int(tile_size * 0.4)),
        )

    def draw(
        self,
        *,
        surface: pygame.Surface,
        state: AgentState,
        animation_time: float,
        rotor_angle: float,
        bob_speed: float,
        bob_amplitude: float,
    ) -> None:
        """Render the drone for the given agent state."""
        tile_size = self.tile_size
        grid_x, grid_y = state.position
        base_x = grid_x * tile_size + tile_size // 2
        base_y = grid_y * tile_size + tile_size // 2

        phase = (state.agent_id or 0) * 0.6
        bob_angle = animation_time * bob_speed + phase
        bob_offset = math.sin(bob_angle) * bob_amplitude
        center_y = base_y - bob_offset
        height_factor = (math.sin(bob_angle) + 1.0) * 0.5

        shadow_alpha = int(140 - 80 * height_factor)
        shadow_surface = self._drone_shadow_base.copy()
        shadow_surface.set_alpha(max(40, min(160, shadow_alpha)))
        shadow_center = (
            base_x,
            grid_y * tile_size + tile_size // 2 + int(tile_size * 0.2),
        )
        surface.blit(shadow_surface, shadow_surface.get_rect(center=shadow_center))

        glow_surface = self._drone_glow_base.copy()
        glow_surface.set_alpha(int(55 + 40 * height_factor))
        glow_rect = glow_surface.get_rect(center=(base_x, int(center_y)))
        surface.blit(glow_surface, glow_rect)

        body_rect = self._drone_body.get_rect(center=(base_x, int(center_y)))
        surface.blit(self._drone_body, body_rect)

        rotor_base_angle = (rotor_angle + (state.agent_id or 0) * 12.0) % 360.0
        for index, (ox, oy) in enumerate(self._rotor_offsets):
            rotor_center = (base_x + ox, center_y + oy)
            pod_rect = self._rotor_pod.get_rect(center=(int(rotor_center[0]), int(rotor_center[1])))
            surface.blit(self._rotor_pod, pod_rect)

            blade_surface = pygame.transform.rotozoom(
                self._rotor_blade, rotor_base_angle + index * 45.0, 1.0
            )
            blade_rect = blade_surface.get_rect(center=(int(rotor_center[0]), int(rotor_center[1])))
            surface.blit(blade_surface, blade_rect)
