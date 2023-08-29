import math
from math import dist

def toVec(coord_1, coord_2):
    return [coord_2[3] - coord_1[3], coord_2[4] - coord_1[4], (coord_2[5] - coord_1[5])]
def mag3d(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)

def cosVec(vec_1, vec_2):
    return dot3d(vec_1, vec_2) / (mag3d(vec_1) * mag3d(vec_2))

def dot3d(vec_1, vec_2):
    [x1, y1, z1] = vec_1[0], vec_1[1], vec_1[2]
    [x2, y2, z2] = vec_2[0], vec_2[1], vec_2[2]

    return x1 * x2 + y1 * y2 + z1 * z2
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

def thumbPointerExtended(node_2, node_3, node_5, node_6, node_7, node_8):
    vec23 = toVec(node_2, node_3)
    if vec23[1] / abs(vec23[0]) > -.7:
        return [False, False, False]

    vec56 = toVec(node_5, node_6)
    vec67 = toVec(node_6, node_7)
    vec78 = toVec(node_7, node_8)

    return [cosVec(vec56, vec67) > .9 and cosVec(vec67, vec78) > .9 and cosVec(vec23, vec56) < .85,
            cosVec(vec56, vec67) > .9 and cosVec(vec67, vec78) > .9, cosVec(vec23, vec56) < .85]

def inPointingGesture(lmList):
    middle_finger_closed = fingerClosed(lmList[0], lmList[9], lmList[11], lmList[12])
    ring_finger_closed = fingerClosed(lmList[0], lmList[13], lmList[15], lmList[16])
    pinky_finger_closed = fingerClosed(lmList[0], lmList[17], lmList[19], lmList[20])
    extended, pointer, thumb = False, False, False
    if middle_finger_closed and ring_finger_closed and pinky_finger_closed:
        # print("all closed!")
        extended, pointer, thumb = thumbPointerExtended(lmList[2], lmList[3], lmList[5], lmList[6], lmList[7], lmList[8])
    else:
        extended, pointer, thumb = thumbPointerExtended(lmList[2], lmList[3], lmList[5], lmList[6], lmList[7], lmList[8])
        # print(middle_finger_closed, ring_finger_closed, pinky_finger_closed)

    # thumbPointerExtended(lmList[2], lmList[3], lmList[5], lmList[6], lmList[7], lmList[8])

    return [middle_finger_closed, ring_finger_closed, pinky_finger_closed, extended, pointer, thumb]
