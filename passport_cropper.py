import face_recognition
from PIL import Image


def crop_passport(path):
    image = face_recognition.load_image_file(path)
    face = face_recognition.face_locations(image)[0]

    width = abs(face[3] - face[1])
    height = abs(face[2] - face[0])

    coors = {
        "x0": min(face[3], face[1]),
        "y0": min(face[0], face[2]),
        "x1": max(face[3], face[1]),
        "y1": max(face[0], face[2]),
    }

    start_x = coors["x1"]
    start_y = coors["y0"]
    end_x = coors["x1"]
    end_y = coors["y1"]

    start_y -= int(height * 1.8)
    end_y += int(height)

    end_x += width * 6

    img = image[start_y:end_y, start_x:end_x]
    img = Image.fromarray(img, 'RGB')

    return img
