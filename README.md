GestureCube Setup Guide
Overview
GestureCube is a gesture-controlled 3D Rubik's Cube project built with Python, OpenCV, MediaPipe, Pygame, PyOpenGL, and NumPy.
The application uses a laptop webcam to detect hand gestures and control a virtual Rubik's Cube rendered on top of the live camera feed.
This guide explains how to set up the project from scratch on Windows.
Requirements
Before starting, make sure you have:
Windows 10 or Windows 11
Python 3.10 or newer
A working laptop webcam or external webcam
VS Code or another code editor
Git, if you want version control
Internet access for installing Python packages
Recommended Python Version
Python 3.11 or Python 3.12 is a good choice for this project.
Check your Python version:
```powershell
python --version
```
Example:
```text
Python 3.12.0
```
If `python` is not recognized, install Python and make sure the option to add Python to PATH is enabled during installation.
Project Folder
Create the project folder:
```powershell
mkdir gesture-rubiks-cube
cd gesture-rubiks-cube
```
Recommended structure:
```text
gesture-rubiks-cube/
│
├── main.py
├── requirements.txt
│
├── models/
│   └── gesture_recognizer.task
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
│   ├── camera_background.py
│   ├── hand_tracker.py
│   └── gesture_detector.py
│
└── controls/
    ├── __init__.py
    ├── keyboard_controller.py
    ├── mouse_controller.py
    └── gesture_controller.py
```
Create a Virtual Environment
Create the virtual environment:
```powershell
python -m venv .venv
```
Activate it:
```powershell
.venv\Scripts\activate
```
After activation, your terminal should show something similar to:
```text
(.venv) PS C:\Users\YourName\gesture-rubiks-cube>
```
Upgrade pip
Upgrade pip before installing packages:
```powershell
python -m pip install --upgrade pip
```
requirements.txt
Create a file named:
```text
requirements.txt
```
Add:
```txt
opencv-python
mediapipe
numpy
pygame
PyOpenGL
```
Install all packages:
```powershell
pip install -r requirements.txt
```
Verify the Installation
Run:
```powershell
python -c "import cv2, mediapipe, numpy, pygame, OpenGL; print('All packages installed successfully!')"
```
Expected result:
```text
All packages installed successfully!
```
MediaPipe Gesture Model
Create a folder:
```text
models/
```
Place the MediaPipe gesture recognition model inside it:
```text
models/gesture_recognizer.task
```
Your project should contain:
```text
gesture-rubiks-cube/
└── models/
    └── gesture_recognizer.task
```
The application expects this exact model path unless you change it in the code.
Test the Webcam
Before testing the full project, confirm that OpenCV can access the laptop camera.
Create a temporary file:
```text
camera_test.py
```
Add:
```python
import cv2

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        print("Camera not detected")
        break

    cv2.imshow(
        "Camera Test",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
```
Run:
```powershell
python camera_test.py
```
Press `Q` to close the camera window.
If camera index `0` does not work, try:
```python
cv2.VideoCapture(1)
```
Camera Permissions
If the webcam does not open, check Windows camera permissions.
Go to:
```text
Settings
    ↓
Privacy and security
    ↓
Camera
```
Make sure camera access is enabled for desktop applications.
Also close any application that may already be using the webcam, such as:
```text
Microsoft Teams
Zoom
Discord
Browser camera tabs
Windows Camera
```
OpenGL Setup
GestureCube currently uses fixed-function OpenGL commands such as:
```text
glBegin
glEnd
glMatrixMode
glTranslatef
glRotatef
```
Request an OpenGL 2.1 context before creating the Pygame window.
Example:
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
    (
        window_width,
        window_height
    ),
    pygame.DOUBLEBUF
    | pygame.OPENGL
    | pygame.NOFRAME
)
```
The OpenGL attributes must be set before `pygame.display.set_mode()`.
Display Setup
To make the application fill the monitor, detect the screen size:
```python
display_info = pygame.display.Info()

window_width = display_info.current_w
window_height = display_info.current_h
```
Then create a borderless full-screen style window:
```python
pygame.display.set_mode(
    (
        window_width,
        window_height
    ),
    pygame.DOUBLEBUF
    | pygame.OPENGL
    | pygame.NOFRAME
)
```
Using `NOFRAME` is useful because it fills the monitor without relying on exclusive fullscreen mode.
Camera Resolution
Start with:
```python
camera = Camera(
    camera_index=0,
    width=640,
    height=480
)
```
If performance is good and the webcam supports it, increase to:
```python
camera = Camera(
    camera_index=0,
    width=1280,
    height=720
)
```
A 1280 x 720 camera feed usually looks better on a 16:9 monitor.
Important Initialization Order
Create components in this order:
```text
pygame.init()
    ↓
Set OpenGL attributes
    ↓
Create Pygame OpenGL window
    ↓
Setup OpenGL
    ↓
Create CameraBackground
    ↓
Create Cube and Renderer
    ↓
Create Controllers
    ↓
Create Camera
    ↓
Create MediaPipe HandTracker
    ↓
Start main loop
```
Do not create `CameraBackground()` before the OpenGL window exists.
Incorrect:
```python
camera_background = CameraBackground()

pygame.display.set_mode(...)
```
Correct:
```python
pygame.display.set_mode(...)

camera_background = CameraBackground()
```
Run the Project
From the project root:
```powershell
python main.py
```
Example:
```text
(.venv) PS C:\Users\Acer\gesture-rubiks-cube> python main.py
```
If everything is configured correctly, you should see:
```text
Camera + MediaPipe enabled
```
The application should open with:
Live camera background
3D Rubik's Cube
Hand landmarks
Current gesture
Selected cube face
Current action
FPS information
Keyboard Controls
Use these controls to test the cube:
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
Shift + Face -> Counterclockwise turn
Ctrl + Face  -> 180 degree turn
S            -> Scramble cube
Space        -> Reset cube
Esc          -> Exit application
```
Mouse Controls
```text
Left Mouse Drag -> Orbit camera
Mouse Wheel     -> Zoom in or out
```
Gesture Controls
Current planned controls:
```text
Open Palm + Swipe -> Rotate view
Closed Fist + Move -> Orbit camera
Point + Circle -> Rotate selected face
Pinch + Drag -> Rotate selected face or layer
Fast Flick -> 180 degree turn
```
Recommended Testing Order
Do not test everything at once.
Use this order:
```text
1. Test Python environment
2. Test package imports
3. Test webcam
4. Test Rubik's Cube logic
5. Test OpenGL rendering
6. Test keyboard controls
7. Test mouse controls
8. Test MediaPipe landmarks
9. Test built-in gestures
10. Test custom gestures
11. Test camera background
12. Test full integration
```
This makes debugging much easier.
Common Setup Problems
Python is not recognized
Check:
```powershell
python --version
```
If Python is missing, reinstall Python and enable the PATH option.
Virtual environment does not activate
Try:
```powershell
.venv\Scripts\activate
```
If PowerShell blocks scripts, you may need to allow local script execution according to your Windows security settings.
Module not found
Example:
```text
ModuleNotFoundError: No module named 'cv2'
```
Make sure the virtual environment is active, then run:
```powershell
pip install -r requirements.txt
```
Camera does not open
Try:
```python
camera_index=1
```
Also close applications that may already be using the camera.
Gesture model not found
Check that this file exists:
```text
models/gesture_recognizer.task
```
Black screen
Check that:
```text
The OpenGL window is created only once
CameraBackground is created after the OpenGL context
The camera is actually returning frames
The camera texture is updated every frame
```
OpenGL error at glBegin
Make sure the OpenGL 2.1 context is requested before creating the Pygame window.
Git Setup
Initialize Git:
```powershell
git init
```
Create a `.gitignore` file:
```gitignore
.venv/
__pycache__/
*.pyc
.vscode/
.idea/
```
Then:
```powershell
git add .
git commit -m "Initial GestureCube setup"
```
If a GitHub repository already exists:
```powershell
git remote add origin YOUR_REPOSITORY_URL
git branch -M main
git push -u origin main
```
Suggested Development Setup
Recommended:
```text
Operating System: Windows
Editor: VS Code
Python: 3.11 or 3.12
Camera: Laptop Webcam
Environment: Python virtual environment
Version Control: Git
Repository: GitHub
```
For this project, native Windows Python is recommended because webcam and OpenGL access are simpler than running the main application inside WSL.
Final Checklist
Before running `main.py`, confirm:
- Python is installed
- Virtual environment is activated
- requirements.txt packages are installed
- Webcam works with OpenCV
- Camera permission is enabled
- `gesture_recognizer.task` exists
- Cube files exist
- Vision files exist
- Control files exist
- OpenGL window is created only once
- CameraBackground is created after the OpenGL window
- `main.py` runs from the project root
When all items are complete, run:
```powershell
python main.py
```
The GestureCube development environment is now ready.