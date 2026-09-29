import cv2

from vision.camera import Camera
from vision.hand_tracker import HandTracker
from vision.gesture_detector import GestureDetector


camera = Camera()

tracker = HandTracker(
    model_path="models/gesture_recognizer.task"
)

detector = GestureDetector()


try:

    while True:

        success, frame = camera.read()

        if not success:
            break

        hands = tracker.process(frame)

        if hands:
            hand = hands[0]

            event = detector.update(hand)

            if event:

                print(
                    event.name,
                    event.direction,
                    event.dx,
                    event.dy
                )

        else:
            detector.update(None)

        tracker.draw_landmarks(
            frame,
            hands
        )

        cv2.putText(
            frame,
            f"FPS: {camera.get_fps():.0f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "GestureCube Vision Test",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


finally:

    camera.release()

    tracker.close()

    cv2.destroyAllWindows()