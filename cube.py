import numpy as np

A, B, C = 0.0, 0.0, 0.0  # radian x, y, z
add_A, add_B, add_C = 0.05, 0.05, 0.01

cube_half_width = 10
width, height = 160, 44
distance_from_cam = 60  # cam placed at (0, 0, -distance_from_cam)
focal_length = 40  # for a screen parallel with xy plane
increment_speed = 0.6

background_ASCII_char = "."
z_buffer = np.zeros(width * height)
buffer = np.chararray(width * height, unicode=True)


def show_coordinate_system():
    render_point(0, 0, 0, "0")
    render_point(5, 0, 0, "x")
    render_point(0, 5, 0, "y")
    render_point(-5, -5, 10, "p")
    render_point(-5, -5, -10, "m")


def calculate_rotation(_A, _B, _C):
    rot_x = np.matrix(
        [
            [1, 0, 0],
            [0, np.cos(_A), -np.sin(_A)],
            [0, np.sin(_A), np.cos(_A)],
        ]
    )
    rot_y = np.matrix(
        [
            [np.cos(_B), 0, np.sin(_B)],
            [0, 1, 0],
            [-np.sin(_B), 0, np.cos(_B)],
        ]
    )
    rot_z = np.matrix(
        [
            [np.cos(_C), -np.sin(_C), 0],
            [np.sin(_C), np.cos(_C), 0],
            [0, 0, 1],
        ]
    )
    return np.matmul(rot_z, np.matmul(rot_y, rot_x))


def render_point(_x, _y, _z, _char: str, _rot_matrix: np.matrix = None):
    arr = np.array(
        [
            [_x],
            [_y],
            [_z],
        ]
    )
    if _rot_matrix.all is not None:
        arr = np.matmul(_rot_matrix, arr)
    arr = np.ravel(arr)

    # perspective projection
    recip_dist = 1 / (arr[2] + distance_from_cam)
    # inverse of subject distance
    # larger is closer

    # calculate the screen coordinate
    xp = int(focal_length * recip_dist * arr[0] * 2 + width / 2)  # x2 to match terminal text ratio
    yp = int(focal_length * recip_dist * arr[1] + height / 2)
    idx = xp + yp * width  # screen coordinate to index

    if idx >= 0 & idx < width * height:
        if recip_dist > z_buffer[idx]:  # overwrite with closer ones
            z_buffer[idx] = recip_dist
            buffer[idx] = _char


print(chr(27) + "[2J", end="")  # clear screen
while True:
    # initialize buffer
    z_buffer.fill(0)
    buffer.fill(background_ASCII_char)

    # show_coordinate_system()  # test purpose

    # caclulate current rotation
    rotation = calculate_rotation(A, B, C)

    # render a cube
    cube_x = -cube_half_width
    while cube_x < cube_half_width:
        cube_y = -cube_half_width
        while cube_y < cube_half_width:
            # by checking all 6 surfaces of a cube
            render_point(cube_x, cube_y, -cube_half_width, "#", rotation)
            render_point(cube_half_width, cube_y, cube_x, "$", rotation)
            render_point(-cube_half_width, cube_y, -cube_x, "~", rotation)
            render_point(-cube_x, cube_y, cube_half_width, "#", rotation)
            render_point(cube_x, -cube_half_width, -cube_y, ";", rotation)
            render_point(cube_x, cube_half_width, cube_y, "+", rotation)
            cube_y += increment_speed
        cube_x += increment_speed

    print(chr(27) + "[H", end="")  # move cursor to the top
    for a in range(width * height):  # print the cube
        print(buffer[a] if a % width else "\n", end="")

    A += add_A
    B += add_B
    C += add_C
