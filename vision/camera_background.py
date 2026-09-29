import cv2

from OpenGL.GL import (
    glGenTextures,
    glBindTexture,
    glTexImage2D,
    glTexParameteri,
    glEnable,
    glDisable,
    glBegin,
    glEnd,
    glTexCoord2f,
    glVertex2f,
    glColor3f,
    glMatrixMode,
    glPushMatrix,
    glPopMatrix,
    glLoadIdentity,
    glDepthMask,
    GL_TEXTURE_2D,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_LINEAR,
    GL_RGB,
    GL_UNSIGNED_BYTE,
    GL_QUADS,
    GL_PROJECTION,
    GL_MODELVIEW,
)


class CameraBackground:

    def __init__(self):

        self.texture = glGenTextures(1)

        glBindTexture(
            GL_TEXTURE_2D,
            self.texture
        )

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MIN_FILTER,
            GL_LINEAR
        )

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MAG_FILTER,
            GL_LINEAR
        )

    def update(self, frame):
        """
        Upload OpenCV camera frame
        into an OpenGL texture.
        """

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # OpenCV and OpenGL have different
        # vertical coordinate directions
        rgb = cv2.flip(
            rgb,
            0
        )

        height, width = rgb.shape[:2]

        glBindTexture(
            GL_TEXTURE_2D,
            self.texture
        )

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            rgb
        )

    def draw(self):
        """
        Draw camera texture across
        the whole screen.
        """

        # Do not let background modify depth
        glDepthMask(False)

        
        # ORTHOGRAPHIC PROJECTION
        

        glMatrixMode(
            GL_PROJECTION
        )

        glPushMatrix()

        glLoadIdentity()

        
        # MODEL VIEW
        

        glMatrixMode(
            GL_MODELVIEW
        )

        glPushMatrix()

        glLoadIdentity()

        glEnable(
            GL_TEXTURE_2D
        )

        glBindTexture(
            GL_TEXTURE_2D,
            self.texture
        )

        # Prevent cube colors affecting texture
        glColor3f(
            1.0,
            1.0,
            1.0
        )

        glBegin(
            GL_QUADS
        )

        # Bottom-left
        glTexCoord2f(
            0.0,
            0.0
        )

        glVertex2f(
            -1.0,
            -1.0
        )

        # Bottom-right
        glTexCoord2f(
            1.0,
            0.0
        )

        glVertex2f(
            1.0,
            -1.0
        )

        # Top-right
        glTexCoord2f(
            1.0,
            1.0
        )

        glVertex2f(
            1.0,
            1.0
        )

        # Top-left
        glTexCoord2f(
            0.0,
            1.0
        )

        glVertex2f(
            -1.0,
            1.0
        )

        glEnd()

        glDisable(
            GL_TEXTURE_2D
        )

        
        # RESTORE MATRICES
        

        glPopMatrix()

        glMatrixMode(
            GL_PROJECTION
        )

        glPopMatrix()

        glMatrixMode(
            GL_MODELVIEW
        )

        glDepthMask(True)