import cv2


def list_ports():
    # Test the ports and returns a tuple with the available ports and the ones that are working.
    dev_port = 0
    working_ports = []
    while True:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            print("Port %s is not working." % dev_port)
            break
        else:
            is_reading, img = camera.read()
            w, h = camera.get(3), camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera (%s x %s) is present but does not read." % (dev_port, h, w))
        dev_port += 1
    return working_ports

list_ports()

