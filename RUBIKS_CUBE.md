# Gesture-Controlled Rubik’s Cube

## Project Overview

Build a 3D Rubik’s Cube simulator in Python that can be controlled using hand gestures captured through a laptop camera.

The project will combine:

* Python
* OpenCV
* MediaPipe
* NumPy
* Pygame
* PyOpenGL
* Computer Vision
* Gesture Recognition
* 3D Graphics
* Human-Computer Interaction

The user should be able to rotate the Rubik’s Cube, move the camera, select cube faces, and rotate cube layers using natural hand gestures.

---

# Main Features

## 1. 3D Rubik’s Cube

Create a fully functional 3×3×3 Rubik’s Cube.

The cube should contain:

* 27 cubelets
* 6 colored faces
* Smooth rotations
* 90-degree turns
* 180-degree turns
* Clockwise rotations
* Counterclockwise rotations

Standard Rubik’s Cube colors:

| Face  | Color  |
| ----- | ------ |
| Front | Green  |
| Back  | Blue   |
| Left  | Orange |
| Right | Red    |
| Up    | White  |
| Down  | Yellow |

---

# 2. Cube Controls

Initially support keyboard and mouse controls before implementing gestures.

## Keyboard Controls

```text
R → Rotate right face

L → Rotate left face

U → Rotate upper face

D → Rotate bottom face

F → Rotate front face

B → Rotate back face
```

Optional inverse turns:

```text
Shift + R → R'
Shift + L → L'
Shift + U → U'
Shift + D → D'
Shift + F → F'
Shift + B → B'
```

---

# 3. Mouse Controls

Implement a mouse simulation mode.

This will make development easier when a camera is unavailable.

Controls:

```text
Left Mouse Drag
→ Orbit camera

Mouse Wheel
→ Zoom camera

Click Cube Face
→ Select face

Drag Selected Face
→ Rotate cube layer
```

---

# 4. Laptop Camera

Use the laptop's built-in webcam.

OpenCV will capture video frames.

Basic camera setup:

```python
import cv2

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
```

---

# 5. Hand Tracking

Use MediaPipe to detect hands.

MediaPipe provides 21 hand landmarks.

Important landmarks:

```text
0  → Wrist

4  → Thumb Tip

8  → Index Finger Tip

12 → Middle Finger Tip

16 → Ring Finger Tip

20 → Pinky Tip
```

The system should track:

* Hand position
* Finger positions
* Hand movement
* Hand direction
* Gesture state
* Movement speed

---

# 6. Gesture Controls

## Open Hand + Swipe

Gesture:

```text
✋ Open Palm + Swipe
```

Action:

```text
Swipe Right
→ Rotate cube view 90° right

Swipe Left
→ Rotate cube view 90° left

Swipe Up
→ Rotate cube view upward

Swipe Down
→ Rotate cube view downward
```

---

## Fist + Movement

Gesture:

```text
✊ Closed Fist
```

Action:

```text
Move Fist Left
→ Orbit camera left

Move Fist Right
→ Orbit camera right

Move Fist Up
→ Orbit camera upward

Move Fist Down
→ Orbit camera downward
```

This movement should be continuous.

---

# 7. Point + Circle

Gesture:

```text
☝️ Point using index finger
```

The user first points toward a cube face.

Then they make a circular movement.

```text
Clockwise Circle
→ Rotate selected face clockwise

Counterclockwise Circle
→ Rotate selected face counterclockwise
```

Track the path of landmark:

```text
Index fingertip = landmark 8
```

Store recent coordinates:

```python
finger_path = [
    (x1, y1),
    (x2, y2),
    (x3, y3)
]
```

Analyze the movement to determine whether the user drew a circle.

---

# 8. Pinch + Drag

Gesture:

```text
🤏 Thumb + Index Finger
```

Calculate the distance between:

```text
Thumb Tip = landmark 4

Index Tip = landmark 8
```

Example:

```python
import math

def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2
    )
```

When the fingers become close:

```text
PINCH_START
```

Track hand movement.

Example:

```text
Pinch + Horizontal Drag
→ Rotate horizontal cube layer

Pinch + Vertical Drag
→ Rotate vertical cube layer
```

When the pinch is released:

```text
PINCH_END
```

The cube should snap to the nearest valid angle:

```text
0°
90°
180°
270°
```

---

# 9. Fast Flick

Detect fast hand movement.

Calculate:

```text
velocity = movement_distance / time
```

If movement velocity exceeds a threshold:

```text
FLICK
```

Action:

```text
Fast Flick Left
→ 180° turn

Fast Flick Right
→ 180° turn
```

---

# 10. Gesture State Machine

Avoid executing gestures every frame.

Use a state machine.

```text
IDLE
 ↓
GESTURE_DETECTED
 ↓
TRACKING
 ↓
GESTURE_CONFIRMED
 ↓
EXECUTE_ACTION
 ↓
COOLDOWN
 ↓
IDLE
```

Example:

```python
if gesture == "Open_Palm":
    gesture_frames += 1

if gesture_frames >= 5:
    state = "TRACKING_SWIPE"
```

After executing an action:

```python
cooldown = 0.4
```

This prevents accidental multiple rotations.

---

# Project Architecture

```text
Laptop Camera
      │
      ▼
    OpenCV
      │
      ▼
   MediaPipe
      │
      ├───────────────┐
      ▼               ▼
Gesture Detection   Hand Landmarks
      │               │
      └───────┬───────┘
              ▼
        Motion Tracker
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
    Swipe   Pinch    Circle
      │       │        │
      └───────┼────────┘
              ▼
      Gesture Controller
              │
              ▼
          Cube Command
              │
       ┌──────┴───────┐
       ▼              ▼
 Cube Controller   Camera Controller
       │              │
       └──────┬───────┘
              ▼
        Pygame/OpenGL
              │
              ▼
        3D Rubik's Cube
```

---

# Project Folder Structure

```text
gesture-rubiks-cube/
│
├── main.py
├── requirements.txt
├── README.md
│
├── cube/
│   ├── __init__.py
│   ├── cube.py
│   ├── cubelet.py
│   ├── renderer.py
│   └── rotations.py
│
├── vision/
│   ├── __init__.py
│   ├── camera.py
│   ├── hand_tracker.py
│   ├── gesture_detector.py
│   └── motion_tracker.py
│
├── controls/
│   ├── __init__.py
│   ├── gesture_controller.py
│   ├── keyboard_controller.py
│   └── mouse_controller.py
│
├── utils/
│   ├── __init__.py
│   ├── geometry.py
│   └── constants.py
│
└── assets/
```

---

# Installation

Create the project:

```bash
mkdir gesture-rubiks-cube
cd gesture-rubiks-cube
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install opencv-python mediapipe numpy pygame PyOpenGL
```

Create:

```text
requirements.txt
```

Example:

```text
opencv-python
mediapipe
numpy
pygame
PyOpenGL
```

---

#
