from dataclasses import dataclass, field
from typing import Dict, Tuple
import random

Vector3 = Tuple[int, int, int]

WHITE = "white"
YELLOW = "yellow"
RED = "red"
ORANGE = "orange"
GREEN = "green"
BLUE = "blue"


@dataclass
class Cubelet:
    """
    One small cube inside the 3x3x3 Rubik's Cube.
    position:
        x = -1 left, 0 middle, 1 right
        y = -1 bottom, 0 middle, 1 top
        z = -1 back, 0 middle, 1 front

    stickers:
        Maps a face direction to its color.
    """
    position: Vector3
    stickers: Dict[Vector3, str] = field(default_factory=dict)


class Cube:
    def __init__(self):
        self.cubelets = []
        self.create_cube()

    def create_cube(self):
        """Create a solved 3x3x3 Rubik's Cube."""

        self.cubelets.clear()

        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):

                    stickers = {}
                    if x == 1:
                        stickers[(1, 0, 0)] = RED
                    if x == -1:
                        stickers[(-1, 0, 0)] = ORANGE
                    if y == 1:
                        stickers[(0, 1, 0)] = WHITE
                    if y == -1:
                        stickers[(0, -1, 0)] = YELLOW
                    if z == 1:
                        stickers[(0, 0, 1)] = GREEN
                    if z == -1:
                        stickers[(0, 0, -1)] = BLUE

                    cubelet = Cubelet(position=(x, y, z), stickers=stickers)
                    self.cubelets.append(cubelet)

    def _rotate_vector_90(
        self,
        vector: Vector3,
        axis: str,
        direction: int
    ) -> Vector3:
        x, y, z = vector

        if direction not in (-1, 1):
            raise ValueError("Direction must be 1 or -1.")
        # Rotate around X axis
        if axis == "x":
            if direction == 1:
                return x, -z, y
            return x, z, -y
        # Rotate around Y axis
        elif axis == "y":
            if direction == 1:
                return z, y, -x
            return -z, y, x
        # Rotate around Z axis
        elif axis == "z":
            if direction == 1:
                return -y, x, z
            return y, -x, z
        else:
            raise ValueError("Axis must be x, y or z.")

    def _rotate_layer(
        self,
        axis: str,
        layer: int,
        direction: int
    ):
        """
        Rotate one layer by 90 degrees.

        axis:
            x, y or z

        layer:
            -1, 0 or 1

        direction:
            1  = +90 degrees
            -1 = -90 degrees
        """

        axis_index = {
            "x": 0,
            "y": 1,
            "z": 2
        }

        index = axis_index[axis]

        for cubelet in self.cubelets:

            position = cubelet.position

            # Ignore cubelets that are not in selected layer
            if position[index] != layer:
                continue

            # Rotate cubelet position
            cubelet.position = self._rotate_vector_90(
                position,
                axis,
                direction
            )

            # Rotate sticker directions
            rotated_stickers = {}

            for normal, color in cubelet.stickers.items():

                new_normal = self._rotate_vector_90(
                    normal,
                    axis,
                    direction
                )

                rotated_stickers[new_normal] = color

            cubelet.stickers = rotated_stickers

    def rotate_face(self, face: str, angle: int = 90):
        """
        Rotate one Rubik's Cube face.

        Examples:

        cube.rotate_face("R", 90)
        cube.rotate_face("R", -90)
        cube.rotate_face("F", 180)
        """

        face = face.upper()

        if face not in ["R", "L", "U", "D", "F", "B"]:
            raise ValueError(
                "Face must be R, L, U, D, F or B."
            )

        if angle not in (-180, -90, 90, 180):
            raise ValueError(
                "Angle must be -180, -90, 90 or 180."
            )

        face_data = {

            # face: (axis, layer, clockwise direction)

            "R": ("x", 1, -1),
            "L": ("x", -1, 1),

            "U": ("y", 1, -1),
            "D": ("y", -1, 1),

            "F": ("z", 1, -1),
            "B": ("z", -1, 1),
        }

        axis, layer, clockwise = face_data[face]

        # Number of 90 degree rotations
        turns = abs(angle) // 90

        # Negative angle means counterclockwise
        if angle < 0:
            clockwise *= -1

        for _ in range(turns):

            self._rotate_layer(
                axis,
                layer,
                clockwise
            )
    # reset
    def reset(self):
        """Return cube to solved state."""

        self.create_cube()

    def scramble(self, moves: int = 20):
        """Randomly scramble the Rubik's Cube."""

        faces = [
            "R",
            "L",
            "U",
            "D",
            "F",
            "B"
        ]

        angles = [
            90,
            -90,
            180
        ]

        scramble_moves = []

        previous_face = None

        for _ in range(moves):

            available_faces = [
                face
                for face in faces
                if face != previous_face
            ]

            face = random.choice(available_faces)

            angle = random.choice(angles)

            self.rotate_face(
                face,
                angle
            )

            scramble_moves.append(
                (face, angle)
            )

            previous_face = face

        return scramble_moves


    def get_cubelet(
        self,
        x: int,
        y: int,
        z: int
        ):

        for cubelet in self.cubelets:
            if cubelet.position == (x, y, z):
                return cubelet
        return None
    
    def print_cubelets(self):

        for cubelet in self.cubelets:

            print(
                "Position:",
                cubelet.position,
                "Stickers:",
                cubelet.stickers
            )

if __name__ == "__main__":
    cube = Cube()
    print("Cube created")
    print("Cubelets:", len(cube.cubelets))
    print("\nRotate Right Face")
    cube.rotate_face("R", 90)
    cube.print_cubelets()
    print("\nScramble")
    moves = cube.scramble(10)
    print("Scramble moves:")

    for face, angle in moves:
        print(face, angle)
    print("\nReset cube")
    cube.reset()
    print("Cubelets:", len(cube.cubelets))