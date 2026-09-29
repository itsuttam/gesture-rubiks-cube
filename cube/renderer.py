import pygame

from OpenGL.GL import (
    glBegin,
    glEnd,
    glVertex3fv,
    glColor3fv,
    glLineWidth,
    glPushMatrix,
    glPopMatrix,
    glTranslatef,
    GL_QUADS,
    GL_LINES
)


# --------------------------------------------
# COLORS
# --------------------------------------------

COLORS = {
    "white": (
        1.0,
        1.0,
        1.0
    ),

    "yellow": (
        1.0,
        1.0,
        0.0
    ),

    "red": (
        1.0,
        0.0,
        0.0
    ),

    "orange": (
        1.0,
        0.5,
        0.0
    ),

    "green": (
        0.0,
        1.0,
        0.0
    ),

    "blue": (
        0.0,
        0.0,
        1.0
    ),

    "black": (
        0.03,
        0.03,
        0.03
    )
}


# --------------------------------------------
# CUBE GEOMETRY
# --------------------------------------------

VERTICES = [
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),

    (-0.5, -0.5, 0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),
    (-0.5, 0.5, 0.5),
]


# Each face has 4 vertex indexes

FACES = {
    # Front
    (0, 0, 1): (
        4,
        5,
        6,
        7
    ),

    # Back
    (0, 0, -1): (
        1,
        0,
        3,
        2
    ),

    # Right
    (1, 0, 0): (
        5,
        1,
        2,
        6
    ),

    # Left
    (-1, 0, 0): (
        0,
        4,
        7,
        3
    ),

    # Up
    (0, 1, 0): (
        7,
        6,
        2,
        3
    ),

    # Down
    (0, -1, 0): (
        0,
        1,
        5,
        4
    )
}


EDGES = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),

    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),

    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]


class CubeRenderer:
    def __init__(
        self,
        cubelet_size=0.92,
        spacing=1.05
    ):

        self.cubelet_size = cubelet_size
        self.spacing = spacing

    # ----------------------------------------
    # GET COLOR
    # ----------------------------------------

    def _get_face_color(
        self,
        cubelet,
        face_direction
    ):
        """
        Return sticker color for a face.

        Internal cube faces are black.
        """

        color_name = cubelet.stickers.get(
            face_direction,
            "black"
        )

        return COLORS.get(
            color_name,
            COLORS["black"]
        )

    # ----------------------------------------
    # DRAW ONE FACE
    # ----------------------------------------

    def _draw_face(
        self,
        cubelet,
        direction,
        vertex_indices
    ):

        color = self._get_face_color(
            cubelet,
            direction
        )

        glColor3fv(color)

        glBegin(GL_QUADS)

        for vertex_index in vertex_indices:

            vertex = VERTICES[
                vertex_index
            ]

            scaled_vertex = (
                vertex[0]
                * self.cubelet_size,

                vertex[1]
                * self.cubelet_size,

                vertex[2]
                * self.cubelet_size
            )

            glVertex3fv(
                scaled_vertex
            )

        glEnd()

    # ----------------------------------------
    # DRAW EDGES
    # ----------------------------------------

    def _draw_edges(self):

        glColor3fv(
            COLORS["black"]
        )

        glLineWidth(3)

        glBegin(GL_LINES)

        for edge in EDGES:

            for vertex_index in edge:

                vertex = VERTICES[
                    vertex_index
                ]

                scaled_vertex = (
                    vertex[0]
                    * self.cubelet_size,

                    vertex[1]
                    * self.cubelet_size,

                    vertex[2]
                    * self.cubelet_size
                )

                glVertex3fv(
                    scaled_vertex
                )

        glEnd()

    # ----------------------------------------
    # DRAW ONE CUBELET
    # ----------------------------------------

    def draw_cubelet(
        self,
        cubelet
    ):

        x, y, z = cubelet.position

        glPushMatrix()

        glTranslatef(
            x * self.spacing,
            y * self.spacing,
            z * self.spacing
        )

        for direction, face_vertices in FACES.items():

            self._draw_face(
                cubelet,
                direction,
                face_vertices
            )

        self._draw_edges()

        glPopMatrix()

    # ----------------------------------------
    # DRAW COMPLETE CUBE
    # ----------------------------------------

    def draw(
        self,
        cube
    ):
        """
        Draw every cubelet.
        """

        for cubelet in cube.cubelets:

            self.draw_cubelet(
                cubelet
            )