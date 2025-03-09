from svg_turtle import SvgTurtle
import turtle
import math

# IMPORTANT
# CONFIGURE KEY VALUES HERE
total_edge_length = 250
num_of_peaks = 4
starting_coor = [-300, 300]

# GLOBALS
multiplier = 1

# Turtle Set up and configuration (everything is in mm)
#t = SvgTurtle(200, 200)
t = turtle.Turtle()
t.getscreen().bgcolor("white")
t.width = 0.05
t.speed(100)
t.penup()
t.goto(starting_coor[0], starting_coor[1])
t.pendown()
# starts facing right

# Function to figure out the lengths of the lines and diagonals
def figure_out_specs(total_edge_length, num_of_peaks):
    global num_long_lines
    global num_short_lines
    global num_of_diagonals
    global length_long_lines
    global length_short_lines
    global length_diagonals
    global height_diagonals
    global angle_diagonals
    num_long_lines = num_of_peaks + 1
    num_short_lines = num_of_peaks
    num_of_diagonals = num_of_peaks * 2
    length_long_lines = total_edge_length / (2.4*num_of_peaks + 0.6)
    length_short_lines = length_long_lines * 0.6
    length_diagonals = length_long_lines * 0.4
    height_diagonals = total_edge_length * 0.2
    angle_diagonals = math.degrees(math.atan(height_diagonals / length_diagonals))

def draw_peak_old(isFirst, isLast):
    t.forward(length_long_lines)
    t.left(angle_diagonals)
    if isFirst or isLast:
        t.forward(height_diagonals/2)
    else:
        t.forward(height_diagonals)
    t.right(angle_diagonals)
    t.forward(length_short_lines)
    if not isLast:
        t.right(angle_diagonals)
        t.forward(height_diagonals)
        t.left(angle_diagonals)

def draw_peak_new(isFirst, isLast):
    t.forward(length_long_lines)
    t.left(angle_diagonals*multiplier)
    if isFirst:
        t.forward(height_diagonals/2)
    else:
        t.forward(height_diagonals)
    t.right(angle_diagonals*multiplier)
    t.forward(length_short_lines)
    t.right(angle_diagonals*multiplier)
    if isLast:
        t.forward(height_diagonals/2)
        t.left(angle_diagonals*multiplier)
        t.forward(length_long_lines)
    else:
        t.forward(height_diagonals)
        t.left(angle_diagonals*multiplier)

# Function to create one edge of an electrode
def draw_normal_edge(is_mirrored):
    global multiplier
    if is_mirrored == True:
        multiplier = -1
    else:
        multiplier = 1
    # Draw first peak
    draw_peak_new(True, False)
    # Draw the required amount of the middle peaks
    for i in range(num_of_peaks - 2):
        draw_peak_new(False, False)
    # Draw the last peak
    draw_peak_new(False, True)

def draw_electrode():
    for edge in range(4):
        if (edge == 2 or edge == 3):
            draw_normal_edge(False)
        else:
            draw_normal_edge(True)
        t.right(90)

def place_and_draw_electrode():#x_distance_in_electrodes, y_distance_in_electrodes):
    for electrode in range(4):
        draw_electrode()
        t.penup()
        t.forward(total_edge_length)
        t.pendown()

def draw_grid():
    pass

# Run everything
figure_out_specs(total_edge_length, num_of_peaks)
place_and_draw_electrode()
turtle.done()


# Export to SVG
# t.save_as("test.")