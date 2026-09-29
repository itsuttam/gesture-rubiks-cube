import os
from dataclasses import dataclass
from typing import Any, List

import cv2
import mediapipe as mp
import numpy as np



# HAND CONNECTIONS


HAND_CONNECTIONS = [
    # Thumb
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),

    # Index
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),

    # Middle
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),

    # Ring
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),

    # Pinky
    (13, 17),
    (17, 18),
    (18, 19),
    (19, 20),

    # Palm
    (0, 17)
]


@dataclass
class HandData:
    landmarks: List[Any]

    handedness: str = "Unknown"
    handedness_score: float = 0.0

    gesture: str = "None"
    gesture_score: float = 0.0


class HandTracker:
    def __init__(
        self,
        model_path="models/gesture_recognizer.task",
        num_hands=1,
        minimum_confidence=0.5
    ):

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                "\nMediaPipe model was not found:\n"
                f"{model_path}\n\n"
                "Create the models/ folder and place "
                "gesture_recognizer.task inside it."
            )

        self.minimum_confidence = minimum_confidence

        BaseOptions = mp.tasks.BaseOptions

        GestureRecognizer = (
            mp.tasks.vision.GestureRecognizer
        )

        GestureRecognizerOptions = (
            mp.tasks.vision.GestureRecognizerOptions
        )

        RunningMode = (
            mp.tasks.vision.RunningMode
        )

        options = GestureRecognizerOptions(
            base_options=BaseOptions(
                model_asset_path=model_path
            ),

            running_mode=RunningMode.IMAGE,

            num_hands=num_hands,

            min_hand_detection_confidence=0.5,

            min_hand_presence_confidence=0.5,

            min_tracking_confidence=0.5
        )

        self.recognizer = (
            GestureRecognizer.create_from_options(
                options
            )
        )

    
    # PROCESS FRAME
    

    def process(self, frame):
        """
        Detect hand landmarks and gestures.

        Returns:
            List[HandData]
        """

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        rgb_frame = np.ascontiguousarray(
            rgb_frame
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.recognizer.recognize(
            mp_image
        )

        hands = []

        if not result.hand_landmarks:
            return hands

        for index, landmarks in enumerate(
            result.hand_landmarks
        ):

            handedness = "Unknown"
            handedness_score = 0.0

            gesture = "None"
            gesture_score = 0.0

            # --------------------------------
            # HANDEDNESS
            # --------------------------------

            if (
                result.handedness
                and index < len(result.handedness)
                and result.handedness[index]
            ):

                hand_category = (
                    result.handedness[index][0]
                )

                handedness = (
                    hand_category.category_name
                    or hand_category.display_name
                    or "Unknown"
                )

                handedness_score = (
                    hand_category.score
                )

            # --------------------------------
            # GESTURE
            # --------------------------------

            if (
                result.gestures
                and index < len(result.gestures)
                and result.gestures[index]
            ):

                gesture_category = (
                    result.gestures[index][0]
                )

                if (
                    gesture_category.score
                    >= self.minimum_confidence
                ):
                    gesture = (
                        gesture_category.category_name
                        or "None"
                    )

                    gesture_score = (
                        gesture_category.score
                    )

            hands.append(
                HandData(
                    landmarks=landmarks,
                    handedness=handedness,
                    handedness_score=handedness_score,
                    gesture=gesture,
                    gesture_score=gesture_score
                )
            )

        return hands

    
    # DRAW LANDMARKS
    

    def draw_landmarks(
        self,
        frame,
        hands
    ):
        """
        Draw hand skeleton on OpenCV frame.
        """

        height, width = frame.shape[:2]

        for hand in hands:

            landmarks = hand.landmarks

            # -------------------------------
            # CONNECTION LINES
            # -------------------------------

            for start_index, end_index in HAND_CONNECTIONS:

                start = landmarks[start_index]
                end = landmarks[end_index]

                start_point = (
                    int(start.x * width),
                    int(start.y * height)
                )

                end_point = (
                    int(end.x * width),
                    int(end.y * height)
                )

                cv2.line(
                    frame,
                    start_point,
                    end_point,
                    (200, 200, 200),
                    2
                )

            # -------------------------------
            # LANDMARK POINTS
            # -------------------------------

            for landmark in landmarks:

                point = (
                    int(landmark.x * width),
                    int(landmark.y * height)
                )

                cv2.circle(
                    frame,
                    point,
                    4,
                    (0, 255, 0),
                    -1
                )

            # -------------------------------
            # TEXT
            # -------------------------------

            wrist = landmarks[0]

            text_position = (
                int(wrist.x * width),
                int(wrist.y * height) - 20
            )

            text = (
                f"{hand.handedness} | "
                f"{hand.gesture} "
                f"{hand.gesture_score:.2f}"
            )

            cv2.putText(
                frame,
                text,
                text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        return frame

    

    def close(self):
        if self.recognizer:
            self.recognizer.close()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        self.close()