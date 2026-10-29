"""Profile cards package.

Generates dark SVG profile cards from the SpreadSheets600 snapshot API.
Only two canvas sizes exist: FULL_W (830) and HALF_W (410).
"""

from .theme import FULL_W, HALF_W, PAD, GAP, RADIUS

__all__ = ["FULL_W", "HALF_W", "PAD", "GAP", "RADIUS"]
