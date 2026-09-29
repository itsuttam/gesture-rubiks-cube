import cv2
import time


class Camera:
    def __init__(
        self,
        camera_index=0,
        width=1280,
        height=720,
        mirror=True
    ):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.mirror = mirror

        self.capture = cv2.VideoCapture(camera_index)

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Could not open camera {camera_index}"
            )

        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height
        )

        self.previous_time = time.perf_counter()
        self.fps = 0.0

    def read(self):
        """
        Read one frame from the camera.

        Returns:
            success, frame
        """

        success, frame = self.capture.read()

        if not success:
            return False, None

        if self.mirror:
            frame = cv2.flip(frame, 1)

        self._calculate_fps()

        return True, frame

    def _calculate_fps(self):
        current_time = time.perf_counter()

        delta = current_time - self.previous_time

        if delta > 0:
            current_fps = 1.0 / delta

            # Smooth FPS instead of letting it jump wildly
            if self.fps == 0:
                self.fps = current_fps
            else:
                self.fps = (
                    self.fps * 0.9
                    + current_fps * 0.1
                )

        self.previous_time = current_time

    def get_fps(self):
        return self.fps

    def release(self):
        if self.capture:
            self.capture.release()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        self.release()