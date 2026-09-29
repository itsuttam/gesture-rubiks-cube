from collections import deque
from dataclasses import dataclass
from typing import Optional
import math
import time


@dataclass
class GestureEvent:
    name: str

    direction: Optional[str] = None

    dx: float = 0.0
    dy: float = 0.0

    confidence: float = 1.0


class GestureDetector:
    def __init__(self):

        # Palm movement history
        self.palm_history = deque(
            maxlen=30
        )

        # Index finger movement history
        self.index_history = deque(
            maxlen=60
        )

        self.previous_palm = None

        # Pinch information
        self.pinching = False
        self.pinch_start = None

        # Prevent one movement from firing repeatedly
        self.last_action_time = 0.0

        self.cooldown = 0.40

    
    # DISTANCE
    

    @staticmethod
    def distance(a, b):
        return math.sqrt(
            (a.x - b.x) ** 2
            +
            (a.y - b.y) ** 2
        )

    
    # PALM CENTER
    

    @staticmethod
    def palm_center(landmarks):
        """
        Approximate palm center using:
        wrist + finger MCP joints
        """

        indexes = [
            0,
            5,
            9,
            13,
            17
        ]

        x = sum(
            landmarks[i].x
            for i in indexes
        ) / len(indexes)

        y = sum(
            landmarks[i].y
            for i in indexes
        ) / len(indexes)

        return x, y

    
    # HAND SIZE
    

    def hand_size(self, landmarks):
        """
        Used to normalize pinch distance.

        Wrist -> middle MCP.
        """

        wrist = landmarks[0]
        middle_mcp = landmarks[9]

        size = self.distance(
            wrist,
            middle_mcp
        )

        return max(
            size,
            0.001
        )

    
    # PINCH
    

    def is_pinching(self, landmarks):

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        pinch_distance = self.distance(
            thumb_tip,
            index_tip
        )

        normalized_distance = (
            pinch_distance
            /
            self.hand_size(landmarks)
        )

        return normalized_distance < 0.35

    
    # MOVEMENT DIRECTION
    

    @staticmethod
    def movement_direction(dx, dy):

        if abs(dx) > abs(dy):

            if dx > 0:
                return "RIGHT"

            return "LEFT"

        if dy > 0:
            return "DOWN"

        return "UP"

    
    # COOLDOWN
    

    def can_trigger(self):

        now = time.monotonic()

        return (
            now - self.last_action_time
            >= self.cooldown
        )

    def trigger(self):
        self.last_action_time = time.monotonic()

    
    # SWIPE
    

    def detect_swipe(self):

        if len(self.palm_history) < 5:
            return None

        start_time, start_x, start_y = (
            self.palm_history[0]
        )

        end_time, end_x, end_y = (
            self.palm_history[-1]
        )

        duration = (
            end_time - start_time
        )

        if duration <= 0:
            return None

        dx = end_x - start_x
        dy = end_y - start_y

        distance = math.sqrt(
            dx ** 2
            +
            dy ** 2
        )

        if distance < 0.18:
            return None

        direction = self.movement_direction(
            dx,
            dy
        )

        return GestureEvent(
            name="SWIPE",
            direction=direction,
            dx=dx,
            dy=dy
        )

    
    # FLICK
    

    def detect_flick(self):

        if len(self.palm_history) < 3:
            return None

        start_time, start_x, start_y = (
            self.palm_history[0]
        )

        end_time, end_x, end_y = (
            self.palm_history[-1]
        )

        duration = (
            end_time - start_time
        )

        if duration <= 0:
            return None

        dx = end_x - start_x
        dy = end_y - start_y

        distance = math.sqrt(
            dx ** 2
            +
            dy ** 2
        )

        speed = distance / duration

        if (
            duration <= 0.25
            and distance >= 0.12
            and speed >= 0.8
        ):

            return GestureEvent(
                name="FLICK",
                direction=self.movement_direction(
                    dx,
                    dy
                ),
                dx=dx,
                dy=dy
            )

        return None

    
    # CIRCLE
    

    def detect_circle(self):

        if len(self.index_history) < 12:
            return None

        points = [
            (x, y)
            for _, x, y
            in self.index_history
        ]

        xs = [
            p[0]
            for p in points
        ]

        ys = [
            p[1]
            for p in points
        ]

        width = max(xs) - min(xs)
        height = max(ys) - min(ys)

        # Circle is too small
        if width < 0.07 or height < 0.07:
            return None

        aspect_ratio = (
            width / max(height, 0.001)
        )

        # Avoid long straight/oval shapes
        if not 0.5 <= aspect_ratio <= 2.0:
            return None

        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)

        angles = []

        for x, y in points:

            angle = math.atan2(
                y - center_y,
                x - center_x
            )

            angles.append(angle)

        total_angle = 0.0

        for index in range(
            1,
            len(angles)
        ):

            difference = (
                angles[index]
                -
                angles[index - 1]
            )

            # Unwrap angle
            while difference > math.pi:
                difference -= 2 * math.pi

            while difference < -math.pi:
                difference += 2 * math.pi

            total_angle += difference

        # Require almost a full circle
        if abs(total_angle) < 5.0:
            return None

        start_x, start_y = points[0]
        end_x, end_y = points[-1]

        closing_distance = math.sqrt(
            (end_x - start_x) ** 2
            +
            (end_y - start_y) ** 2
        )

        radius = (
            width + height
        ) / 4

        if closing_distance > radius:
            return None

        # Image coordinates increase downward,
        # so positive rotation appears clockwise.
        if total_angle > 0:
            direction = "CLOCKWISE"
        else:
            direction = "COUNTERCLOCKWISE"

        return GestureEvent(
            name="CIRCLE",
            direction=direction
        )

    
    # MAIN UPDATE
    

    def update(self, hand):
        """
        Call this once per frame.

        Returns GestureEvent or None.
        """

        if hand is None:
            self.reset_tracking()
            return None

        landmarks = hand.landmarks
        now = time.monotonic()

        palm_x, palm_y = self.palm_center(
            landmarks
        )

        index_tip = landmarks[8]

        # Store movements
        self.palm_history.append(
            (
                now,
                palm_x,
                palm_y
            )
        )

        self.index_history.append(
            (
                now,
                index_tip.x,
                index_tip.y
            )
        )

        # Keep only recent palm data
        while (
            self.palm_history
            and
            now - self.palm_history[0][0]
            > 0.45
        ):
            self.palm_history.popleft()

        # Circle gets a longer history
        while (
            self.index_history
            and
            now - self.index_history[0][0]
            > 1.25
        ):
            self.index_history.popleft()

        # ----------------------------------------------
        # PINCH
        # ----------------------------------------------

        pinching_now = self.is_pinching(
            landmarks
        )

        if pinching_now:

            if not self.pinching:

                self.pinching = True

                self.pinch_start = (
                    index_tip.x,
                    index_tip.y
                )

                return GestureEvent(
                    name="PINCH_START"
                )

            if self.pinch_start:

                dx = (
                    index_tip.x
                    -
                    self.pinch_start[0]
                )

                dy = (
                    index_tip.y
                    -
                    self.pinch_start[1]
                )

                return GestureEvent(
                    name="PINCH_DRAG",
                    direction=(
                        self.movement_direction(
                            dx,
                            dy
                        )
                        if abs(dx) + abs(dy) > 0.02
                        else None
                    ),
                    dx=dx,
                    dy=dy
                )

        elif self.pinching:

            self.pinching = False
            self.pinch_start = None

            return GestureEvent(
                name="PINCH_END"
            )

        # ----------------------------------------------
        # CLOSED FIST → CAMERA ORBIT
        # ----------------------------------------------

        if hand.gesture == "Closed_Fist":

            if self.previous_palm:

                dx = (
                    palm_x
                    -
                    self.previous_palm[0]
                )

                dy = (
                    palm_y
                    -
                    self.previous_palm[1]
                )

                self.previous_palm = (
                    palm_x,
                    palm_y
                )

                return GestureEvent(
                    name="ORBIT",
                    direction=self.movement_direction(
                        dx,
                        dy
                    ),
                    dx=dx,
                    dy=dy,
                    confidence=hand.gesture_score
                )

            self.previous_palm = (
                palm_x,
                palm_y
            )

            return GestureEvent(
                name="FIST",
                confidence=hand.gesture_score
            )

        self.previous_palm = (
            palm_x,
            palm_y
        )

        # ----------------------------------------------
        # POINT + CIRCLE
        # ----------------------------------------------

        if hand.gesture == "Pointing_Up":

            circle = self.detect_circle()

            if (
                circle
                and self.can_trigger()
            ):

                self.trigger()

                self.index_history.clear()

                return circle

            return GestureEvent(
                name="POINT",
                confidence=hand.gesture_score
            )

        # ----------------------------------------------
        # OPEN PALM
        # ----------------------------------------------

        if hand.gesture == "Open_Palm":

            # Check fast flick first
            flick = self.detect_flick()

            if (
                flick
                and self.can_trigger()
            ):

                self.trigger()

                self.palm_history.clear()

                return flick

            swipe = self.detect_swipe()

            if (
                swipe
                and self.can_trigger()
            ):

                self.trigger()

                self.palm_history.clear()

                return swipe

            return GestureEvent(
                name="OPEN_PALM",
                confidence=hand.gesture_score
            )

        return GestureEvent(
            name=hand.gesture.upper(),
            confidence=hand.gesture_score
        )

    

    def reset_tracking(self):

        self.palm_history.clear()
        self.index_history.clear()

        self.pinching = False
        self.pinch_start = None

        self.previous_palm = None