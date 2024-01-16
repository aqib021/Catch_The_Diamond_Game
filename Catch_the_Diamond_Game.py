
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluOrtho2D
import random
import sys

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700

class DiamondCatcher:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = 0  # Start at the center
        self.y = -WINDOW_HEIGHT / 2 + self.height / 2  # Adjusted to stay at the bottom

def draw_diamond_catcher(catcher, is_failure):
    if is_failure:
        glColor3f(1.0, 0.0, 0.0)  # Set color to red for the failed catcher
    else:
        glColor3f(0.0, 0.0, 1.0)  # Set color to blue for the successful catcher

    # Draw the trapezium using GL_POINTS
    draw_line(catcher.x - catcher.width / 4, catcher.y, catcher.x + catcher.width / 4, catcher.y)
    draw_line(catcher.x - catcher.width / 2, catcher.y + catcher.height, catcher.x + catcher.width / 2, catcher.y + catcher.height)
    draw_line(catcher.x - catcher.width / 4, catcher.y, catcher.x - catcher.width / 2, catcher.y + catcher.height)
    draw_line(catcher.x + catcher.width / 4, catcher.y, catcher.x + catcher.width / 2, catcher.y + catcher.height)

def draw_line(x1, y1, x2, y2):
    # Midpoint Line Drawing Algorithm
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            glVertex2f(x, y)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            glVertex2f(x, y)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    glVertex2f(x, y)  # Ensure the last point is drawn

class FallingDiamond:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(-200, 200)
        self.y = 400
        self.size = 20
        self.color = [random.uniform(0, 1) for _ in range(3)]
        self.speed = 0.5
        self.fall_speed_increase_threshold = 3
        self.fall_speed_increase_factor = 1.0

def draw_falling_diamond(diamond):
    glColor3f(*diamond.color)  # Set the color
    draw_line(diamond.x, diamond.y + diamond.size, diamond.x + diamond.size, diamond.y)
    draw_line(diamond.x + diamond.size, diamond.y, diamond.x, diamond.y - diamond.size)
    draw_line(diamond.x, diamond.y - diamond.size, diamond.x - diamond.size, diamond.y)
    draw_line(diamond.x - diamond.size, diamond.y, diamond.x, diamond.y + diamond.size)

diamond_catcher = DiamondCatcher(200, 40)  # Adjusted width and height
catcher_speed = 5
falling_diamond = FallingDiamond()
diamonds_caught = 0
game_over = False
catcher_failure = False
score = 0  # New variable to keep track of the score

def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-WINDOW_WIDTH / 2, WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2, WINDOW_HEIGHT / 2)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    global diamond_catcher, catcher_speed, falling_diamond, diamonds_caught, game_over, catcher_failure, score

    glClear(GL_COLOR_BUFFER_BIT)

    if not game_over:
        falling_diamond.y -= falling_diamond.speed

        # Check for collision
        catcher_left = diamond_catcher.x - diamond_catcher.width / 2
        catcher_right = diamond_catcher.x + diamond_catcher.width / 2
        catcher_bottom = diamond_catcher.y
        catcher_top = diamond_catcher.y + diamond_catcher.height

        diamond_left = falling_diamond.x - falling_diamond.size / 2
        diamond_right = falling_diamond.x + falling_diamond.size / 2
        diamond_bottom = falling_diamond.y - falling_diamond.size / 2
        diamond_top = falling_diamond.y + falling_diamond.size / 2

        if (
            catcher_left < diamond_right
            and catcher_right > diamond_left
            and catcher_bottom < diamond_top
            and catcher_top > diamond_bottom
        ):
            diamonds_caught += 1
            score += 1  # Increase score
            falling_diamond.reset()
            catcher_failure = False

            # Increase the speed gradually after a certain number of diamonds
            if diamonds_caught % falling_diamond.fall_speed_increase_threshold == 0:
                falling_diamond.speed *= falling_diamond.fall_speed_increase_factor

        elif falling_diamond.y - falling_diamond.size / 2 < -WINDOW_HEIGHT / 2:
            game_over = True
            catcher_failure = True

    # Clamp the catcher within the window bounds
    diamond_catcher.x = max(-WINDOW_WIDTH / 2 + diamond_catcher.width / 2, min(WINDOW_WIDTH / 2 - diamond_catcher.width / 2, diamond_catcher.x))

    glBegin(GL_POINTS)
    draw_falling_diamond(falling_diamond)
    draw_diamond_catcher(diamond_catcher, catcher_failure)
    glEnd()

    # Display the score
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glRasterPos2f(-WINDOW_WIDTH / 2 + 10, WINDOW_HEIGHT / 2 - 30)
    score_str = f"Score: {score}"
    for char in score_str:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    # Display game over message
    if game_over:
        glColor3f(1.0, 0.0, 0.0)  # Set color to red
        glRasterPos2f(-80, 0)
        game_over_str = "Game Over!"
        for char in game_over_str:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    glutSwapBuffers()

def keyboard_special_keys(key, _, __):
    global diamond_catcher

    if key == GLUT_KEY_LEFT:
        diamond_catcher.x -= catcher_speed
    elif key == GLUT_KEY_RIGHT:
        diamond_catcher.x += catcher_speed

    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b'Catch the Diamonds!')

    glutDisplayFunc(display)
    glutSpecialFunc(keyboard_special_keys)
    glutIdleFunc(display)

    initialize()

    glutMainLoop()

if __name__ == "__main__":
    main()




'''
# Controlling Buttons 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluOrtho2D
import random
import sys

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700

class DiamondCatcher:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = 0  # Start at the center
        self.y = -WINDOW_HEIGHT / 2 + self.height / 2  # Adjusted to stay at the bottom

def draw_diamond_catcher(catcher, is_failure):
    if is_failure:
        glColor3f(1.0, 0.0, 0.0)  # Set color to red for the failed catcher
    else:
        glColor3f(0.0, 0.0, 1.0)  # Set color to blue for the successful catcher

    # Draw the trapezium using GL_POINTS
    draw_line(catcher.x - catcher.width / 4, catcher.y, catcher.x + catcher.width / 4, catcher.y)
    draw_line(catcher.x - catcher.width / 2, catcher.y + catcher.height, catcher.x + catcher.width / 2, catcher.y + catcher.height)
    draw_line(catcher.x - catcher.width / 4, catcher.y, catcher.x - catcher.width / 2, catcher.y + catcher.height)
    draw_line(catcher.x + catcher.width / 4, catcher.y, catcher.x + catcher.width / 2, catcher.y + catcher.height)

def draw_line(x1, y1, x2, y2):
    # Midpoint Line Drawing Algorithm
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            glVertex2f(x, y)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            glVertex2f(x, y)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    glVertex2f(x, y)  # Ensure the last point is drawn

class FallingDiamond:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(-WINDOW_WIDTH / 2, WINDOW_WIDTH / 2)
        self.y = WINDOW_HEIGHT / 2
        self.size = 20
        self.color = [random.uniform(0, 1) for _ in range(3)]
        self.speed = 0.5
        self.fall_speed_increase_threshold = 3
        self.fall_speed_increase_factor = 1.0

def draw_falling_diamond(diamond):
    glColor3f(*diamond.color)  # Set the color
    draw_line(diamond.x, diamond.y + diamond.size, diamond.x + diamond.size, diamond.y)
    draw_line(diamond.x + diamond.size, diamond.y, diamond.x, diamond.y - diamond.size)
    draw_line(diamond.x, diamond.y - diamond.size, diamond.x - diamond.size, diamond.y)
    draw_line(diamond.x - diamond.size, diamond.y, diamond.x, diamond.y + diamond.size)

diamond_catcher = DiamondCatcher(200, 40)  # Adjusted width and height
catcher_speed = 5
falling_diamond = FallingDiamond()
diamonds_caught = 0
game_over = False
catcher_failure = False

# Additional global variables for buttons
next_button_color = [0.0, 1.0, 0.0]  # Green color for 'Next' button
play_pause_button_color = [1.0, 0.5, 0.0]  # Orange color for 'Play/Pause' button
cross_button_color = [1.0, 0.0, 0.0]  # Red color for 'Cross' button

# Additional global variables for buttons
button_size = 20  # Add this line to define button_size globally
button_thickness = 3

# Global variable to track the diamond position
xc = 0
yc = 400
L = 20
color = [random.uniform(0, 1) for _ in range(3)]
speed = 0.5

# Global variables for diamond animation
diamonds_dropped = 0  # Counter for dropped diamonds
fall_speed_increase_threshold = 3  # Number of diamonds to fall before increasing speed
fall_speed_increase_factor = 1.0  # Factor by which to increase speed
falling = True  # Flag to control whether the diamond is falling or not

# Button positions
next_button_position = [button_size, WINDOW_HEIGHT - 2 * button_size]
play_pause_button_position = [WINDOW_WIDTH // 2 - button_size, WINDOW_HEIGHT - 2 * button_size]
cross_button_position = [WINDOW_WIDTH - 2 * button_size, WINDOW_HEIGHT - 2 * button_size]

isPlay = True

def draw_line(x1, y1, x2, y2):
    # Midpoint Line Drawing Algorithm
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x2 - x1 > 0 else -1
    sy = 1 if y2 - y1 > 0 else -1

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(int(dx)):
            glVertex2i(int(x), int(y))
            x += sx
            if p < 0:
                p += 2 * dy
            else:
                p += 2 * (dy - dx)
                y += sy
    else:
        p = 2 * dx - dy
        for _ in range(int(dy)):
            glVertex2i(int(x), int(y))
            y += sy
            if p < 0:
                p += 2 * dx
            else:
                p += 2 * (dx - dy)
                x += sx

def draw_diamond(xc, yc, L, color):
    # Draw four lines to form a diamond using the Midpoint Line Drawing Algorithm
    # Draw four lines to form a diamond
    glColor3f(*color)  # Set the color
    draw_line(xc, yc + L, xc + L, yc)  # Top to right
    draw_line(xc + L, yc, xc, yc - L)  # Right to bottom
    draw_line(xc, yc - L, xc - L, yc)  # Bottom to left
    draw_line(xc - L, yc, xc, yc + L)  # Left to top

def display():
    global diamond_catcher, catcher_speed, falling_diamond, diamonds_caught, game_over, catcher_failure

    glClear(GL_COLOR_BUFFER_BIT)

    if not game_over:
        falling_diamond.y -= falling_diamond.speed

        # Check for collision
        catcher_left = diamond_catcher.x - diamond_catcher.width / 2
        catcher_right = diamond_catcher.x + diamond_catcher.width / 2
        catcher_bottom = diamond_catcher.y
        catcher_top = diamond_catcher.y + diamond_catcher.height

        diamond_left = falling_diamond.x - falling_diamond.size / 2
        diamond_right = falling_diamond.x + falling_diamond.size / 2
        diamond_bottom = falling_diamond.y - falling_diamond.size / 2
        diamond_top = falling_diamond.y + falling_diamond.size / 2

        if (
            catcher_left < diamond_right
            and catcher_right > diamond_left
            and catcher_bottom < diamond_top
            and catcher_top > diamond_bottom
        ):
            diamonds_caught += 1
            falling_diamond.reset()
            catcher_failure = False

            # Increase the speed gradually after a certain number of diamonds
            if diamonds_caught % falling_diamond.fall_speed_increase_threshold == 0:
                falling_diamond.speed *= falling_diamond.fall_speed_increase_factor

        elif falling_diamond.y - falling_diamond.size / 2 < -WINDOW_HEIGHT / 2:
            game_over = True
            catcher_failure = True

    # Clamp the catcher within the window bounds
    diamond_catcher.x = max(-WINDOW_WIDTH / 2 + diamond_catcher.width / 2, min(WINDOW_WIDTH / 2 - diamond_catcher.width / 2, diamond_catcher.x))

    glBegin(GL_POINTS)
    draw_falling_diamond(falling_diamond)
    draw_diamond_catcher(diamond_catcher, catcher_failure)
    glEnd()

    glutSwapBuffers()

def keyboard_special_keys(key, _, __):
    global diamond_catcher

    if key == GLUT_KEY_LEFT:
        diamond_catcher.x -= catcher_speed
    elif key == GLUT_KEY_RIGHT:
        diamond_catcher.x += catcher_speed

    glutPostRedisplay()

def draw_next_button():
    global next_button_color, button_size, button_thickness, next_button_position

    glColor3fv(next_button_color)
    glPointSize(button_thickness)

    glBegin(GL_POINTS)

    for i in range(button_size):
        # Horizontal line
        glVertex2f(next_button_position[0] + i, next_button_position[1])

        # Diagonal lines
        glVertex2f(next_button_position[0] + i, next_button_position[1] - i)
        glVertex2f(next_button_position[0] + i, next_button_position[1] + i)

    glEnd()

    glPointSize(1.0)

def draw_play_pause_button():
    global isPlay, play_pause_button_color, button_size, button_thickness, play_pause_button_position

    glColor3fv(play_pause_button_color)
    glPointSize(button_thickness)

    glBegin(GL_POINTS)

    if isPlay:
        # Draw 'play' symbol (two vertical lines)
        for i in range(20, 41):
            glVertex2f(play_pause_button_position[0] + i, play_pause_button_position[1])
            glVertex2f(play_pause_button_position[0] + i, play_pause_button_position[1] + 20)
    else:
        # Draw 'pause' symbol (triangle) at the center of 'play' symbol
        triangle_size = 25
        play_symbol_position = [play_pause_button_position[0] + 20, play_pause_button_position[1] + 20]

        triangle_position = [play_symbol_position[0] - triangle_size // 2, play_symbol_position[1] - triangle_size // 2]

        for i in range(triangle_size - 1):
            glVertex2f(triangle_position[0] + i, triangle_position[1] - i)
            glVertex2f(triangle_position[0] + i, triangle_position[1] + i)

        glVertex2f(triangle_position[0] + triangle_size - 1, triangle_position[1] - triangle_size + 1)
        glVertex2f(triangle_position[0], triangle_position[1] - triangle_size + 1)

    glEnd()

    glPointSize(1.0)

def draw_cross_button():
    global cross_button_color, button_size, button_thickness, cross_button_position

    glColor3fv(cross_button_color)
    glPointSize(button_thickness)

    glBegin(GL_POINTS)

    for i in range(-button_size, button_size + 1):
        glVertex2f(cross_button_position[0] + i, cross_button_position[1] + i)
        glVertex2f(cross_button_position[0] + i, cross_button_position[1] - i)

    glEnd()

    glPointSize(1.0)

def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

diamonds_caught = 0
game_over = False
catcher_failure = False

def mouse_click(button, state, x, y):
    global isPlay, xc, yc, L, color, speed

    mx, my = x, WINDOW_HEIGHT - y

    # Check if the click is within the 'Next' button
    if (
        next_button_position[0] <= mx <= next_button_position[0] + button_size
        and next_button_position[1] - button_size <= my <= next_button_position[1] + button_size
        and state == GLUT_DOWN
    ):
        # Handle 'Next' button click
        xc = random.uniform(-200, 200)
        yc = 400
        L = 20
        color = [random.uniform(0, 1) for _ in range(3)]
        speed = 0.5

    # Check if the click is within the 'Play/Pause' button
    elif (
        play_pause_button_position[0] - button_size <= mx <= play_pause_button_position[0] + 2*button_size
        and play_pause_button_position[1] - button_size <= my <= play_pause_button_position[1] + button_size
        and state == GLUT_DOWN
    ):
        # Handle 'Play/Pause' button click
        isPlay = not isPlay

    # Check if the click is within the 'Cross' button
    elif (
        cross_button_position[0] - button_size <= mx <= cross_button_position[0] + button_size
        and cross_button_position[1] - button_size <= my <= cross_button_position[1] + button_size
        and state == GLUT_DOWN
    ):
        # Handle 'Cross' button click
        glutLeaveMainLoop()

    glutPostRedisplay()

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_next_button()
    draw_play_pause_button()
    draw_cross_button()

    if isPlay:
        # Incrementally update diamond position for the falling motion
        global yc, speed
        yc -= speed

        glBegin(GL_POINTS)
        draw_diamond(xc, yc, L, color)
        glEnd()

    glutSwapBuffers()

def animation():
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Buttons")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 700)
    glutCreateWindow(b'Diamond Falling from Top')
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard_special_keys)
    glutIdleFunc(display)
    initialize()
    glutMainLoop()

'''







