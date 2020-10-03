from .Shakalizer import shakalayzer
from . import fields_finder as ff
from PIL import Image
import pytesseract


class FieldRecognizer:
	def __init__(self):
		self.shak = shakalayzer()
		self.FF = ff.fields_finder()
		self.series = ""
		self.number = ""
		self.name = ""
		self.second_name = ""
		self.middle_name = ""
		self.birthday = ""
		self.sex = ""
		self.place_of_birth = ""

		self.boxes = ""

	def __combine_closes_boxes(self):
		new_box_list = []
		parts = {}
		mark = {}
		for i in range(len(self.boxes)):
			for j in range(i + 1, len(self.boxes)):
				if (abs(min(self.boxes[i][1][0], self.boxes[j][1][0]) - max(self.boxes[i][0][0], self.boxes[j][0][0])) < 10 
				and abs(self.boxes[i][0][1] - self.boxes[j][0][1]) < 5):
					parts[i] = j

		for i in range(len(self.boxes)):
			if not (i in mark):
				mark[i] = 1
				if not (i in parts):
					new_box_list.append(self.boxes[i])
				else:
					j = parts[i]
					new_box_list.append([
						[min(self.boxes[i][0][0], self.boxes[j][0][0]), min(self.boxes[i][0][1], self.boxes[j][0][1])], 
						[max(self.boxes[i][1][0], self.boxes[j][1][0]), min(self.boxes[i][0][1], self.boxes[j][0][1])],
						[max(self.boxes[i][1][0], self.boxes[j][1][0]), max(self.boxes[i][2][1], self.boxes[j][2][1])],
						[min(self.boxes[i][0][0], self.boxes[j][0][0]), max(self.boxes[i][2][1], self.boxes[j][2][1])]]
					)
					mark[j] = 1
		self.boxes = new_box_list

	def __init_fields_by_num(self, cnt_other, text):
		if cnt_other == 1:
			self.second_name = text
		if cnt_other == 2:
			self.name = text
		if cnt_other == 3:
			self.middle_name = text
		if cnt_other == 4 or cnt_other == 5:
			if text == "МУЖ." or text == "ЖЕН.":
				self.sex = text
			else:
				self.birthday = text
		if cnt_other > 5:
			self.place_of_birth += text + ' '

	def recognize(self, img):
		image = img
		self.shak.shakalayz(image)
		image_list = ["test.jpg"]
		self.boxes = self.FF.find_fields(image_list)

		for i in range(10):
			self.__combine_closes_boxes()
		
		count_number = 0
		cnt_other = 0
		for k, box in enumerate(self.boxes):
			image = img
			width, height = image.size
			string_img = image.crop((box[0][0] * 2 - 2, box[0][1] * 2 - 2, box[2][0] * 2 + 3, box[2][1] * 2 + 3))
			width, height = string_img.size
			custom_oem_psm_config_one_char = r'--oem 1 --psm 7'
			if height > 1.2 * width:
				count_number += 1
				string_img = string_img.transpose(Image.ROTATE_90)	
				text = pytesseract.image_to_string(string_img, 'rus', config=custom_oem_psm_config_one_char)
				if count_number <= 2:
					self.series += text
				else:
					self.number += text
			else:
				cnt_other += 1
				text = pytesseract.image_to_string(string_img, 'rus', config=custom_oem_psm_config_one_char)
				self.__init_fields_by_num(cnt_other, text)
				
			string_img.save("tmp/" + str(k) + '.jpg')


if __name__ == '__main__':
	pass
