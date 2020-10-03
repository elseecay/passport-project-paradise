import Shakalizer as Shakal
import fields_finder as ff
from PIL import Image
import pytesseract


image_path = "pasport132.jpg"

shak = Shakal.shakalayzer()
image = Image.open(image_path)
shak.shakalayz(image)

FF = ff.fields_finder()
image_list = ["test.jpg"]
Boxes = FF.find_fields(image_list)
#print(Boxes)
for k, box in enumerate(Boxes):
	image = Image.open(image_path)
	width, height = image.size
	string_img = image.crop((box[0][0] * 2 - 2, box[0][1] * 2 - 2, box[2][0] * 2 + 3, box[2][1] * 2 + 3))
	width, height = string_img.size

	custom_oem_psm_config_one_char = r'--oem 1 --psm 7'
	if (height > 1.2 * width):
		string_img = string_img.transpose(Image.ROTATE_90)	
		text = pytesseract.image_to_string(string_img, 'rus', config=custom_oem_psm_config_one_char)
		print(text)
	else:
		text = pytesseract.image_to_string(string_img, 'rus', config=custom_oem_psm_config_one_char)
		print(text)
		
	string_img.save("tmp/" + str(k) + '.jpg')