from svg_turtle import SvgTurtle
import turtle
import math

# IMPORTANT
# CONFIGURE KEY VALUES HERE
gap_width = 0.027
total_edge_length = 50
num_of_peaks = 4
base_distance = 150
base_width = 45
starting_coor = [-200, 200]
grid = [[True, False, False, False, False, False, False, True],
        [True, True, True, True, True, True, True, True],
        [True, True, True, True, True, True, True, True],
        [True, False, False, False, False, False, False, True],
        [True, False, False, False, False, False, False, True]]

# GLOBALS

# Turtle Set up and configuration (everything is in mm)
#t = SvgTurtle(1280, 800)
t = turtle.Turtle()
t.getscreen().bgcolor("white")
t.width(gap_width)
t.color("black")
t.speed("fastest")
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
    t.left(angle_diagonals)
    if isFirst:
        t.forward(height_diagonals/2)
    else:
        t.forward(height_diagonals)
    t.right(angle_diagonals)
    t.forward(length_short_lines)
    t.right(angle_diagonals)
    if isLast:
        t.forward(height_diagonals/2)
        t.left(angle_diagonals)
        t.forward(length_long_lines)
    else:
        t.forward(height_diagonals)
        t.left(angle_diagonals)

# Function to create one edge of an electrode
def draw_normal_edge():
    # Draw first peak
    draw_peak_new(True, False)
    # Draw the required amount of the middle peaks
    for i in range(num_of_peaks - 2):
        draw_peak_new(False, False)
    # Draw the last peak
    draw_peak_new(False, True)

def draw_attached_base(is_even):
    base_channel_length = length_long_lines if is_even else length_short_lines
    base_short_near_gap_line_length = (base_width - base_channel_length)/2
    t.left(90)
    t.forward(base_distance)
    t.left(90)
    # t.width(15)
    t.forward(base_short_near_gap_line_length)
    for edge in range(3):
        t.right(90)
        t.forward(base_width)
    t.right(90)
    t.forward(base_short_near_gap_line_length)

    t.left(90)

    # Return to the electrode and reset the heading
    t.forward(base_distance)
    t.left(90)

def draw_base_edge():
    # Draw first peak
    draw_peak_new(True, False)

    # Draw the required amount of the middle peaks with the base in the middle
    # If the number of peaks is even
    if num_of_peaks % 2 == 0:
        stop_before_peak = int(num_of_peaks / 2) - 1
        for i in range(stop_before_peak):
            draw_peak_new(False, False)
        # Draw the base
        # Increase pen width for the base
        # t.width(1)
        draw_attached_base(True)
        # Change pen width back to normal
        # t.width(gap_width)
        # Draw the remaining partial peak
        t.left(angle_diagonals)
        t.forward(height_diagonals)
        t.right(angle_diagonals)
        t.forward(length_short_lines)
        t.right(angle_diagonals)
        t.forward(height_diagonals)
        t.left(angle_diagonals)
        # Draw the remaining peaks
        for i in range(int((num_of_peaks - 4)/2)):
            draw_peak_new(False, False)
    # If the number of peaks is odd
    else:
        stop_before_peak = int((num_of_peaks - 1) / 2)
        for i in range(stop_before_peak - 1):
            draw_peak_new(False, False)
        # Draw the first half of the peak
        t.forward(length_long_lines)
        t.left(angle_diagonals)
        t.forward(height_diagonals)
        t.right(angle_diagonals)
        # Draw the base
        # Increase pen width for the base
        # t.width(1)
        draw_attached_base(False)
        # Change pen width back to normal
        # t.width(gap_width)
        # Draw the second half of the peak
        t.right(angle_diagonals)
        t.forward(height_diagonals)
        t.left(angle_diagonals)
        # Draw the remaining peaks
        for i in range(int((num_of_peaks - 3)/2)):
            draw_peak_new(False, False)
    # Draw the last peak
    draw_peak_new(False, True)
    
def draw_electrode(edges_to_ignore, edge_to_attach_base_to):
    for edge in range(4):
        if edge == edge_to_attach_base_to:
            draw_base_edge()
        elif (edge not in edges_to_ignore):
            draw_normal_edge()
        else:
            t.penup()
            draw_normal_edge()
            t.pendown()
        t.right(90)

# Function to check if the current electrode is touching another electrode to its left
def is_adjacent_electrode_to_the_left(x, y):
    if x > 0:
        if grid[y][x-1]:
            return True

# Function to check if the current electrode is touching another electrode above it
def is_adjacent_electrode_upwards(x, y):
    if y > 0:
        if grid[y-1][x]:
            return True
        
# Function to identify which edge to attach the base to
def identify_edge_to_attach_base_to(x, y, edges_to_ignore):
    if x == 0:
        return 3
    elif x == (len(grid[y]) - 1):
        return 1
    elif 0 in edges_to_ignore:
        return 2
    else:
        return 0

def place_and_draw_electrode(x_coor, y_coor):
    # Identify which edges to ignore depending on what other electrodes it is touching (if any)
    edges_to_ignore = []
    if is_adjacent_electrode_to_the_left(x_coor, y_coor):
        edges_to_ignore.append(3)
    if is_adjacent_electrode_upwards(x_coor, y_coor):
        edges_to_ignore.append(0)

    # Move to the correct position
    t.penup()
    t.goto(starting_coor[0], starting_coor[1])
    for i in range(x_coor):
        draw_normal_edge()
    t.right(90)
    for i in range(y_coor):
        draw_normal_edge()
    t.left(90)
    t.pendown()

    # Draw the electrode
    draw_electrode(edges_to_ignore, identify_edge_to_attach_base_to(x_coor, y_coor, edges_to_ignore))

def draw_safety_border_around_bases(first_base, last_base):
    if first_base:
        pass
    elif last_base:
        pass
    else:
        t.width(50)
        for edge in range(4):
            t.forward()
            t.right()

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                place_and_draw_electrode(x, y)

# Run everything
figure_out_specs(total_edge_length, num_of_peaks)
draw_grid()
turtle.done()

# Export to SVG
#t.save_as("NextStageTesting1.svg")