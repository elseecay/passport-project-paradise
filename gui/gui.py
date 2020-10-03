# pip install kivy
# python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
# pip install PyInstaller
# python -m PyInstaller --name [exe-name] [path_to_python_file]

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
import time
import glob
from processing import passport_cropper as pc

Builder.load_string('''
<CameraClick>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Camera:
                index: 0
                id: camera
                resolution: (640, 480)
                play: True
            BoxLayout:
                height: 200
                orientation: 'vertical'
                Label:
                    text: 'Серия/Номер'
                TextInput:
                    id: series
                    font_size: '18sp'
                    height: '36dp'
                Label:
                    text: 'ФИО'
                TextInput:
                    id: fio
                    font_size: '18sp'
                    height: '36dp'
                Label:
                    text: 'Пол'
                TextInput:
                    id: gender
                    font_size: '18sp'
                    height: '36dp'
                Label:
                    text: 'Место рождения'
                TextInput:
                    id: birth_place
                    font_size: '18sp'
                    height: '36dp'
                Label:
                    text: 'Дата рождения'
                TextInput:
                    id: birthdate
                    font_size: '18sp'
                    height: '36dp'
        # ToggleButton:
        #     text: 'Play'
        #     on_press: camera.play = not camera.play
        #     size_hint_y: None
        #     height: '48dp'
        Button:
            text: 'Распознать'
            size_hint_y: None
            height: '48dp'
            on_press: root.capture()
        Button:
            text: 'Сохранить результат'
            size_hint_y: None
            height: '48dp'
            on_press: root.save()
''')


class CameraClick(BoxLayout):
    def __init__(self, recognizer):
        super().__init__()
        self.was_recognize = False
        self.recognizer = recognizer
        self.interval = 1.0
        self.event = Clock.schedule_interval(self.check_passport, self.interval)

    def check_passport(self, dt):
        pass
        # Clock.unschedule(self.event)

    def capture(self):
        camera = self.ids['camera']
        filename = "IMG_{}.png".format(time.strftime("%Y%m%d_%H%M%S"))
        camera.export_to_png(filename)

        img = pc.crop_passport_down(filename)

        self.recognizer.recognize(img)

        self.ids['series'].text = self.recognizer.series + self.recognizer.number
        self.ids['fio'].text = self.recognizer.second_name + ' ' + self.recognizer.name + ' ' + self.recognizer.middle_name
        self.ids['gender'].text = self.recognizer.sex
        self.ids['birth_place'].text = self.recognizer.place_of_birth
        self.ids['birthdate'].text = self.recognizer.birthday
        self.was_recognize = True

    def save(self):
        if hasattr(self, 'was_recognize'):
            print('okay')
        else:
            print('please recognize passport firstly')


class TestCamera(App):
    def __init__(self, recognizer):
        super().__init__()
        self.recognizer = recognizer

    def build(self):
        return CameraClick(recognizer=self.recognizer)


Window.size = (1265, 570)

if __name__ == '__main__':
    pass
