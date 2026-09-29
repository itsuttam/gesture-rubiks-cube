from pathlib import Path

import cv2
import pygame

from pygame.locals import DOUBLEBUF, OPENGL

from OpenGL.GL import (
    glClear,
    glClearColor,
    glEnable,
    glLoadIdentity,
    glMatrixMode,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_MODELVIEW,
    GL_PROJECTION,
)

from OpenGL.GLU import gluPerspective


# cube
from cube.cube import Cube
from cube.renderer import CubeRenderer


# controls
from controls.keyboard_controller import KeyboardController
from controls.mouse_controller import MouseController
from controls.gesture_controller import GestureController


# vision
from vision.camera import Camera
from vision.hand_tracker import HandTracker
from vision.gesture_detector import GestureDetector
from vision.camera_background import CameraBackground


# settings
FPS = 60


# opengl
def setup_opengl(width, height):
    glEnable(GL_DEPTH_TEST)

    glClearColor(
        0.08,
        0.08,
        0.10,
        1.0
    )

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        45,
        width / height,
        0.1,
        100.0
    )

    glMatrixMode(GL_MODELVIEW)


# main
def main():
    pygame.init()

    # screen
    display_info = pygame.display.Info()

    window_width = display_info.current_w
    window_height = display_info.current_h

    print(
        f"Screen: {window_width}x{window_height}"
    )

    # opengl context
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_MAJOR_VERSION,
        2
    )

    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_MINOR_VERSION,
        1
    )

    pygame.display.gl_set_attribute(
        pygame.GL_DEPTH_SIZE,
        24
    )

    # fullscreen window
    # window
    pygame.display.set_mode(
        (
            window_width,
            window_height
        ),
        pygame.DOUBLEBUF
        | pygame.OPENGL
        | pygame.NOFRAME
    )

    pygame.display.set_caption(
        "GestureCube"
    )

    setup_opengl(
        window_width,
        window_height
    )

    clock = pygame.time.Clock()

    # camera background
    camera_background = CameraBackground()

    # cube
    cube = Cube()
    renderer = CubeRenderer()

    # controls
    keyboard = KeyboardController()
    mouse = MouseController()

    gestures = GestureController(
        cube,
        mouse
    )

    # model
    project_root = (
        Path(__file__)
        .resolve()
        .parent
    )

    model_path = (
        project_root
        / "models"
        / "gesture_recognizer.task"
    )

    # vision
    camera = None
    hand_tracker = None
    gesture_detector = None

    vision_enabled = False

    if model_path.exists():
        try:
            camera = Camera(
                camera_index=0,
                width=1280,
                height=720
            )

            hand_tracker = HandTracker(
                model_path=str(model_path),
                num_hands=1
            )

            gesture_detector = GestureDetector()

            vision_enabled = True

            print(
                "Camera + MediaPipe enabled"
            )

        except Exception as error:
            print(
                "Could not start vision:"
            )

            print(error)

    else:
        print(
            "Gesture model not found:"
        )

        print(model_path)

    # loop
    running = True

    try:
        while running:

            # events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    running = False

                # keyboard
                selected_face = (
                    keyboard.handle_event(
                        event,
                        cube
                    )
                )

                if selected_face:
                    gestures.set_selected_face(
                        selected_face
                    )

                # mouse
                mouse.handle_event(
                    event
                )

            current_gesture = "None"

            # camera
            if vision_enabled:

                success, frame = camera.read()

                if success:

                    # hand tracking
                    hands = hand_tracker.process(
                        frame
                    )

                    if hands:
                        hand = hands[0]

                        current_gesture = (
                            hand.gesture
                        )

                        gesture_event = (
                            gesture_detector.update(
                                hand
                            )
                        )

                        if gesture_event:
                            gestures.handle(
                                gesture_event
                            )

                    else:
                        gesture_detector.update(
                            None
                        )

                    # landmarks
                    hand_tracker.draw_landmarks(
                        frame,
                        hands
                    )

                    # ui
                    cv2.putText(
                        frame,
                        f"Gesture: {current_gesture}",
                        (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        (
                            "Selected: "
                            f"{gestures.selected_face}"
                        ),
                        (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        (
                            "Action: "
                            f"{gestures.last_action}"
                        ),
                        (20, 105),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        (
                            "FPS: "
                            f"{camera.get_fps():.0f}"
                        ),
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

                    # camera texture
                    camera_background.update(
                        frame
                    )

            # render
            glClear(
                GL_COLOR_BUFFER_BIT
                |
                GL_DEPTH_BUFFER_BIT
            )

            # background
            if vision_enabled:
                camera_background.draw()

            # 3d projection
            glMatrixMode(
                GL_PROJECTION
            )

            glLoadIdentity()

            gluPerspective(
                45,
                window_width / window_height,
                0.1,
                100.0
            )

            glMatrixMode(
                GL_MODELVIEW
            )

            glLoadIdentity()

            # cube
            mouse.apply_camera()

            renderer.draw(
                cube
            )

            # display
            pygame.display.flip()

            pygame.display.set_caption(
                (
                    "GestureCube | "
                    f"Gesture: {current_gesture} | "
                    f"Face: {gestures.selected_face}"
                )
            )

            clock.tick(FPS)

    # cleanup
    finally:

        if camera:
            camera.release()

        if hand_tracker:
            hand_tracker.close()

        cv2.destroyAllWindows()

        pygame.quit()


# run
if __name__ == "__main__":
    main()