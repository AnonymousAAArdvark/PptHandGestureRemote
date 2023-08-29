from math import dist

def dist3d(coord_1, coord_2):
    [x1, y1, z1] = coord_1[3], coord_1[4], coord_1[5]
    [x2, y2, z2] = coord_2[3], coord_2[4], coord_2[5]

    return (((x2-x1)**2)+((y2-y1)**2)+((z2-z1)**2))**(1/2)

def findOrientation(coordinate_landmark_0, coordinate_landmark_9):
    x0 = coordinate_landmark_0[3]
    y0 = coordinate_landmark_0[4]

    x9 = coordinate_landmark_9[3]
    y9 = coordinate_landmark_9[4]

    if abs(x9 - x0) < 0.05:  # since tan(0) --> ∞
        m = 1000000000
    else:
        m = abs((y9 - y0) / (x9 - x0))

    if m >= 0 and m <= 2:
        if x9 > x0:
            return "Right"
        else:
            return "Left"
    if m > 2:
        if y9 < y0:  # since, y decreases upwards
            return "Up"
        else:
            return "Down"

def fingerClosed(base_node, knuckle_node, joint_node, tip_node):
    knuckle_dist = dist3d(knuckle_node, base_node)
    joint_dist = dist3d(joint_node, base_node)
    tip_dist = dist3d(tip_node, base_node)
    return tip_dist < knuckle_dist and tip_dist < joint_dist

def inPointingGesture(lmList):
    middle_finger_closed = fingerClosed(lmList[0], lmList[9], lmList[11], lmList[12])
    ring_finger_closed = fingerClosed(lmList[0], lmList[13], lmList[15], lmList[16])
    pinky_finger_closed = fingerClosed(lmList[0], lmList[17], lmList[19], lmList[20])
    if middle_finger_closed and ring_finger_closed and pinky_finger_closed:
        print("all closed!")
    else:
        print(middle_finger_closed, ring_finger_closed, pinky_finger_closed)

    return [middle_finger_closed, ring_finger_closed, pinky_finger_closed]
