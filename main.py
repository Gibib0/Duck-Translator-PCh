from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
import random
import os

class BackgroundLabel(Label):
    pass

class DuckTranslator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.duck_count = 0
        self.background_sound = None
        self.current_sound = None
        self.sounds = {}
        self.active_popup_sound = None
        self.background_position = 0

        with self.canvas.before:
            self.bg = Rectangle(source='assets/images/background.jpg', pos=self.pos, size=self.size)
            self.bind(pos=self.update_bg, size=self.update_bg)

        self.load_assets()
        self.create_ui()
        Clock.schedule_once(lambda dt: self.show_welcome_message(), 0.5)

        Clock.schedule_interval(self.increment_duck_count, 1)

        self.play_background_music()

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def load_assets(self):
        self.sounds = {
            'background': SoundLoader.load('assets/sounds/background_sound.wav'),
            'duck': SoundLoader.load('assets/sounds/duck_sound.wav'),
            'iloveyou': SoundLoader.load('assets/sounds/ILoveU_sound.wav'),
            'screamer': SoundLoader.load('assets/sounds/screamer_sound.wav'),
            'holy': SoundLoader.load('assets/sounds/holy_sound.wav')
        }

        for sound in self.sounds.values():
            if sound: sound.volume = 0.7

    def create_ui(self):
        title_label = Label(
            text = 'Duck Translator',
            font_name = 'assets/fonts/comic.ttf',
            font_size = '30sp',
            bold = True,
            size_hint = (1, 0.1),
            color=(1, 0.8, 0.2, 1)
        )
        self.add_widget(title_label)

        io_container = BoxLayout(
            orientation = 'vertical',
            size_hint = (1, 0.6),
            pos_hint = {'center_x':0.5},
            spacing = 10
        )

        self.input_text = TextInput(
            hint_text = 'Enter human text here...',
            size_hint = (0.9, 0.1),
            pos_hint={'center_x': 0.5},
            multiline = True,
            background_color = (1, 0.8, 0.8, 0.7),
            foreground_color = (0, 0, 0, 1),
            font_name = 'assets/fonts/comic.ttf',
            font_size = '16sp',
            padding = [10, 10]
        )
        self.input_text.bind(text=self.on_text_change)
        io_container.add_widget(self.input_text)

        self.output_text = TextInput(
            hint_text='Duck translation...',
            size_hint=(0.9, 0.1),
            pos_hint={'center_x': 0.5},
            multiline=True,
            readonly=True,
            background_color=(1, 0.8, 0.8, 0.7),
            foreground_color=(0, 0, 0, 1),
            font_name='assets/fonts/comic.ttf',
            font_size='16sp',
            padding=[10, 10]
        )
        io_container.add_widget(self.output_text)

        self.add_widget(io_container)

        bottom_container = BoxLayout(
            size_hint = (1, 0.2),
            pos_hint = {'center_x':0.5},
            spacing = 20
        )

        self.praise_button = Button(
            text='Praise the Great Duck',
            size_hint=(0.3, 0.15),
            pos_hint={'center_x': 0.5},
            background_color=(0.6, 1, 0.6, 1),
            color=(1, 1, 1, 1),
            font_name='assets/fonts/comic.ttf',
            font_size='16sp',
            bold=True
        )
        self.praise_button.bind(on_press=self.praise_duck)
        self.add_widget(self.praise_button)

        self.duck_counter = Label(
            text=str(self.duck_count),
            size_hint=(0.4, 0.8),
            color=(1, 1, 1, 1),
            font_name='assets/fonts/comic.ttf',
            font_size='18sp',
            bold=True
        )
        bottom_container.add_widget(self.duck_counter)

        self.add_widget(bottom_container)

    def show_welcome_message(self):
        content = BoxLayout(orientation = 'vertical', spacing = 10)
        content.add_widget(Label(
            text='From this moment ducks will come to you every second.',
            font_name='assets/fonts/comic.ttf',
            font_size='16sp',
            bold=True
        ))
        content.add_widget(Label(
            text='Dont wait until 300 ducks...',
            font_name = 'assets/fonts/comic.ttf',
            font_size='16sp',
            bold=True
        ))

        popup = Popup(
            title = 'Warning',
            title_font='assets/fonts/comic.ttf',
            content = content,
            size_hint = (0.8, 0.4),
            auto_dismiss = False
        )

        btn = Button(
            text='OK',
            size_hint_y=0.3,
            background_color=(0, 0.7, 0, 1),
            font_name='assets/fonts/comic.ttf',
            bold=True
        )
        btn.bind(on_press = popup.dismiss)
        content.add_widget(btn)
        popup.open()

    def on_text_change(self, instance, value):
        if any (phrase in value.lower() for phrase in ['я люблю тебя', 'люблю тебя', 'я тебя люблю']):
            self.show_love_message()
            return

        self.translate_text(value)

    def translate_text(self, text):
        if not text:
            self.output_text.text = ""
            return

        duck_words = ['Quack', 'quack-quack', 'HONK', 'honk-honk', 'quackle!', '(flap)', '(flap-flap)', '(puddle)', 'Quackly~ quackly~']
        translated = ' '.join([random.choice(duck_words) for _ in text.split()])
        self.output_text.text = translated

    def increment_duck_count(self, dt):
        self.duck_count += 1
        self.duck_counter.text = f'Ducks arrived: {self.duck_count}'

        if self.duck_count == 300:
            self.show_screamer()

    def show_screamer(self):
        self.play_sound('screamer')

        content = Image(source = 'assets/images/screamer.jpeg')

        popup = Popup(
            title = '!!!',
            content = content,
            size_hint = (0.9, 0.9),
            auto_dismiss = False
        )

        Clock.schedule_once(lambda dt: popup.dismiss(), 3)
        popup.bind(on_dismiss = self.on_popup_close)
        popup.open()

    def play_background_music(self):
        if self.sounds.get('background'):
            if self.sounds['background'].state == 'play':
                self.background_position = self.sounds['background'].get_pos()
                self.sounds['background'].stop()

            self.sounds['background'].loop = True
            self.sounds['background'].play()
            self.sounds['background'].seek(self.background_position)
            self.current_sound = self.sounds['background']

    def pause_current_sound(self):
        if self.current_sound and self.current_sound.state == 'play':
            self.paused_position = self.current_sound.get_pos() or 0
            self.current_sound.stop()

    def resume_background_music(self):
        background = self.sounds.get('background')
        if background:
            if hasattr(self, "paused_position") and self.paused_position is not None:
                def _resume(dt):
                    background.play()
                    background.seek(self.paused_position)
                    self.current_sound = background

                Clock.schedule_once(_resume, 0.1)
            else:
                background.play()
                self.current_sound = background

    def play_sound(self, sound_name):
        sound = self.sounds.get(sound_name)
        if sound:
            if sound_name != 'background':
                self.pause_current_sound()
                sound.play()
                self.current_sound = sound
            else:
                sound.loop = True
                sound.play()
                self.current_sound = sound

    def stop_sound(self, sound_name):
        sound = self.sounds.get(sound_name)
        if sound and sound.state == 'play':
            sound.stop()

    def on_popup_close(self, instance):
        for name, sound in self.sounds.items():
            if name != 'background' and sound and sound.state == 'play':
                sound.stop()

        self.resume_background_music()

    def praise_duck(self, instance):
        self.play_sound('duck')

        content = BoxLayout(orientation = 'vertical')
        content.add_widget(Image(source = 'assets/images/rating_up.jpeg'))
        content.add_widget(Label(
            text='U made the right choice. The Great Duck accepted ur praise.',
            font_name='assets/fonts/comic.ttf',
            font_size='16sp',
            bold=True
        ))

        popup = Popup(
            title='Praise the Great Duck',
            title_font='assets/fonts/comic.ttf',
            content=content,
            size_hint=(0.9, 0.9)
        )

        btn = Button(
            text='OK',
            size_hint_y=0.2,
            background_color=(0, 0.7, 0, 1),
            font_name='assets/fonts/comic.ttf',
            bold=True
        )
        btn.bind(on_press = popup.dismiss)
        content.add_widget(btn)

        popup.bind(on_dismiss = self.show_duck_god)
        popup.open()

    def show_duck_god(self, instance = None):
        if self.sounds.get('holy'):
            self.holy_sound = self.sounds['holy']
            self.holy_sound.play()

        content = BoxLayout(orientation = 'vertical')
        content.add_widget(Image(source = 'assets/images/duck_god.jpeg'))
        content.add_widget(Label(
            text='Now U have seen the God of Ducks',
            font_name='assets/fonts/comic.ttf',
            font_size='16sp',
            bold=True
        ))
        popup = Popup(
            title='Duck God',
            title_font='assets/fonts/comic.ttf',
            content=content,
            size_hint=(0.9, 0.9)
        )

        btn = Button(
            text='OK',
            size_hint_y=0.2,
            background_color=(0, 0.7, 0, 1),
            font_name='assets/fonts/comic.ttf',
            bold=True
        )
        btn.bind(on_press = popup.dismiss)
        content.add_widget(btn)

        popup.bind(on_dismiss=self.on_popup_close)

        def on_duck_god_close(instance):
            if hasattr(self, "holy_sound") and self.holy_sound:
                self.holy_sound.stop()
                self.holy_sound = None
            self.resume_background_music()

        popup.bind(on_dismiss=on_duck_god_close)
        popup.open()

    def show_love_message(self):
        self.play_sound('iloveyou')

        content  =BoxLayout(orientation = 'vertical')
        content.add_widget(Image(source = 'assets/images/romantic.jpg'))

        popup = Popup(
            title = 'Billy`s Love',
            title_font='assets/fonts/comic.ttf',
            content = content,
            size_hint = (0.7, 0.7)
        )

        btn = Button(
            text='OK',
            size_hint_y=0.2,
            background_color=(0, 0.7, 0, 1),
            font_name='assets/fonts/comic.ttf',
            bold=True
        )
        btn.bind(on_press = popup.dismiss)
        content.add_widget(btn)

        popup.bind(on_dismiss = self.show_cute_message)
        popup.open()

    def show_cute_message(self, instance = None):
        self.stop_sound('iloveyou')

        content = Label(
            text='And I love you ;)',
            font_name='assets/fonts/comic.ttf',
            font_size='20sp',
            bold=True,
            size_hint=(0.6, 0.4)
        )

        popup = Popup(
            title=':]',
            title_font='assets/fonts/comic.ttf',
            content=content,
            size_hint=(0.5, 0.3)
        )

        Clock.schedule_once(lambda dt: popup.dismiss(), 3)
        popup.bind(on_dismiss=lambda instance: self.resume_background_music())
        popup.open()

class DuckTranslatorApp(App):
    def build(self):
        self.title = 'Duck Translator'
        Window.set_icon('assets/icons/icon.ico')
        return DuckTranslator()

if __name__ == '__main__':
    DuckTranslatorApp().run()