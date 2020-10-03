import os, sys
from PIL import Image


class shakalayzer():
	def __init(self):
		pass
	
	def shakalayz (self, image):
		width, height = image.size
		new_width = width // 2
		new_height = height // 2
		image = image.resize((new_width, new_height), Image.ANTIALIAS)
		image.save("test" + ".jpg")

