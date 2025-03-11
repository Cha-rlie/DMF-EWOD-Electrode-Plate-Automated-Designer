from svg_turtle import SvgTurtle
import turtle
import math

# IMPORTANT
# CONFIGURE KEY VALUES HERE
gap_width = 0.027
total_edge_length = 50
num_of_peaks = 4
node_channel_width_fraction = 0.3 # Percentage of electrode edge length
channel_straight = False
channel_length = 150
channel_end_length = 10
node_width = 65
starting_coor = [-200, 100]
grid = [[True, False, False, False, False, False, False, True],
        [True, True, True, True, True, True, True, True],
        [True, True, True, True, True, True, True, True],
        [True, False, False, False, False, False, False, True],
        [True, False, False, False, False, False, False, True]]

# GLOBALS
nodes_counter = [-1, -1, -1, -1]

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
    global angle_half_diagonals
    global first_peak_length
    global last_peak_length
    global num_of_nodes_needed_on_each_side
    global max_design_size
    global node_width
    num_long_lines = num_of_peaks + 1
    num_short_lines = num_of_peaks
    num_of_diagonals = num_of_peaks * 2
    length_long_lines = total_edge_length / (2.4*num_of_peaks + 0.6)
    length_short_lines = length_long_lines * 0.6
    length_diagonals = length_long_lines * 0.4
    height_diagonals = total_edge_length * 0.2
    angle_diagonals = math.degrees(math.atan(height_diagonals / length_diagonals))

    # Calculate the length of the first and last peak
    first_peak_length = length_long_lines + length_diagonals/2 + length_short_lines + length_diagonals
    last_peak_length = length_long_lines + length_diagonals + length_short_lines + length_diagonals/2 + length_long_lines

    # Calculate the number of nodes needed on each side of the electrode plate
    num_of_nodes_needed_on_each_side = count_number_of_nodes_needed_on_each_side()
    
    # Calculate the maximum size of the electrode plate design based on the provided grid
    max_design_size = []
    max_design_size.append(len(grid[0]) * total_edge_length)
    max_design_size.append(len(grid) * total_edge_length)
    
    # If the channels are to be straight, automatically derive the width of the nodes to make sure they fit next to each other
    if channel_straight:
        node_width = round(total_edge_length * 0.9)

def draw_peak(isFirst, isLast):
    # TODO: FIX THE LENGTH MATH TO DEAL WITH THIS AND MAKE IT FASTER
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
    draw_peak(True, False)
    # Draw the required amount of the middle peaks
    for i in range(num_of_peaks - 2):
        draw_peak(False, False)
    # Draw the last peak
    draw_peak(False, True)

def draw_channel(side_node_is_being_drawn_on, going_up_node, x_coor, y_coor):
    # Check if the channel is straight and if so draw it and return
    if channel_straight:
        t.forward(channel_length)
        return

    # FIX X BEING EQUAL TO THE AMOUNT OF NODE NOT GLOBAL COORDINATE
    nodes_counter[side_node_is_being_drawn_on] += 0.5
    # Check if the number of nodes that need to be drawn on this side is even or odd
    is_num_of_nodes_even = num_of_nodes_needed_on_each_side[side_node_is_being_drawn_on] % 2 == 0
    # Calculate the number of spacing units necessary
    spacing_units_necessary = (num_of_nodes_needed_on_each_side[side_node_is_being_drawn_on] - (0 if is_num_of_nodes_even else 1)) / 2
    # Calcualte the minimum channel length to clear other nearby electrodes
    relevant_coor = y_coor if side_node_is_being_drawn_on in [0, 2] else x_coor
    min_channel_length = round(total_edge_length/2) if side_node_is_being_drawn_on in [1, 3] else ((relevant_coor * total_edge_length + 5) if side_node_is_being_drawn_on == 0 else ((len(grid) - relevant_coor - 1) * total_edge_length + 5))
    
    node_coor = math.ceil(nodes_counter[side_node_is_being_drawn_on])
    distance_from_middle = (node_coor-spacing_units_necessary+1) if ((is_num_of_nodes_even) and ((node_coor-spacing_units_necessary) >= 0)) else (node_coor-spacing_units_necessary)
    inverted_distance_from_middle = 1 + spacing_units_necessary - abs(distance_from_middle)
    # Calculate a value between 0 and 0.5 using the distance between the node and the middle
    distance_from_middle_normalised = (abs(inverted_distance_from_middle) / (spacing_units_necessary)*(0.5))
    # Calculate the length of the first part of the channel
    calc_channel_length = min_channel_length + (node_width+15)*(inverted_distance_from_middle-0.5) + round(node_width/2)

    # Determine which way to turn
    if distance_from_middle == 0:
        rotation = 0
    elif distance_from_middle < 0:
        rotation = 90 if side_node_is_being_drawn_on in [0, 1] else -90
    else:
        rotation = -90 if side_node_is_being_drawn_on in [0, 1] else 90

    # Move sideways if drawing the channel back from the node to the electrode
    if distance_from_middle != 0 and not going_up_node:
        t.forward(channel_end_length + round(node_channel_width_fraction*total_edge_length)) if ((distance_from_middle < 0 and side_node_is_being_drawn_on in [0, 1]) or (distance_from_middle > 0 and side_node_is_being_drawn_on in [2,3])) else t.forward(channel_end_length)
        t.left(rotation*-1)

    # Move forward the right amount
    if distance_from_middle == 0:
        t.forward(calc_channel_length - round(node_width/3))
    elif (distance_from_middle < 0 and side_node_is_being_drawn_on in [0, 1]) or (distance_from_middle > 0 and side_node_is_being_drawn_on in [2,3]):
        # Draw the first part of the channel
        t.forward(calc_channel_length - round(node_channel_width_fraction*total_edge_length)) if going_up_node else t.forward(calc_channel_length)
    else:
        # Draw the first part of the channel
        t.forward(calc_channel_length) if going_up_node else t.forward(calc_channel_length - round(node_channel_width_fraction*total_edge_length))            

    # Move sideways an appropriate amount
    if distance_from_middle != 0 and going_up_node:
        t.left(rotation)
        t.forward(channel_end_length) if ((distance_from_middle < 0 and side_node_is_being_drawn_on in [0, 1]) or (distance_from_middle > 0 and side_node_is_being_drawn_on in [2,3])) else t.forward(channel_end_length + round(node_channel_width_fraction*total_edge_length))

def draw_attached_node(side_being_draw_on, x, y):
    # TODO: MAKE THIS THICKER
    # Calculate the length of the spacers that are not part of the channel
    base_short_near_gap_line_length = (node_width - node_channel_width_fraction*total_edge_length)/2
    
    t.left(90)

    # Draw the channel up to the node
    draw_channel(side_being_draw_on, True, x, y)

    # Draw the node
    t.left(90)
    t.forward(base_short_near_gap_line_length)
    for edge in range(3):
        t.right(90)
        t.forward(node_width)
    t.right(90)
    t.forward(base_short_near_gap_line_length)

    t.left(90)

    # Draw the channel back from the node
    draw_channel(side_being_draw_on, False, x, y)
    # Return to the electrode and reset the heading
    t.left(90)

    # TODO: MAKE THIS THIN AGAIN
    # t.width(gap_width)

def draw_node_edge(side_edge_is_on, x, y):
    # Draw first peak
    draw_peak(True, False)
    t.forward(length_long_lines)
    # Sandwhich the channel to the connecting node between evenly spaced lines and calculate the sandwhiching lengths
    spacing_line_length = (total_edge_length - total_edge_length * node_channel_width_fraction - first_peak_length - last_peak_length - length_long_lines) / 2
    # Draw the first spacing line
    t.forward(spacing_line_length)
    # Draw the entire channel and the conencting node
    draw_attached_node(side_edge_is_on, x, y)
    # Draw the second spacing line
    t.forward(spacing_line_length)
    # Draw the last peak
    draw_peak(False, True)
    
def draw_electrode(edges_to_ignore, edge_to_attach_base_to, x, y):
    for edge in range(4):
        if edge == edge_to_attach_base_to:
            draw_node_edge(edge, x, y)
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
        
# Function to identify which edges to ignore depending on what other electrodes it is touching (if any)
def identify_edges_to_ignore(x_coor, y_coor):
    edges_to_ignore = []
    if is_adjacent_electrode_to_the_left(x_coor, y_coor):
        edges_to_ignore.append(3)
    if is_adjacent_electrode_upwards(x_coor, y_coor):
        edges_to_ignore.append(0)
    return edges_to_ignore

# Function to identify which edge to attach the node to
def identify_edge_to_attach_node_to(x, y, edges_to_ignore):
    if x == 0:
        return 3
    elif x == (len(grid[y]) - 1):
        return 1
    elif 0 in edges_to_ignore:
        return 2
    else:
        return 0

# Function to count the number of nodes needed on each side of the grid
def count_number_of_nodes_needed_on_each_side():
    nodes_needed_on_each_side = [0, 0, 0, 0]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                nodes_needed_on_each_side[identify_edge_to_attach_node_to(x, y, identify_edges_to_ignore(x, y))] += 1
    return nodes_needed_on_each_side

def place_and_draw_electrode(x_coor, y_coor):
    # Identify the edge to ignore when drawing the electrode
    edges_to_ignore = identify_edges_to_ignore(x_coor, y_coor)

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
    draw_electrode(edges_to_ignore, identify_edge_to_attach_node_to(x_coor, y_coor, edges_to_ignore), x_coor, y_coor)

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
# t.save_as("Test_Results/NextStageTesting1.svg")