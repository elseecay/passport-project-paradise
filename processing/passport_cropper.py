# import passport_cropper as pc
#
# pc.crop_passport_down("photo.jpg").save("cropped_photo.jpg", "JPEG", quality=100)
# pc.crop_passport_down("photo.jpg").show()
#
import face_recognition
from PIL import Image


def find_face(path):
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

    return coors, width, height, image


def crop_passport(image, start_x, start_y, end_x, end_y):
    img = image[start_y:end_y, start_x:end_x]
    img = Image.fromarray(img, 'RGB')

    return img


def crop_passport_up(path):
    coors, width, height, image = find_face(path)

    start_x = coors["x0"]
    start_y = coors["y0"]
    end_x = coors["x1"]
    end_y = coors["y0"]

    start_y -= int(height * 6)
    start_y = max(start_y, 0)
    end_y -= int(height * 3.5)

    end_x += width * 6

    return crop_passport(image, start_x, start_y, end_x, end_y)


def crop_passport_down(path):
    coors, width, height, image = find_face(path)

    start_x = coors["x1"]
    start_y = coors["y0"]
    end_x = coors["x1"]
    end_y = coors["y1"]

    start_y -= int(height * 1.8)
    end_y += int(height)

    end_x += width * 6

    return crop_passport(image, start_x, start_y, end_x, end_y)
