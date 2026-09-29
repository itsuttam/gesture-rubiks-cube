class GestureController:
    def __init__(
        self,
        cube,
        camera_controller
    ):
        self.cube = cube

        self.camera = camera_controller

        # Gesture rotations affect this face
        self.selected_face = "F"

        self.pinch_has_rotated = False

        self.pinch_threshold = 0.12

        self.last_action = "None"

    
    # SELECT FACE
    

    def set_selected_face(
        self,
        face
    ):
        face = face.upper()

        if face in (
            "R",
            "L",
            "U",
            "D",
            "F",
            "B"
        ):
            self.selected_face = face

            self.last_action = (
                f"Selected face: {face}"
            )

    
    # HANDLE GESTURE
    

    def handle(
        self,
        event
    ):

        if event is None:
            return None

        
        # FIST MOVEMENT
        

        if event.name == "ORBIT":

            self.camera.gesture_orbit(
                event.dx,
                event.dy
            )

            self.last_action = (
                f"Orbit {event.direction}"
            )

            return self.last_action

        
        # OPEN HAND SWIPE
        

        if event.name == "SWIPE":

            self.camera.rotate_view(
                event.direction
            )

            self.last_action = (
                f"View {event.direction}"
            )

            return self.last_action

        
        # POINT + CIRCLE
        

        if event.name == "CIRCLE":

            if (
                event.direction
                == "CLOCKWISE"
            ):
                angle = 90

            else:
                angle = -90

            self.cube.rotate_face(
                self.selected_face,
                angle
            )

            self.last_action = (
                f"{self.selected_face} "
                f"{event.direction}"
            )

            print(self.last_action)

            return self.last_action

        
        # FAST FLICK
        

        if event.name == "FLICK":

            self.cube.rotate_face(
                self.selected_face,
                180
            )

            self.last_action = (
                f"{self.selected_face} 180°"
            )

            print(self.last_action)

            return self.last_action

        
        # PINCH START
        

        if event.name == "PINCH_START":

            self.pinch_has_rotated = False

            self.last_action = (
                "Pinch started"
            )

            return self.last_action

        
        # PINCH DRAG
        

        if event.name == "PINCH_DRAG":

            if self.pinch_has_rotated:
                return None

            dx = event.dx
            dy = event.dy

            movement = max(
                abs(dx),
                abs(dy)
            )

            if movement < self.pinch_threshold:
                return None

            # Determine rotation direction
            if abs(dx) > abs(dy):

                if dx > 0:
                    angle = 90
                else:
                    angle = -90

            else:

                if dy > 0:
                    angle = 90
                else:
                    angle = -90

            self.cube.rotate_face(
                self.selected_face,
                angle
            )

            self.pinch_has_rotated = True

            self.last_action = (
                f"Pinch rotate "
                f"{self.selected_face} "
                f"{angle}°"
            )

            print(self.last_action)

            return self.last_action

        
        # PINCH END
        

        if event.name == "PINCH_END":

            self.pinch_has_rotated = False

            self.last_action = (
                "Pinch released"
            )

            return self.last_action

        return None