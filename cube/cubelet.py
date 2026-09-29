from dataclasses import dataclass, field
from typing import Dict, Tuple


Vector3 = Tuple[int, int, int]


@dataclass
class Cubelet:
    """
    Represents one small cube inside a 3x3x3 Rubik's Cube.

    Position coordinates:
        x = -1 -> left
        x =  0 -> middle
        x =  1 -> right

        y = -1 -> bottom
        y =  0 -> middle
        y =  1 -> top

        z = -1 -> back
        z =  0 -> middle
        z =  1 -> front

    stickers:
        Dictionary where the key is the direction
        of a sticker and the value is its color.

    Example:

        {
            (1, 0, 0): "red",
            (0, 1, 0): "white",
            (0, 0, 1): "green"
        }
    """

    position: Vector3
    stickers: Dict[Vector3, str] = field(default_factory=dict)

    def get_position(self) -> Vector3:
        return self.position

    def set_position(self, position: Vector3):
        self.position = position

    def get_stickers(self):
        return self.stickers

    def set_stickers(self, stickers):
        self.stickers = stickers

    def has_sticker(self, direction: Vector3) -> bool:
        """
        Check if this cubelet has a sticker
        pointing in a specific direction.
        """

        return direction in self.stickers

    def get_sticker_color(self, direction: Vector3):
        """
        Return sticker color for a direction.

        Returns None if no sticker exists.
        """

        return self.stickers.get(direction)

    def __repr__(self):
        return (
            f"Cubelet("
            f"position={self.position}, "
            f"stickers={self.stickers}"
            f")"
        )