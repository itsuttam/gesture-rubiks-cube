GestureCube Problems and Solutions
Overview
This document records the main problems that can happen while building GestureCube, why they happen, and how they can be solved.
The project combines several systems:
```text
Python
OpenCV
MediaPipe
Pygame
PyOpenGL
Laptop Camera
Gesture Recognition
3D Rubik's Cube Logic
```
Because all of these systems work together, a problem in one part can affect the whole application.
The best way to debug the project is to test each part separately before combining everything.
1. Camera Does Not Open
Problem
The program starts but the webcam does not show anything.
Possible error:
```text
Could not open camera 0
```
Why It Happens
Possible reasons:
```text
Wrong camera index
Another application is using the camera
Windows camera permission is disabled
Camera driver problem
Running inside WSL instead of Windows
```
Solution
Start with:
```python
camera = cv2.VideoCapture(0)
```
If camera `0` does not work, try:
```python
camera = cv2.VideoCapture(1)
```
Close applications that may already be using the webcam, such as:
```text
Teams
Zoom
Discord
Browser camera tabs
Windows Camera
```
Also check:
```text
Windows Settings
    ↓
Privacy and security
    ↓
Camera
    ↓
Allow desktop apps to access your camera
```
For this project, running Python directly on Windows is easier than using WSL for webcam access.
2. Camera Works but the Screen Is Black
Problem
The application opens, but only a black screen is visible.
Why It Happens
This can happen when the OpenGL window is created incorrectly.
One problem we encountered was creating the display more than once.
Bad structure:
```python
pygame.display.set_mode(...)

def main():
    pygame.display.set_mode(...)
```
The second call can recreate the OpenGL context and invalidate resources created earlier.
Another possible issue is creating `CameraBackground()` before the OpenGL context exists.
Bad:
```python
camera_background = CameraBackground()

pygame.display.set_mode(...)
```
Solution
Create the Pygame OpenGL window only once.
Correct order:
```text
pygame.init()
    ↓
pygame.display.set_mode()
    ↓
setup_opengl()
    ↓
CameraBackground()
    ↓
Camera
    ↓
Main loop
```
Example:
```python
pygame.init()

pygame.display.set_mode(
    (window_width, window_height),
    pygame.DOUBLEBUF
    | pygame.OPENGL
    | pygame.NOFRAME
)

setup_opengl(
    window_width,
    window_height
)

camera_background = CameraBackground()
```
3. `glBegin(GL_QUADS)` Crashes
Problem
Example error:
```text
renderer.py
glBegin(GL_QUADS)
```
The program crashes while drawing the cube.
Why It Happens
The renderer uses older fixed-function OpenGL commands such as:
```text
glBegin
glEnd
glMatrixMode
glPushMatrix
glTranslatef
```
These commands require a compatible OpenGL context.
Solution
Request an OpenGL 2.1 context before creating the window.
```python
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
```
Then create the window:
```python
pygame.display.set_mode(
    (window_width, window_height),
    pygame.DOUBLEBUF
    | pygame.OPENGL
)
```
The OpenGL attributes must be set before `pygame.display.set_mode()`.
4. MediaPipe Shows `NORM_RECT` Warning
Problem
Example:
```text
Using NORM_RECT without IMAGE_DIMENSIONS is only supported for the square ROI.
Provide IMAGE_DIMENSIONS or use PROJECTION_MATRIX.
```
Why It Happens
This warning comes from MediaPipe's internal landmark projection system.
It does not necessarily mean that hand tracking has failed.
Solution
If hand landmarks and gestures are still detected correctly, the warning can be ignored during development.
Focus on actual runtime errors first.
The important question is:
```text
Does the hand tracker still return landmarks?
```
If yes, this warning is not currently blocking the project.
5. MediaPipe Says Custom Gesture Classifier Is Not Defined
Problem
Example:
```text
Custom gesture classifier is not defined.
```
Why It Happens
The project uses MediaPipe's built-in gesture recognizer.
A custom gesture classifier has not been added.
Solution
No fix is required for the current version.
Built-in gestures such as these can still work:
```text
Open_Palm
Closed_Fist
Pointing_Up
Thumb_Up
Thumb_Down
Victory
```
A custom model can be added later if needed.
6. Gesture Model File Is Missing
Problem
Example:
```text
Gesture model not found
```
Why It Happens
The file:
```text
models/gesture_recognizer.task
```
is missing or the path is wrong.
Solution
The project should contain:
```text
gesture-rubiks-cube/
│
├── main.py
│
└── models/
    └── gesture_recognizer.task
```
Build the path using:
```python
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
```
This is safer than depending on the current terminal folder.
7. Camera Does Not Fill the Screen
Problem
The camera works, but only part of the monitor is used.
Why It Happens
The application may use a fixed window size such as:
```python
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
```
That creates only a 1000 by 800 window.
Solution
Read the actual monitor size:
```python
display_info = pygame.display.Info()

window_width = display_info.current_w
window_height = display_info.current_h
```
Then create a full-size window.
```python
pygame.display.set_mode(
    (window_width, window_height),
    pygame.DOUBLEBUF
    | pygame.OPENGL
    | pygame.NOFRAME
)
```
`NOFRAME` provides a borderless full-screen style without using exclusive fullscreen mode.
8. Fullscreen Causes a Black Screen
Problem
The application works in windowed mode but becomes black when using:
```python
pygame.FULLSCREEN
```
Why It Happens
Exclusive fullscreen can behave differently depending on:
```text
GPU
Display driver
Monitor resolution
OpenGL context
Windows display settings
```
Solution
Use borderless fullscreen instead:
```python
pygame.display.set_mode(
    (window_width, window_height),
    pygame.DOUBLEBUF
    | pygame.OPENGL
    | pygame.NOFRAME
)
```
This still fills the monitor but is usually easier to work with.
9. Camera Image Looks Stretched
Problem
The camera fills the whole screen but faces or objects look too wide or too tall.
Why It Happens
The camera aspect ratio and monitor aspect ratio may be different.
Example:
```text
Camera: 640 x 480
Aspect ratio: 4:3

Screen: 1920 x 1080
Aspect ratio: 16:9
```
Stretching a 4:3 image across a 16:9 screen changes its shape.
Solution
Prefer a camera resolution that matches the screen aspect ratio.
Example:
```python
camera = Camera(
    camera_index=0,
    width=1280,
    height=720
)
```
Both 1280 x 720 and 1920 x 1080 use a 16:9 aspect ratio.
A future improvement can crop the camera image instead of stretching it.
10. Camera Looks Blurry
Problem
The camera fills the screen but looks low quality.
Why It Happens
A small frame such as:
```text
640 x 480
```
is being enlarged to a large display.
Solution
Try:
```python
camera = Camera(
    camera_index=0,
    width=1280,
    height=720
)
```
If the laptop camera supports 720p, this gives better quality.
Do not assume the requested resolution is always supported. Some webcams may return a different resolution.
11. Camera Texture Is Upside Down
Problem
The webcam image appears vertically flipped.
Why It Happens
OpenCV and OpenGL use different coordinate directions for image textures.
Solution
Before uploading the image to OpenGL:
```python
rgb = cv2.flip(
    rgb,
    0
)
```
This flips the image vertically.
12. Camera Is Not Mirrored
Problem
Moving the right hand appears like moving the left side of the image.
Why It Happens
A normal webcam frame behaves like another person is looking at you, not like a mirror.
Solution
Mirror the camera frame:
```python
frame = cv2.flip(
    frame,
    1
)
```
This makes interaction more natural.
13. Cube Appears in the Center
Problem
The cube blocks the user because it is rendered in the middle of the screen.
Why It Happens
The camera transform uses:
```python
glTranslatef(
    0,
    0,
    -distance
)
```
The first value is the horizontal position.
Solution
Move the cube to the right:
```python
self.position_x = 2.7
```
Then:
```python
glTranslatef(
    self.position_x,
    self.position_y,
    -self.distance
)
```
Example values:
```text
1.5 -> slightly right
2.5 -> right
2.7 -> good starting point
3.5 -> near right edge
```
14. Cube Goes Outside the Screen
Problem
After moving the cube to the right, part of it disappears.
Why It Happens
The cube's 3D position is too far from the camera's visible area.
Solution
Reduce:
```python
self.position_x
```
For example:
```python
self.position_x = 2.2
```
Another option is to move the camera slightly farther away:
```python
self.distance = 12.0
```
Test position and distance together.
15. Open Palm Is Detected but Swipe Does Not Work
Problem
MediaPipe recognizes:
```text
Open_Palm
```
but no swipe action happens.
Why It Happens
Possible reasons:
```text
Movement distance is below threshold
Movement is too slow
Gesture history is too short
Hand temporarily leaves the frame
Detection confidence changes during movement
```
Solution
Check the swipe threshold.
Example:
```python
if distance < 0.18:
    return None
```
For testing, reduce it slightly:
```python
if distance < 0.12:
    return None
```
Do not reduce it too much because small hand movement could trigger false swipes.
16. Pinch Is Hard to Detect
Problem
Thumb and index finger touch, but the system does not always detect the pinch.
Why It Happens
Using a fixed distance can fail when the hand moves closer or farther from the camera.
Solution
Normalize the pinch distance using hand size.
```python
normalized_distance = (
    pinch_distance
    /
    hand_size
)
```
Then check:
```python
return normalized_distance < 0.35
```
The exact threshold should be calibrated using the actual webcam.
17. One Pinch Rotates the Cube Multiple Times
Problem
A single pinch can produce output such as:
```text
Pinch rotate F 90°
Pinch rotate F -90°
```
Why It Happens
`PINCH_DRAG` is generated continuously while the fingers remain pinched.
Without a state lock, the same pinch can trigger another rotation.
Solution
Use a flag:
```python
self.pinch_has_rotated = False
```
When the pinch starts:
```python
if event.name == "PINCH_START":
    self.pinch_has_rotated = False
```
Before rotating:
```python
if self.pinch_has_rotated:
    return None
```
After rotation:
```python
self.pinch_has_rotated = True
```
When the pinch ends:
```python
if event.name == "PINCH_END":
    self.pinch_has_rotated = False
```
The desired behavior is:
```text
Pinch
    ↓
Drag
    ↓
One rotation
    ↓
Keep holding
    ↓
No more rotation
    ↓
Release
    ↓
Ready for next pinch
```
18. Gesture Direction Suddenly Reverses
Problem
A gesture starts in one direction but is later interpreted in the opposite direction.
Why It Happens
The gesture system may continue measuring movement after the action has already happened.
Small hand movements can change the final `dx` or `dy`.
Solution
Once a gesture is confirmed:
```text
Execute action
Clear movement history
Start cooldown
```
Example:
```python
self.palm_history.clear()
self.trigger()
```
For pinch, lock the action until release.
19. Gestures Trigger Too Often
Problem
One swipe or circle causes several actions.
Why It Happens
The camera processes many frames every second.
At 30 FPS, the same gesture can exist in many frames.
Solution
Use a cooldown:
```python
self.cooldown = 0.40
```
Check:
```python
if self.can_trigger():
    self.trigger()
```
The state should behave like:
```text
Gesture detected
    ↓
Execute once
    ↓
Cooldown
    ↓
Ready again
```
20. Gesture Detection Feels Unstable
Problem
The displayed gesture quickly changes between:
```text
Open_Palm
None
Open_Palm
None
Closed_Fist
```
Why It Happens
Real-time recognition confidence changes from frame to frame.
Lighting, hand angle, motion blur, and distance can affect detection.
Solution
Require the same gesture for several frames before accepting it.
Example idea:
```text
Open_Palm
Open_Palm
Open_Palm
Open_Palm
Open_Palm
    ↓
Confirmed Open Palm
```
A future version should implement gesture smoothing.
21. Circle Gesture Is Difficult to Trigger
Problem
The index finger moves in a circle but no `CIRCLE` event is detected.
Why It Happens
Circle detection depends on:
```text
Path size
Path duration
Start and end distance
Aspect ratio
Total rotation angle
```
Solution
Display or print index fingertip coordinates during testing.
Then tune:
```python
width < 0.07
height < 0.07
abs(total_angle) < 5.0
```
A circle should not need to be mathematically perfect.
The goal is to recognize a natural human circular motion.
22. Wrong Face Rotates
Problem
The user gestures near one face but another face rotates.
Why It Happens
The current version does not yet detect which 3D face the finger is pointing at.
It uses:
```python
self.selected_face = "F"
```
or the last face selected with the keyboard.
Solution
For the current version, select the face using:
```text
R
L
U
D
F
B
```
A future version should implement 3D face picking:
```text
Index fingertip position
    ↓
Convert screen point to 3D ray
    ↓
Check cube face intersection
    ↓
Highlight face
    ↓
Select face
```
23. Cube Rotation Happens Instantly
Problem
A face jumps directly from one position to another.
Why It Happens
The cube state is updated immediately by:
```python
cube.rotate_face(
    face,
    90
)
```
There is no animation system yet.
Solution
This is acceptable for the first version.
Later, add:
```text
Start rotation
    ↓
Animate 0° to 90°
    ↓
Finish rotation
    ↓
Update logical cube state
```
This will make the cube feel much more realistic.
24. Low FPS
Problem
The camera or cube movement feels slow.
Why It Happens
Possible causes:
```text
High webcam resolution
MediaPipe inference
Uploading a new OpenGL texture every frame
Drawing too much debug information
Running multiple camera windows
```
Solution
Test with:
```python
width=640
height=480
```
If performance is good, increase to:
```python
width=1280
height=720
```
Also make sure there is only one webcam capture and one application window.
25. Two Camera Objects Are Created
Problem
The camera may fail, freeze, or behave inconsistently.
Why It Happens
A camera was previously created globally:
```python
camera = Camera(...)
```
and then another one was created inside:
```python
def main():
    camera = Camera(...)
```
Two objects can attempt to access the same webcam.
Solution
Create the camera only once inside `main()`.
Correct:
```python
def main():
    camera = Camera(
        camera_index=0,
        width=1280,
        height=720
    )
```
Do not create a second camera at the top of the file.
26. Text Does Not Appear on Camera Background
Problem
OpenCV text is created but is not visible in the OpenGL window.
Why It Happens
The frame was uploaded to OpenGL before drawing the text.
Wrong order:
```python
camera_background.update(
    frame
)

cv2.putText(
    frame,
    ...
)
```
Solution
Draw everything first:
```python
hand_tracker.draw_landmarks(
    frame,
    hands
)

cv2.putText(
    frame,
    ...
)
```
Then upload the final image:
```python
camera_background.update(
    frame
)
```
Correct flow:
```text
Camera frame
    ↓
Hand landmarks
    ↓
UI text
    ↓
OpenGL texture
    ↓
Display
```
27. Keyboard Works but Gestures Do Not
Problem
Cube rotations work using keyboard controls but gesture controls do nothing.
Why It Happens
This usually means the cube system is working and the problem is in the vision pipeline.
Debugging Steps
Check each stage separately:
```text
1. Does the camera open?
2. Are hand landmarks visible?
3. Is hand.gesture changing?
4. Does GestureDetector return an event?
5. Does GestureController receive the event?
6. Does cube.rotate_face() run?
```
Print values during testing:
```python
print(
    hand.gesture
)
```
Then:
```python
print(
    gesture_event
)
```
This helps identify exactly where the data stops.
28. How to Debug the Project Properly
Do not debug the whole project at once.
Use this order:
```text
Step 1
Test Rubik's Cube logic

Step 2
Test OpenGL rendering

Step 3
Test keyboard controls

Step 4
Test mouse controls

Step 5
Test webcam

Step 6
Test MediaPipe landmarks

Step 7
Test built-in gestures

Step 8
Test custom gesture detection

Step 9
Connect gestures to cube

Step 10
Add camera background
```
If a new feature breaks the project, test the last feature that was added.
29. Useful Debug Output
During development, useful console output includes:
```text
Camera + MediaPipe enabled
Gesture: Open_Palm
Gesture: Closed_Fist
Swipe RIGHT
Pinch started
Pinch rotate F 90°
Pinch released
Circle CLOCKWISE
```
Avoid printing every hand landmark every frame because the console will become difficult to read.
30. Current Known Limitations
The current project still has some limitations.
```text
Face selection is mostly keyboard based
Cube does not yet follow the hand
Pinch rotation is not physically attached to a layer
Circle detection needs calibration
Gesture thresholds may differ between cameras
Cube rotations are not animated
Two-hand gestures are not implemented yet
```
These are normal development limitations, not failures.
They can be improved one feature at a time.
Problem Solving Summary
The main problems and solutions are:
Problem	Main Solution
Camera not detected	Check camera index and permissions
Black screen	Create OpenGL window only once
OpenGL crash	Use compatible OpenGL context
Camera not full width	Use monitor dimensions
Fullscreen black screen	Use borderless `NOFRAME`
Camera stretched	Match camera and screen aspect ratio
Camera blurry	Use higher supported camera resolution
Cube in center	Change cube X position
Cube outside screen	Reduce X position or increase distance
Pinch repeats	Lock rotation until pinch release
Swipe repeats	Add cooldown
Gesture unstable	Add frame smoothing
Wrong face rotates	Use selected face until ray picking is added
UI text missing	Draw text before texture upload
Low FPS	Reduce camera resolution and duplicate work
Model missing	Add `gesture_recognizer.task`
MediaPipe warnings	Separate warnings from real runtime errors
Final Debugging Rule
Always find which system is failing before changing code.
Use this mental model:
```text
Camera problem?
    ↓
Test OpenCV

Hand problem?
    ↓
Test MediaPipe

Gesture problem?
    ↓
Test GestureDetector

Cube problem?
    ↓
Test keyboard controls

Rendering problem?
    ↓
Test OpenGL

Integration problem?
    ↓
Check main.py
```
This makes debugging much faster than changing several files at the same time.