import math

def toVec(coord_1, coord_2):
    return [coord_2[i] - coord_1[i] for i in range(3, 6)]

def mag3d(vec):
    return math.sqrt(sum(v ** 2 for v in vec))

def dot3d(vec_1, vec_2):
    return sum(v1 * v2 for v1, v2 in zip(vec_1, vec_2))

def cosVec(vec_1, vec_2):
    return dot3d(vec_1, vec_2) / (mag3d(vec_1) * mag3d(vec_2))

def dist3d(coord_1, coord_2):
    x1, y1, z1 = coord_1[3:6]
    x2, y2, z2 = coord_2[3:6]

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5

def findOrientation(coordinate_landmark_0, coordinate_landmark_9):
    # Finds orientation of hand through finding 2d slope between base node and middle finger knuckle node
    x0, y0 = coordinate_landmark_0[3:5]
    x9, y9 = coordinate_landmark_9[3:5]

    xd = x9 - x0
    yd = y9 - y0

    # Note: "Left" and "Right" are swapped due to camera mirroring
    if xd > 0 and -2 <= yd / xd <= -.05:
        return "Right"
    if xd < 0 and .05 <= yd / xd <= 2:
        return "Left"
    return "None"

def fingerClosed(base_node, knuckle_node, joint_node, tip_node):
    # Detects closed finger if the tip of a finger is closer to the base node than both the joint and knuckle

    knuckle_dist = dist3d(knuckle_node, base_node)
    joint_dist = dist3d(joint_node, base_node)
    tip_dist = dist3d(tip_node, base_node)
    return tip_dist < knuckle_dist * 1.2 and tip_dist < joint_dist

def thumbPointerExtended(node_2, node_3, node_5, node_6, node_7, node_8):
    # Detects 90-degree angle between extended thumb and pointer
    # node 2: thumb knuckle, node 3: thumb joint, node 5 - 8: knuckle, 2 joints, and fingertip

    # Determines if the thumb is facing the right orientation
    vec23 = toVec(node_2, node_3)
    if vec23[1] / abs(vec23[0]) > -.5:
        return False

    vec56 = toVec(node_5, node_6)
    vec67 = toVec(node_6, node_7)
    vec78 = toVec(node_7, node_8)

    # Determines if the pointer is straight enough, and if the pointer and thumb vectors are orthogonal enough
    return cosVec(vec56, vec67) > .95 and cosVec(vec67, vec78) > .95 and cosVec(vec23, vec56) < .85

def inPointingGesture(lmList):
    # Combines all detections above to get the complete gesture detection, returns the direction of the gesture

    # Iterates through the middle, ring, and pinky fingers and determines if they are closed
    closed_fingers = [fingerClosed(lmList[0], lmList[i], lmList[i + 2], lmList[i + 3]) for i in [9, 13, 17]]

    thumb_extended = thumbPointerExtended(lmList[2], lmList[3], lmList[5], lmList[6], lmList[7], lmList[8])

    if all(closed_fingers) and thumb_extended:
        return findOrientation(lmList[0], lmList[9])

    return "None"