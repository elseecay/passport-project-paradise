import json
import cv2


def get_webcam_image():
    camera_device = cv2.VideoCapture(0)
    _, img = camera_device.read()
    return img


def is_passport(img):
    return True


def recognition(img):
    return {'data': 1}


def json_to_mem(mem: memoryview, data):
    data = json.dumps(data).encode('utf8')
    l = len(data)
    mem[:4] = l.to_bytes(4, 'little', signed=False)
    mem[4:4 + l] = data




