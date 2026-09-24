I am creating a hand gesture rubiks cube.

Project Structure
gesture-rubiks-cube/
│
├── main.py
├── requirements.txt
│
├── cube/
│   ├── cube.py
│   ├── cubelet.py
│   ├── rotations.py
│   └── renderer.py
│
├── vision/
│   ├── camera.py
│   ├── hand_tracker.py
│   ├── gesture_detector.py
│   └── motion_tracker.py
│
├── controls/
│   ├── gesture_controller.py
│   └── mouse_controller.py
│
├── models/
│   └── gesture_recognizer.task
│
└── utils/
    ├── geometry.py
    └── constants.py