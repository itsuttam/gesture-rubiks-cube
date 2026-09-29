import pygame

from OpenGL.GL import (
    glTranslatef,
    glRotatef
)


class MouseController:
    def __init__(self, distance=11.0):

        self.yaw = -35.0
        self.pitch = 25.0
        self.distance = distance

        # Cube position inside camera frame
        self.position_x = 2.8
        self.position_y = 0.0

        self.dragging = False

        self.mouse_sensitivity = 0.4
        self.zoom_speed = 0.8

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                self.dragging = True

            # Older pygame mouse wheel support
            elif event.button == 4:
                self.zoom(-self.zoom_speed)

            elif event.button == 5:
                self.zoom(self.zoom_speed)

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:
                self.dragging = False

        elif (
            event.type == pygame.MOUSEMOTION
            and self.dragging
        ):

            dx, dy = event.rel

            self.orbit(
                dx,
                dy
            )

        elif event.type == pygame.MOUSEWHEEL:

            self.zoom(
                -event.y * self.zoom_speed
            )

    #orbit
    def orbit(
        self,
        dx,
        dy
    ):
        self.yaw += (
            dx * self.mouse_sensitivity
        )

        self.pitch += (
            dy * self.mouse_sensitivity
        )

    #gesture orbit
    def gesture_orbit(
        self,
        dx,
        dy
    ):
        """
        dx/dy coming from MediaPipe are normalized,
        so they need a larger multiplier.
        """

        gesture_sensitivity = 250

        self.yaw += (
            dx * gesture_sensitivity
        )

        self.pitch += (
            dy * gesture_sensitivity
        )

    #90 degree rotation
    def rotate_view(
        self,
        direction
    ):

        if direction == "RIGHT":
            self.yaw += 90

        elif direction == "LEFT":
            self.yaw -= 90

        elif direction == "UP":
            self.pitch -= 90

        elif direction == "DOWN":
            self.pitch += 90

    #zoom
    def zoom(
        self,
        amount
    ):
        self.distance += amount

        self.distance = max(
            5.0,
            min(
                self.distance,
                25.0
            )
        )

    #aaply camera
    def apply_camera(self):

        glTranslatef(
            self.position_x,
            self.position_y,
            -self.distance
        )

        glRotatef(
            self.pitch,
            1,
            0,
            0
        )

        glRotatef(
            self.yaw,
            0,
            1,
            0
        )