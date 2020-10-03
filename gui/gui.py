# pip install kivy
# python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
# pip install PyInstaller
# python -m PyInstaller --name [exe-name] [path_to_python_file]

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import time

Builder.load_string('''
<CameraClick>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Camera:
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
    def capture(self):
        camera = self.ids['camera']
        self.ids['series'].text = '05 17 472413'
        self.ids['fio'].text = 'Гусаров Владислав Евгеньевич'
        self.ids['gender'].text = 'Муж.'
        filename = "IMG_{}.png".format(time.strftime("%Y%m%d_%H%M%S"))
        camera.export_to_png(filename)
        self.was_recognize = True

    def save(self):
        if hasattr(self, 'was_recognize'):
            print('okay')
        else:
            print('please recognize passport firstly')


class TestCamera(App):
    def build(self):
        return CameraClick()


Window.size = (1265, 570)

TestCamera().run()
