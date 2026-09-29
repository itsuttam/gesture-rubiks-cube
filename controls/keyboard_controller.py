import pygame


class KeyboardController:
    """
    Keyboard controls:

    R -> Right face
    L -> Left face
    U -> Up face
    D -> Down face
    F -> Front face
    B -> Back face

    Shift + face -> counterclockwise
    Ctrl + face  -> 180 degrees

    Space -> reset cube
    S     -> scramble cube
    """

    def __init__(self):
        self.face_keys = {
            pygame.K_r: "R",
            pygame.K_l: "L",
            pygame.K_u: "U",
            pygame.K_d: "D",
            pygame.K_f: "F",
            pygame.K_b: "B",
        }

    def handle_event(self, event, cube):
        """
        Process keyboard input.

        Returns selected face if a face was rotated.
        Otherwise returns None.
        """

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_SPACE:
            cube.reset()

            print("Cube reset")

            return None

        if event.key == pygame.K_s:
            moves = cube.scramble(20)

            print("Scramble:")
            print(moves)

            return None

        if event.key in self.face_keys:

            face = self.face_keys[event.key]

            angle = 90

            # Shift = counterclockwise
            if event.mod & pygame.KMOD_SHIFT:
                angle = -90

            # Ctrl = 180 degrees
            elif event.mod & pygame.KMOD_CTRL:
                angle = 180

            cube.rotate_face(
                face,
                angle
            )

            print(
                f"Rotate {face}: {angle}°"
            )

            return face

        return None