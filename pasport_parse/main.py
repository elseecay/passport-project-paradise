from PIL import Image
import field_recognize as fr

FR = fr.field_recognizer()
image_path = "image_test.jpg"
image = Image.open(image_path)
FR.recognize(image)
print("Series: ", FR.series)
print("Number: ", FR.number)
print("Name: ", FR.name)
print("Second name: ", FR.second_name)
print("Middle name: ", FR.middle_name)
print("Sex: ", FR.sex)
print("Birthday: ", FR.birthday)
print("Place of birth:", FR.place_of_birth)