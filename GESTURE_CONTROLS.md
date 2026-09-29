GestureCube Hand Control Documentation
Overview
GestureCube is a gesture-controlled Rubik's Cube simulator built with Python, OpenCV, MediaPipe, Pygame, and PyOpenGL.
The goal is to make the cube feel natural to control. Instead of depending only on a keyboard or mouse, the user can use hand gestures in front of the laptop camera to rotate the cube, move the view, select faces, turn layers, and perform other actions.
The camera remains visible in the background while the 3D Rubik's Cube is rendered on top of the camera feed.
Main Interaction Idea
The hand is used as the main controller.
The basic flow is:
```text
Laptop Camera
    ↓
OpenCV captures the frame
    ↓
MediaPipe detects the hand
    ↓
GestureDetector identifies the gesture
    ↓
GestureController converts it into an action
    ↓
Rubik's Cube or camera view responds
```
Current Hand Gestures
Open Palm and Swipe
Gesture:
```text
✋ Open Palm + Swipe
```
Purpose:
Rotate the cube view by 90 degrees.
Actions:
```text
Swipe Right  -> Rotate view 90° right
Swipe Left   -> Rotate view 90° left
Swipe Up     -> Rotate view upward
Swipe Down   -> Rotate view downward
```
This gesture changes how the cube is viewed. It does not turn a Rubik's Cube face.
Closed Fist and Movement
Gesture:
```text
✊ Closed Fist + Move Hand
```
Purpose:
Orbit the camera around the cube.
Actions:
```text
Move Left   -> Orbit left
Move Right  -> Orbit right
Move Up     -> Orbit upward
Move Down   -> Orbit downward
```
Unlike a swipe, this action is continuous. The cube view follows the movement of the fist.
Point and Circle
Gesture:
```text
☝️ Point + Draw a Circle
```
Purpose:
Rotate the currently selected face.
Actions:
```text
Clockwise circle        -> Rotate selected face 90° clockwise
Counterclockwise circle -> Rotate selected face 90° counterclockwise
```
The system tracks the index fingertip and stores its recent movement path. It then checks whether the movement looks like a circular path.
Pinch and Drag
Gesture:
```text
🤏 Pinch + Drag
```
Purpose:
Turn a cube face or layer.
The pinch starts when the thumb tip and index fingertip move close together.
Actions:
```text
Pinch Start
    ↓
Drag hand
    ↓
Detect drag direction
    ↓
Rotate selected face
    ↓
Release pinch
```
Example:
```text
Pinch + Drag Right -> Rotate selected face 90°
Pinch + Drag Left  -> Rotate selected face -90°
```
Only one rotation should happen during a single pinch. The user must release the pinch before another pinch rotation can begin.
Fast Flick
Gesture:
```text
⚡ Fast Hand Flick
```
Purpose:
Perform a 180 degree turn.
Action:
```text
Fast Flick -> Rotate selected face 180°
```
The system detects this by measuring how quickly the hand moves over a short period of time.
Face Selection
The cube currently uses a selected face.
Possible faces are:
```text
F -> Front
B -> Back
R -> Right
L -> Left
U -> Up
D -> Down
```
The selected face is used by gestures such as:
```text
Point + Circle
Pinch + Drag
Fast Flick
```
For example, if the selected face is `F`:
```text
Pinch + Drag Right
    ↓
Front face rotates 90°
```
Keyboard Support
Keyboard controls are useful for testing the Rubik's Cube logic before testing gestures.
```text
R -> Rotate right face
L -> Rotate left face
U -> Rotate upper face
D -> Rotate lower face
F -> Rotate front face
B -> Rotate back face
```
Additional controls:
```text
Shift + Face -> Counterclockwise rotation
Ctrl + Face  -> 180° rotation
S            -> Scramble cube
Space        -> Reset cube
Esc          -> Exit application
```
Pressing a face key also changes the selected face.
Mouse Support
Mouse controls are useful when testing without a camera.
```text
Left Mouse Drag -> Orbit camera
Mouse Wheel     -> Zoom in or out
```
Mouse mode should remain available even when gesture control is enabled.
Planned Hand Controls
The current gesture system can be extended with more natural interactions.
Point at a Face
Instead of selecting a face using the keyboard, the user should be able to point directly at a visible cube face.
Example:
```text
Point at right face
    ↓
Right face becomes highlighted
    ↓
Right face becomes selected
```
This will require converting the 2D fingertip position into a ray and checking which 3D face the ray intersects.
Grab the Whole Cube
Gesture:
```text
🤌 Pinch and Hold
```
Purpose:
Pick up and move the entire virtual cube.
Example:
```text
Pinch cube
    ↓
Move hand
    ↓
Cube follows hand
```
Cube Following the Palm
The cube can be positioned using the detected palm location.
Example:
```text
Open Palm
    ↓
Detect palm center
    ↓
Move 3D cube toward palm position
```
This can create the effect of holding a virtual Rubik's Cube in the hand.
Two Hand Zoom
Gesture:
```text
✋        ✋
```
Move hands apart:
```text
Cube becomes larger
```
Move hands together:
```text
Cube becomes smaller
```
This is similar to pinch-to-zoom on a touchscreen.
Wrist Rotation
The system can estimate hand orientation from MediaPipe landmarks.
Possible action:
```text
Rotate wrist
    ↓
Rotate whole cube
```
This could make camera control feel more natural than using a fist.
Thumbs Up
Gesture:
```text
👍
```
Possible use:
```text
Confirm current action
Select highlighted face
Resume gesture mode
```
Thumbs Down
Gesture:
```text
👎
```
Possible use:
```text
Cancel current action
Undo latest operation
```
Two Fingers
Gesture:
```text
✌️
```
Possible use:
```text
Undo previous cube move
```
Open Palm Hold
Gesture:
```text
✋ Hold for 2 seconds
```
Possible use:
```text
Reset cube
```
A hold timer should be used so an ordinary open palm does not reset the cube accidentally.
Two Open Hands
Gesture:
```text
✋   ✋
```
Possible use:
```text
Scramble cube
```
A short hold period should be required before the scramble begins.
Pause Gesture Mode
Gesture:
```text
✊ Hold Fist
```
Possible use:
```text
Pause gesture input
```
Then:
```text
✋ Open Palm
```
could resume gesture input.
This helps prevent accidental movements while the user is repositioning their hand.
Recommended Final Gesture Layout
A practical final control system could use:
Gesture	Action
Open palm + swipe	Rotate cube view
Closed fist + move	Orbit camera
Point at face	Select face
Point + circle	Turn selected face
Pinch + drag	Turn selected layer
Fast flick	180° turn
Two fingers	Undo
Thumbs up	Confirm
Thumbs down	Cancel
Open palm hold	Reset
Two open hands	Scramble
Two hands apart or together	Resize cube
Wrist rotation	Rotate whole cube
Gesture Detection Rules
Gesture recognition should not respond immediately to every frame.
A state system should be used.
```text
IDLE
  ↓
GESTURE_DETECTED
  ↓
TRACKING
  ↓
GESTURE_CONFIRMED
  ↓
EXECUTE
  ↓
COOLDOWN
  ↓
IDLE
```
This prevents accidental repeated actions.
For example:
```text
Pinch detected
    ↓
Start tracking drag
    ↓
Movement passes threshold
    ↓
Rotate one face
    ↓
Wait for pinch release
```
The cube should not rotate again until the pinch ends.
Gesture Cooldown
Some gestures should have a short cooldown.
Example:
```text
Swipe detected
    ↓
Rotate view
    ↓
Wait 0.4 seconds
    ↓
Allow another swipe
```
This prevents one movement from being recognized multiple times.
Hand Size Normalization
Distances measured by MediaPipe change depending on how close the hand is to the camera.
A fixed value such as:
```python
distance < 0.05
```
may work at one distance but fail at another.
A better approach is:
```text
thumb-index distance
--------------------
hand size
```
This produces a normalized measurement and makes pinch detection more reliable.
Camera Layout
The camera should fill the application window.
The 3D cube can be placed on the right side so the user's hand and face remain visible.
Example:
```text
+------------------------------------------------------+
| Gesture: Open_Palm                                  |
| Selected: F                                         |
|                                                     |
|          Camera View                  Rubik's Cube  |
|                                       +---------+   |
|               User                    |         |   |
|               Hand                    |  Cube   |   |
|                                       |         |   |
|                                       +---------+   |
|                                                     |
+------------------------------------------------------+
```
Later, the fixed cube position can be replaced by palm tracking.
User Interface Information
The camera view can display:
```text
Gesture: Open_Palm
Selected: F
Action: View RIGHT
FPS: 30
```
Useful future information:
```text
Hand: Right
Confidence: 0.94
Pinch: Active
Mode: Gesture
Moves: 18
Timer: 00:42
```
Project Components
The project is separated into clear modules.
```text
gesture-rubiks-cube/
│
├── main.py
│
├── requirements.txt
│
├── models/
│   └── gesture_recognizer.task
│
├── cube/
│   ├── cube.py
│   ├── cubelet.py
│   ├── renderer.py
│   └── rotations.py
│
├── vision/
│   ├── camera.py
│   ├── camera_background.py
│   ├── hand_tracker.py
│   └── gesture_detector.py
│
└── controls/
    ├── keyboard_controller.py
    ├── mouse_controller.py
    └── gesture_controller.py
```
Responsibility of Each File
`camera.py`
Handles the laptop webcam.
Responsibilities:
```text
Open camera
Read frames
Mirror frames
Calculate FPS
Release camera
```
`hand_tracker.py`
Handles MediaPipe.
Responsibilities:
```text
Detect hand
Read 21 hand landmarks
Recognize built-in gestures
Detect left or right hand
Draw hand skeleton
```
`gesture_detector.py`
Handles movement-based gesture logic.
Responsibilities:
```text
Detect pinch
Detect swipe
Detect flick
Detect circle
Track palm movement
Track index fingertip movement
Apply cooldown
```
`gesture_controller.py`
Connects detected gestures to actions.
Example:
```text
SWIPE RIGHT
    ↓
GestureController
    ↓
Camera.rotate_view("RIGHT")
```
Another example:
```text
CIRCLE CLOCKWISE
    ↓
GestureController
    ↓
Cube.rotate_face("F", 90)
```
`camera_background.py`
Converts the OpenCV camera frame into an OpenGL texture.
This allows the camera and 3D cube to appear in the same window.
`renderer.py`
Draws the 3D Rubik's Cube using OpenGL.
`cube.py`
Stores the Rubik's Cube state and performs legal cube rotations.
Development Priorities
The next improvements should be completed in this order:
Make every current gesture stable.
Prevent repeated pinch rotations.
Add visual face highlighting.
Allow pointing to select a face.
Make the cube follow the palm.
Add two-hand resizing.
Add undo and redo.
Add gesture calibration.
Add smooth cube rotation animations.
Add a Rubik's Cube solver.
Final Goal
The final experience should feel like interacting with a real object.
A user should be able to stand in front of the laptop camera, point at the virtual Rubik's Cube, grab or select a face, move their hands naturally, and see the cube respond immediately.
The long-term interaction can look like:
```text
User points at cube face
    ↓
Face highlights
    ↓
User pinches
    ↓
User drags hand
    ↓
Selected layer follows movement
    ↓
User releases pinch
    ↓
Layer snaps to 90°
```
This creates a more natural human-computer interaction experience than controlling the cube only with keyboard commands.