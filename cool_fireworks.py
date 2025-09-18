"""ASCII firework simulation for the terminal.

Run this module as a script to watch colourful fireworks sparkle in your
terminal window.  The animation relies only on the Python standard library
and ANSI escape codes, so it should work on most Unix shells.
"""
from __future__ import annotations

import argparse
import math
import random
import shutil
import time
from dataclasses import dataclass
from typing import Iterable, List

# Pre-computed palette of bright ANSI 256 colour codes. The palette picks
# lighter, saturated colours that stand out nicely on dark backgrounds.
PALETTE: List[int] = [196, 202, 208, 214, 220, 226, 190, 118, 51, 45, 39, 33, 201, 207]


@dataclass
class Particle:
    """A single spark in the firework explosion."""

    x: float
    y: float
    vx: float
    vy: float
    life: float
    colour: int

    def step(self, gravity: float, damping: float) -> bool:
        """Advance the particle by one frame.

        Returns ``True`` if the particle is still alive afterwards, ``False``
        otherwise.  Dead particles are discarded from the simulation.
        """

        if self.life <= 0:
            return False

        self.x += self.vx
        self.y += self.vy
        self.vx *= damping
        self.vy = self.vy * damping + gravity
        self.life -= 1
        return self.life > 0 and self.y >= 0


class FireworkShow:
    """Manages particle explosions and renders frames to a canvas."""

    def __init__(
        self,
        width: int,
        height: int,
        gravity: float = 0.12,
        damping: float = 0.92,
        sparks: int = 120,
    ) -> None:
        self.width = width
        self.height = height
        self.gravity = gravity
        self.damping = damping
        self.sparks = sparks
        self.particles: List[Particle] = []
        self.frame_counter = 0

    def spawn_firework(self) -> None:
        """Create a fresh explosion near the top of the screen."""

        radius = random.uniform(6.0, 12.0)
        x = random.uniform(0.2 * self.width, 0.8 * self.width)
        y = random.uniform(0.2 * self.height, 0.45 * self.height)
        hue_shift = random.randrange(len(PALETTE))

        self.particles.extend(
            self._create_explosion(x=x, y=y, radius=radius, hue_shift=hue_shift)
        )

    def _create_explosion(
        self, x: float, y: float, radius: float, hue_shift: int
    ) -> Iterable[Particle]:
        """Generate a colourful sphere of spark particles."""

        for _ in range(self.sparks):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.6, 1.6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.randint(18, 40)
            colour = PALETTE[(hue_shift + random.randrange(len(PALETTE))) % len(PALETTE)]
            yield Particle(x, y, vx, vy, life, colour)

    def step(self) -> None:
        """Advance the simulation and occasionally spawn new fireworks."""

        if not self.particles or (self.frame_counter % random.randint(18, 26) == 0):
            self.spawn_firework()

        alive: List[Particle] = []
        for particle in self.particles:
            if particle.step(self.gravity, self.damping):
                if 0 <= particle.x < self.width and 0 <= particle.y < self.height:
                    alive.append(particle)
        self.particles = alive
        self.frame_counter += 1

    def render(self) -> str:
        """Return a string containing the current frame."""

        canvas = [
            [" " for _ in range(self.width)]
            for _ in range(self.height)
        ]
        colour_map = [
            [None for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for particle in self.particles:
            ix, iy = int(particle.x), int(particle.y)
            if 0 <= ix < self.width and 0 <= iy < self.height:
                char = random.choice(["*", "•", "·", "✶"])
                canvas[iy][ix] = char
                colour_map[iy][ix] = particle.colour

        return self._format_canvas(canvas, colour_map)

    def _format_canvas(self, canvas, colour_map) -> str:
        lines = []
        for row, colour_row in zip(canvas, colour_map):
            line_chars = []
            for char, colour in zip(row, colour_row):
                if colour is None or char == " ":
                    line_chars.append(char)
                else:
                    line_chars.append(f"\033[38;5;{colour}m{char}\033[0m")
            lines.append("".join(line_chars))
        return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render dazzling ASCII fireworks.")
    parser.add_argument(
        "--frames",
        type=int,
        default=200,
        help="Number of frames to render. Defaults to 200.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.06,
        help="Delay between frames in seconds. Defaults to 0.06.",
    )
    parser.add_argument(
        "--size",
        type=str,
        default="auto",
        help="Canvas size as WIDTHxHEIGHT or 'auto' to detect terminal size.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for deterministic fireworks.",
    )
    return parser.parse_args()


def detect_size(size_flag: str) -> tuple[int, int]:
    if size_flag != "auto":
        try:
            width_str, height_str = size_flag.lower().split("x", 1)
            return int(width_str), int(height_str)
        except ValueError as exc:  # pragma: no cover - defensive parsing
            raise argparse.ArgumentTypeError("Size must be WIDTHxHEIGHT or 'auto'.") from exc

    width, height = shutil.get_terminal_size((80, 24))
    # Leave a tiny border to avoid scrolling when the terminal wraps.
    return max(40, width - 1), max(15, height - 1)


def main() -> None:
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    width, height = detect_size(args.size)
    show = FireworkShow(width=width, height=height)

    print("\033[2J", end="")  # Clear screen
    for frame in range(args.frames):
        show.step()
        frame_data = show.render()
        print("\033[H" + frame_data + f"\n\nFrame {frame + 1}/{args.frames}", end="")
        time.sleep(args.interval)

    print("\033[0m\nThanks for watching the show!\n")


if __name__ == "__main__":
    main()
