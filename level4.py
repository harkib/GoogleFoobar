from math import sqrt
from fractions import gcd

def reflect_positions(dimensions, your_position, guard_position, distance):
    
    guard_positions_x, your_positions_x = [], []
    guard_positions_xy, your_positions_xy = [], []

    # base dimensions
    x_room, y_room= dimensions[0], dimensions[1]
    x_yours, y_yours = your_position[0], your_position[1]
    x_guard, y_guard = guard_position[0], guard_position[1]

    # mirror distances about walls
    x_mirror_yours = x_room - x_yours
    y_mirror_yours = y_room - y_yours
    x_mirror_guard = x_room - x_guard
    y_mirror_guard = y_room - y_guard

    # reflections needed
    x_reflections = distance/x_room + 1
    y_reflections = distance/y_room + 1

    # reflections about x for base room
    for i in range(-x_reflections, x_reflections + 1): 
        if i%2==0: 
            guard_positions_x.append([x_room*i + x_guard, y_guard])
            your_positions_x.append([x_room*i + x_yours, y_yours])
        else: 
            guard_positions_x.append([x_room*i + x_mirror_guard, y_guard])
            your_positions_x.append([x_room*i + x_mirror_yours, y_yours])

    # reflections about y for each reflections about x
    for i in range(-y_reflections, y_reflections + 1): 
        for base_yours, base_guard in zip (your_positions_x, guard_positions_x):
            x_yours = base_yours[0]
            x_guard = base_guard[0]

            if i%2==0: 
                guard_positions_xy.append([x_guard, y_room*i + y_guard])
                your_positions_xy.append([x_yours, y_room*i + y_yours])
            else: 
                guard_positions_xy.append([x_guard, y_room*i + y_mirror_guard])
                your_positions_xy.append([x_yours, y_room*i + y_mirror_yours])

    return your_positions_xy, guard_positions_xy

def reduce_pair(a,b):
    GCD = abs(gcd(a,b))
    return a/GCD, b/GCD

def solution(dimensions, your_position, guard_position, distance):
    
    # refelct locations about all walls until the reflected area is larger than the gun distance
    your_positions, guard_positions = reflect_positions(dimensions, your_position, guard_position, distance)

    # calculate directions and check distance from base you to reflection of you and all guards
    you2guard, you2you = {}, {}
    x_yours_base = your_position[0]
    y_yours_base = your_position[1]

    # compute directions to shoot yourself and distance
    for your_position in your_positions:

        # compute distance and direction
        x_yours = your_position[0]
        y_yours = your_position[1]
        a = x_yours - x_yours_base
        b = y_yours - y_yours_base
        you2you_dist = sqrt(a**2 + b**2)

        # base you shoot base you
        if you2you_dist == 0: continue

        a , b = reduce_pair(a,b)
        # did you already shoot a closer you
        if (a,b) in you2you: 
            if you2you[a,b] < you2you_dist:
                continue

        # store direction and distance
        you2you[a,b] = you2you_dist

    # compute directions to shoot guards and distance
    for guard_position in guard_positions:

        # compute distance and direction
        x_guard = guard_position[0]
        y_guard = guard_position[1]
        a = x_guard - x_yours_base
        b = y_guard - y_yours_base
        you2guard_dist = sqrt(a**2 + b**2)

        # is guard within range
        if you2guard_dist > distance: continue

        a , b = reduce_pair(a,b)
        # did you already shoot a closer you
        if (a,b) in you2you: 
            if you2you[a,b] < you2guard_dist:
                continue

        you2guard[a,b] = True
        
    return len(you2guard)



assert (solution([3,2], [1,1], [2,1], 4)) == 7
assert (solution([5,2], [1,1], [4,1], 2)) == 0
assert (solution([300,275], [150,150], [185,100], 500)) == 9
print("All tests passed")