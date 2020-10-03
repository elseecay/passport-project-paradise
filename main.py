import os
import sys
from pasport_parse import field_recognize as fr
from gui.gui import TestCamera

pass_recognizer = fr.FieldRecognizer()
TestCamera(recognizer=pass_recognizer).run()

