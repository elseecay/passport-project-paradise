import json
import cv2
from PIL import Image

from pasport_parse import field_recognize as fr


def get_webcam_image():
    camera_device = cv2.VideoCapture(0)
    _, img = camera_device.read()
    return img


def is_passport(img):
    return True


RECOGNIZER = fr.FieldRecognizer()


def recognition(img):
    img = Image.fromarray(img)
    RECOGNIZER.recognize(img)
    return {
        'surname': RECOGNIZER.second_name,
        'name': RECOGNIZER.name,
        'middlename': RECOGNIZER.middle_name,
        'sex': RECOGNIZER.sex,
        'placeofbirth': RECOGNIZER.place_of_birth,
        'birthday': RECOGNIZER.birthday,
        'series': RECOGNIZER.series,
        'number': RECOGNIZER.number
    }


def json_to_mem(mem: memoryview, data):
    data = json.dumps(data).encode('utf8')
    l = len(data)
    mem[:4] = l.to_bytes(4, 'little', signed=False)
    mem[4:4 + l] = data




