from typing import Tuple


Vector3 = Tuple[int, int, int]


def rotate_vector_90(
    vector: Vector3,
    axis: str,
    direction: int
) -> Vector3:
    """
    Rotate a vector by 90 degrees.

    Parameters
    ----------
    vector:
        (x, y, z)

    axis:
        "x", "y", or "z"

    direction:
         1 = +90 degrees
        -1 = -90 degrees

    Returns
    -------
    Rotated (x, y, z) tuple.
    """

    if direction not in (-1, 1):
        raise ValueError(
            "direction must be 1 or -1"
        )

    axis = axis.lower()

    x, y, z = vector

    
    # X AXIS
    

    if axis == "x":

        if direction == 1:
            return (
                x,
                -z,
                y
            )

        return (
            x,
            z,
            -y
        )

    
    # Y AXIS
    

    if axis == "y":

        if direction == 1:
            return (
                z,
                y,
                -x
            )

        return (
            -z,
            y,
            x
        )

    
    # Z AXIS
    

    if axis == "z":

        if direction == 1:
            return (
                -y,
                x,
                z
            )

        return (
            y,
            -x,
            z
        )

    raise ValueError(
        "axis must be 'x', 'y', or 'z'"
    )


def rotate_vector(
    vector: Vector3,
    axis: str,
    angle: int
) -> Vector3:
    """
    Rotate a vector by:

        90
        -90
        180
        -180

    Example:

        rotate_vector(
            (1, 1, 0),
            "x",
            90
        )
    """

    if angle not in (
        90,
        -90,
        180,
        -180
    ):
        raise ValueError(
            "angle must be 90, -90, 180, or -180"
        )

    direction = 1

    if angle < 0:
        direction = -1

    turns = abs(angle) // 90

    result = vector

    for _ in range(turns):

        result = rotate_vector_90(
            result,
            axis,
            direction
        )

    return result


def rotate_cubelet(
    cubelet,
    axis: str,
    direction: int
):
    """
    Rotate both:

    1. cubelet position
    2. cubelet sticker directions
    """

    cubelet.position = rotate_vector_90(
        cubelet.position,
        axis,
        direction
    )

    new_stickers = {}

    for direction_vector, color in cubelet.stickers.items():

        rotated_direction = rotate_vector_90(
            direction_vector,
            axis,
            direction
        )

        new_stickers[
            rotated_direction
        ] = color

    cubelet.stickers = new_stickers